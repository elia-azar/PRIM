-- This test does the following:
-- 	1. Execute ARP so that the devices exchange MAC-addresses
--	2. Send UDP packets from NIC 1 to NIC 2
-- 	3. Read the statistics from the recieving device
--
-- This script demonstrates how to access device specific statistics ("normal" stats and xstats) via DPDK

local mg     = require "moongen"
local memory = require "memory"
local device = require "device"
local ts     = require "timestamping"
local filter = require "filter"
local hist   = require "histogram"
local stats  = require "stats"
local timer  = require "timer"
local arp    = require "proto.arp"
local log    = require "log"

local ffi = require "ffi"
seed = 42
math.randomseed(seed)

-- set addresses here
local DST_MAC     = "aa:cc:dd:cc:00:01" -- resolved via ARP on GW_IP or DST_IP, can be overriden with a string here
local SRC_IP_BASE = "179.14.12.10"
local DST_IP      = "10.0.0.10"
local SRC_PORT    = 1234
local DST_PORT    = 320

local RAND_PORT = 10
--local test_counter = 0
--local test_IP = "10.10.10.1"

-- answer ARP requests for this IP on the rx port
-- change this if benchmarking something like a NAT device
local RX_IP   = DST_IP
-- used to resolve DST_MAC
local GW_IP   = DST_IP
-- used as source IP to resolve GW_IP to DST_MAC
local ARP_IP  = SRC_IP_BASE


local C = ffi.C

--local file = io.open("/opt/pcap/counter.txt","w")

function configure(parser)
	parser:description("Generates UDP traffic and prints out device statistics. Edit the source to modify constants like IPs.")
	parser:argument("txDev", "Device to transmit from."):convert(tonumber)
	--parser:argument("rxDev", "Device to receive from."):convert(tonumber)
	parser:option("-r --rate", "Transmit rate in Mbit/s."):default(10000):convert(tonumber)
	parser:option("-s --size", "Packet size."):default(60):convert(tonumber)
	parser:option("-p --percentage", "Percentage of matching filter."):default(10):convert(tonumber)
end

function master(args)
	txDev = device.config{port = args.txDev, rxQueues = 4, txQueues = 4}
	--rxDev = device.config{port = args.rxDev, rxQueues = 4, txQueues = 4}
	device.waitForLinks()
	-- max 1kpps timestamping traffic timestamping
	-- rate will be somewhat off for high-latency links at low rates
	if args.rate > 0 then
		txDev:getTxQueue(0):setRate(args.rate / 2 - (args.size + 4) * 8 / 1000)
		txDev:getTxQueue(1):setRate(args.rate / 4 - (args.size + 4) * 8 / 1000)
		txDev:getTxQueue(2):setRate(args.rate / 4 - (args.size + 4) * 8 / 1000)
	end
	--print("PERCENTAGE" .. args.percentage)
	RAND_PORT = args.percentage
	print("RAND_PORT" .. RAND_PORT)
	--rxDev:getTxQueue(0).dev:UdpGenericFilter(rxDev:getRxQueue(3))

	mg.startTask("loadSlave", txDev:getTxQueue(0), args.size, args.percentage)
	mg.startTask("loadSlave", txDev:getTxQueue(1), args.size, args.percentage)
	mg.startTask("loadSlave", txDev:getTxQueue(2), args.size, args.percentage)
	--mg.startTask("loadSlave2", txDev:getTxQueue(3), args.size)
	--mg.startTask("receiveSlave", rxDev:getRxQueue(3), args.size)
	arp.startArpTask{
		-- run ARP on both ports
		--{ rxQueue = rxDev:getRxQueue(2), txQueue = rxDev:getTxQueue(2), ips = RX_IP },
		-- we need an IP address to do ARP requests on this interface
		--{ rxQueue = txDev:getRxQueue(2), txQueue = txDev:getTxQueue(2), ips = ARP_IP }
	}
	mg.waitForTasks()
end

function randomDstMacAddress()
	DST_MAC=""
	rand = math.random(math.pow(2,48))
	b = (string.format('%012x', rand))
	DST_MAC = DST_MAC .. string.sub(b,1,2)

	for i=3,11,2 do
		DST_MAC = DST_MAC .. ":" .. string.sub(b, i, i+1)
	end
	return DST_MAC
end

function dstPort(percentage)
        local num = math.random(1,10)
	if num <= percentage then
		DST_PORT = 320
	else
		DST_PORT = 1320
	end
end

function randomDstIP()
	local num_1 = math.random(5,12)
	local num_2 = math.random(255)
	DST_IP = "10." .. num_1 .. "." .. num_2 .. ".1"
	--if num_1 == 10 and num_2 == 10 then
	--	test_counter = test_counter + 1
		--file:write(test_counter .. "\n")
	--print("MATCH " .. test_counter)
	--end
end

local function fillUdpPacket(buf, len, percentage)
	--randomDstIP()
	dstPort(percentage)
	--if DST_IP == test_IP then
	--	test_counter = test_counter + 1
	--	file:write(test_counter .. "\n")
	--end
	buf:getUdpPacket():fill{
		ethSrc = queue,
		ethDst = DST_MAC,
		ip4Src = SRC_IP,
		ip4Dst = DST_IP,
		udpSrc = SRC_PORT,
		udpDst = DST_PORT,
		pktLength = len
	}

	buf:getEthernetPacket():fill{
            ethSrc = queue,
            ethDst = DST_MAC,
            ethType = 0x0800
        }
end


--- Runs on the sending NIC
--- Generates UDP traffic and also fetches the stats
function loadSlave(queue, size, percentage)

	log:info(green("Starting up: LoadSlave"))

	local mempool = memory.createMemPool(function(buf)
		fillUdpPacket(buf, size, percentage)
	end)
	local bufs = mempool:bufArray()
	local txCtr = stats:newDevTxCounter(queue, "plain")
	--local rxCtr = stats:newDevRxCounter(rxDev, "plain")
	local baseIP = parseIPAddress(SRC_IP_BASE)

	-- send out UDP packets until the user stops the script
	while mg.running() do
		bufs:alloc(size)
		for i, buf in ipairs(bufs) do
			local pkt = buf:getUdpPacket()
			pkt.ip4.src:set(baseIP)
		end
		-- UDP checksums are optional, so using just IPv4 checksums would be sufficient here
		bufs:offloadUdpChecksums()
		queue:send(bufs)
		txCtr:update()
		--rxCtr:update()
	end
	txCtr:finalize()
	--rxCtr:finalize()

	local drop = {}
	for i=3, #txCtr.mpps-2
	do
		drop[i-2] = txCtr.mpps[i] -- - rxCtr.mpps[i]
	end
	--file:close()
	print("Avg Drop: " .. stats.average(drop) .. "  stdDev: " .. stats.stdDev(drop))

end


--- Runs on the sending NIC
--- Generates UDP traffic and also fetches the stats
function loadSlave2(queue, size)

	log:info(green("Starting up: LoadSlave2"))

	local mempool = memory.createMemPool(function(buf)
		fillUdpPacket(buf, size)
	end)
	local bufs = mempool:bufArray()
	local txCtr = stats:newDevTxCounter(queue, "plain")
	--local rxCtr = stats:newDevRxCounter(rxDev, "plain")
	local baseIP = parseIPAddress(SRC_IP_BASE)

	-- send out UDP packets until the user stops the script
	while mg.running() do
		bufs:alloc(size)
		for i, buf in ipairs(bufs) do
			local pkt = buf:getUdpPacket()
			pkt.ip4.src:set(baseIP)
		end
		-- UDP checksums are optional, so using just IPv4 checksums would be sufficient here
		bufs:offloadUdpChecksums()
		queue:send(bufs)
		txCtr:update()
		--rxCtr:update()
	end
	txCtr:finalize()
	--rxCtr:finalize()

	local drop = {}
	for i=3, #txCtr.mpps-2
	do
		drop[i-2] = txCtr.mpps[i] -- - rxCtr.mpps[i]
	end

	print("Avg Drop: " .. stats.average(drop) .. "  stdDev: " .. stats.stdDev(drop))

end
