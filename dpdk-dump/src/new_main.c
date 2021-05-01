#include <pcap/pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <errno.h>
#include <libgen.h>
#include <sys/queue.h>
#include <sys/syscall.h>
#include <math.h>
#include <sched.h>
#include <pthread.h>
#include <unistd.h>

#include <rte_common.h>
#include <rte_log.h>
#include <rte_memory.h>
#include <rte_memcpy.h>
#include <rte_memzone.h>
#include <rte_tailq.h>
#include <rte_errno.h>
#include <rte_eal.h>
#include <rte_per_lcore.h>
#include <rte_launch.h>
#include <rte_lcore.h>
#include <rte_branch_prediction.h>
#include <rte_interrupts.h>
#include <rte_pci.h>
#include <rte_debug.h>
#include <rte_ether.h>
#include <rte_ethdev.h>
#include <rte_ring.h>
#include <rte_log.h>
#include <rte_mempool.h>
#include <rte_mbuf.h>
#include <rte_string_fns.h>
#include <rte_cycles.h>
#include <rte_atomic.h>
#include <rte_version.h>


/* Constants of the system */
#define MEMPOOL_NAME "cluster_mem_pool"				// Name of the NICs' mem_pool, useless comment....
#define MEMPOOL_ELEM_SZ 2048  					// Power of two greater than 1500
#define MEMPOOL_CACHE_SZ 512  					// Max is 512

#define INTERMEDIATERING_NAME "intermedate_ring"

#define RX_QUEUE_SZ 4096			// The size of rx queue. Max is 4096 and is the one you'll have best performances with. Use lower if you want to use Burst Bulk Alloc.
#define TX_QUEUE_SZ 256			// Unused, you don't tx packets
#define PKT_BURST_SZ 4096		// The max size of batch of packets retreived when invoking the receive function. Use the RX_QUEUE_SZ for high speed

/* RSS symmetrical 40 Byte seed, according to "Scalable TCP Session Monitoring with Symmetric Receive-side Scaling" (Shinae Woo, KyoungSoo Park from KAIST)  */
uint8_t rss_seed [] = {	0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a,
			0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a,
			0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a,
			0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a,
			0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a, 0x6d, 0x5a
};

/* Struct for devices configuration for const defines see rte_ethdev.h */
static const struct rte_eth_conf port_conf = {
	.rxmode = {
		.mq_mode = ETH_MQ_RX_RSS,  	/* Enable RSS */
	},
	.txmode = {
		.mq_mode = ETH_MQ_TX_NONE,
	},
	.rx_adv_conf = {
		.rss_conf = {
			.rss_key = rss_seed,				/* Set the seed,					*/
			.rss_key_len = 40,				/* and the seed length.					*/
			.rss_hf = (ETH_RSS_IPV4_TCP | ETH_RSS_UDP) ,	/* Set the mask of protocols RSS will be applied to 	*/
		}	
	}
};

/* Struct for configuring each rx queue. These are default values */
static const struct rte_eth_rxconf rx_conf = {
	.rx_thresh = {
		.pthresh = 8,   /* Ring prefetch threshold */
		.hthresh = 8,   /* Ring host threshold */
		.wthresh = 4,   /* Ring writeback threshold */
	},
	.rx_free_thresh = 32,    /* Immediately free RX descriptors */
};

/* Struct for configuring each tx queue. These are default values */
static const struct rte_eth_txconf tx_conf = {
	.tx_thresh = {
		.pthresh = 36,  /* Ring prefetch threshold */
		.hthresh = 0,   /* Ring host threshold */
		.wthresh = 0,   /* Ring writeback threshold */
	},
	.tx_free_thresh = 0,    /* Use PMD default values */
	.txq_flags = ETH_TXQ_FLAGS_NOOFFLOADS | ETH_TXQ_FLAGS_NOMULTSEGS,  /* IMPORTANT for vmxnet3, otherwise it won't work */
	.tx_rs_thresh = 0,      /* Use PMD default values */
};


/* Global vars */
static volatile bool force_quit;
static uint16_t port_id;
char * file_name = NULL;
pcap_dumper_t * pcap_file_p;
uint64_t buffer_size = 1048576;
uint64_t max_size = 0 ;
uint64_t nb_captured_packets = 0;
uint64_t nb_dumped_packets = 0;
uint64_t sz_dumped_file = 0;
uint64_t start_secs;
pcap_t *pd;
int nb_sys_ports;
static struct rte_mempool * pktmbuf_pool;
static struct rte_ring    * intermediate_ring;

void print_stats(void){
	struct rte_eth_stats stat;
	int i;
	uint64_t good_pkt = 0, miss_pkt = 0;

	/* Print per port stats */
	for (i = 0; i < nb_sys_ports; i++){	
		rte_eth_stats_get(i, &stat);
		good_pkt += stat.ipackets;
		miss_pkt += stat.imissed;
		printf("\nPORT: %2d Rx: %ld Drp: %ld Tot: %ld Perc: %.3f%%", i, stat.ipackets, stat.imissed, stat.ipackets+stat.imissed, (float)stat.imissed/(stat.ipackets+stat.imissed)*100 );
	}
	printf("\n-------------------------------------------------");
	printf("\nTOT:     Rx: %ld Drp: %ld Tot: %ld Perc: %.3f%%", good_pkt, miss_pkt, good_pkt+miss_pkt, (float)miss_pkt/(good_pkt+miss_pkt)*100 );
	printf("\n");

}

/* Loop function, batch timing implemented */
static int main_loop_producer(__attribute__((unused)) void * arg){
	struct rte_mbuf * pkts_burst[PKT_BURST_SZ];
	struct timeval t_pack;
	struct rte_mbuf * m;
	int read_from_port = 0;
	int i, nb_rx, ret;


	/* Start stats */
   	alarm(1);

	rte_eth_stats_reset(port_id);


	while (!force_quit) {

		/* Read a burst for current port at queue 'nb_istance'*/
		nb_rx = rte_eth_rx_burst(read_from_port, 0, pkts_burst, PKT_BURST_SZ);

		/* For each received packet. */
		for (i = 0; likely( i < nb_rx ) ; i++) {

			/* Retreive packet from burst, increase the counter */
			m = pkts_burst[i];
			nb_captured_packets++;

			/* Timestamp the packet */
			ret = gettimeofday(&t_pack, NULL);
			if (ret != 0) 
				rte_exit(EXIT_FAILURE,"Error: gettimeofday failed. Quitting...\n");

			/* Writing packet timestamping in unused mbuf fields. (wild approach ! ) */
			m->tx_offload = t_pack.tv_sec;
			m->udata64 =  t_pack.tv_usec;

			/*Enqueieing buffer */
			ret = rte_ring_enqueue(intermediate_ring, m);

		}

		/* Increasing reading port number in Round-Robin logic */
		read_from_port = (read_from_port + 1) % nb_sys_ports;

	}
	return 0;
}

static int main_loop_consumer(__attribute__((unused)) void * arg){

	struct timeval t_pack;
	struct rte_mbuf * m;
	u_char * packet;
	char file_name_rotated [1000];
	int ret;
	struct pcap_pkthdr pcap_hdr;

	/* Open pcap file for writing */
	pd = pcap_open_dead(DLT_EN10MB, 65535 );
	pcap_file_p = pcap_dump_open(pd, file_name);
	if(pcap_file_p==NULL)
		rte_exit(EXIT_FAILURE,"Error in opening pcap file\n");
	printf("Opened file %s\n", file_name);

	/* Init first rotation */
	ret = gettimeofday(&t_pack, NULL);
	if (ret != 0) 
		rte_exit(EXIT_FAILURE,"Error: gettimeofday failed. Quitting...\n");
	start_secs = t_pack.tv_sec;


	while (!force_quit) {

		/* Dequeue packet */
		ret = rte_ring_dequeue(intermediate_ring, (void**)&m);
		
		/* Continue polling if no packet available */
		if( unlikely (ret != 0)) continue;

		/* Read timestamp of the packet */
		t_pack.tv_usec = m->udata64;
		t_pack.tv_sec = m->tx_offload;

		/* Compile pcap header */
		pcap_hdr.ts = t_pack;
		pcap_hdr.caplen = rte_pktmbuf_data_len(m); 
		pcap_hdr.len = rte_pktmbuf_data_len(m); 
		packet = rte_pktmbuf_mtod(m, u_char * ); 	

		/* Write on pcap */
		pcap_dump ((u_char *)pcap_file_p, & pcap_hdr,  packet);
		nb_dumped_packets++;
		sz_dumped_file += rte_pktmbuf_data_len(m) + sizeof (pcap_hdr) ;

		/* Free the buffer */
		rte_pktmbuf_free((struct rte_mbuf *)m);
	}
}

static void
assert_link_status(void)
{
	struct rte_eth_link link;
	uint8_t rep_cnt = MAX_REPEAT_TIMES;
	int link_get_err = -EINVAL;

	memset(&link, 0, sizeof(link));
	do {
		link_get_err = rte_eth_link_get(port_id, &link);
		if (link_get_err == 0 && link.link_status == ETH_LINK_UP)
			break;
		rte_delay_ms(CHECK_INTERVAL);
	} while (--rep_cnt);

	if (link_get_err < 0)
		rte_exit(EXIT_FAILURE, ":: error: link get is failing: %s\n",
			 rte_strerror(-link_get_err));
	if (link.link_status == ETH_LINK_DOWN)
		rte_exit(EXIT_FAILURE, ":: error: link is still down\n");
}

/* Init each port with the configuration contained in the structs. Every interface has nb_sys_cores queues */
static void init_port(int port_id) {

	int ret;
	uint8_t rss_key [40];
	struct rte_eth_link link;
	struct rte_eth_dev_info dev_info;
	struct rte_eth_rss_conf rss_conf;
	struct rte_eth_fdir fdir_conf;

	/* Retreiving and printing device infos */
	ret = rte_eth_dev_info_get(port_id, &dev_info);
	if (ret != 0)
		rte_exit(EXIT_FAILURE,
		"Error during getting device (port %u) info: %s\n",
		port_id, strerror(-ret));

	/* Configure device with '1' rx queues and 1 tx queue */
	printf(":: initializing port: %d\n", port_id);
	ret = rte_eth_dev_configure(port_id, 1, 1, &port_conf);
	if (ret < 0) {
		rte_exit(EXIT_FAILURE,
		":: cannot configure device: err=%d, port=%u\n",
		ret, port_id);
	}

	/* For each RX queue in each NIC */
	/* Configure rx queue j of current device on current NUMA socket. It takes elements from the mempool */
	ret = rte_eth_rx_queue_setup(port_id, 0, RX_QUEUE_SZ, rte_eth_dev_socket_id(port_id), &rx_conf, pktmbuf_pool);
	if (ret < 0) {
		rte_exit(EXIT_FAILURE,
		":: Rx queue setup failed: err=%d, port=%u\n",
		ret, port_id);
	}
	/* Configure mapping [queue] -> [element in stats array] */
	ret = rte_eth_dev_set_rx_queue_stats_mapping(port_id, 0, 0);
	if (ret < 0) {
		rte_exit(EXIT_FAILURE,
		":: Error configuring receiving queue stats: err=%d, port=%u\n",
		ret, port_id);
	}


	/* Configure tx queue of current device on current NUMA socket. Mandatory configuration even if you want only rx packet */
	ret = rte_eth_tx_queue_setup(port_id, 0, TX_QUEUE_SZ, rte_eth_dev_socket_id(port_id), &tx_conf);
	if (ret < 0) {
		rte_exit(EXIT_FAILURE,
		":: Tx queue setup failed: err=%d, port=%u\n",
		ret, port_id);
	}

	/* enable promiscuous mode */
	ret = rte_eth_promiscuous_enable(port_id);
	if (ret != 0)
		rte_exit(EXIT_FAILURE,
		":: promiscuous mode enable failed: err=%s, port=%u\n",
		rte_strerror(-ret), port_id);

	/* Start device */		
	ret = rte_eth_dev_start(port_id);
	if (ret < 0) {
		rte_exit(EXIT_FAILURE,
		"rte_eth_dev_start:err=%d, port=%u\n",
		ret, port_id);
	}

	assert_link_status();

	printf(":: initializing port: %d done\n", port_id);
}

void alarm_routine (__attribute__((unused)) int unused){

	/* If the program is quitting don't print anymore */
	if(force_quit) return;

	/* Print per port stats */
	print_stats();

	/* Schedule an other print */
	alarm(1);
	signal(SIGALRM, alarm_routine);

}

/* Signal handling function */
static void signal_handler(int signum)
{
	uint64_t diff;
	int ret;
	struct timeval t_end;

	if (signum == SIGINT || signum == SIGTERM) {
		printf("\n\nSignal %d received, preparing to exit...\n", signum);
		/* Signal the shutdown */
		force_quit = true;

		/* Print the per port stats  */
		printf("\n\nQUITTING...\n");

		ret = gettimeofday(&t_end, NULL);
		if (ret != 0) FATAL_ERROR("Error: gettimeofday failed. Quitting...\n");		
		diff = t_end.tv_sec - start_secs;
		printf("The capture lasted %ld seconds.\n", diff);
		print_stats();

		/* Close the pcap file */
		pcap_close(pd);
		pcap_dump_close(pcap_file_p);
		exit(0);
	}
}

static int parse_args(int argc, char **argv)
{
	int option;
	
	/* Retrive arguments */
	while ((option = getopt(argc, argv,"w:W:")) != -1) {
        switch (option) {
            case 'w' : file_name = strdup(optarg); /* File name, mandatory */
                break;
            default: return -1; 
		}
   	}
	return 0;
}


/* Main function */
int main(int argc, char **argv)
{
	int ret;
	uint16_t nr_ports;
	struct rte_flow_error error;
	int i;

	ret = rte_eal_init(argc, argv);
	if (ret < 0)
		rte_exit(EXIT_FAILURE, ":: invalid EAL arguments\n");

	argc -= ret;
	argv += ret;

	/* parse application arguments (after the EAL ones) */
	ret = parse_args(argc, argv);
	if (ret < 0)
		rte_exit(EXIT_FAILURE, "Invalid parameters\n");

	/* Configure signal handlers */
	force_quit = false;
	signal(SIGINT, signal_handler);
	signal(SIGTERM, signal_handler);
	signal(SIGALRM, alarm_routine);

	/* Check if this application can use two cores*/
	ret = rte_lcore_count ();
	if (ret != 2) 
		rte_exit(EXIT_FAILURE, ":: This application needs exactly two (2) cores, available %i.\n", ret);

	/* Get number of ethernet devices */
	nb_sys_ports = rte_eth_dev_count_avail();
	if (nb_sys_ports == 0)
		rte_exit(EXIT_FAILURE, ":: no Ethernet ports found\n");
	port_id = 0;

	if (nb_sys_ports != 1) {
		printf(":: warn: %d ports detected, but we use only one: port %u\n", nr_ports, port_id);
	}
	
	/* Create a mempool with per-core cache, initializing every element for be used as mbuf, and allocating on the current NUMA node */
	pktmbuf_pool = rte_mempool_create(MEMPOOL_NAME, buffer_size-1, MEMPOOL_ELEM_SZ, MEMPOOL_CACHE_SZ, sizeof(struct rte_pktmbuf_pool_private), rte_pktmbuf_pool_init, NULL, rte_pktmbuf_init, NULL,rte_socket_id(), 0);
	if (pktmbuf_pool == NULL)
		rte_exit(EXIT_FAILURE, "Cannot init mempool\n");
	
	/* Init intermediate queue data structures: the ring. */
	intermediate_ring = rte_ring_create(INTERMEDIATERING_NAME, buffer_size, rte_socket_id(), RING_F_SP_ENQ | RING_F_SC_DEQ );
 	if (intermediate_ring == NULL)
		rte_exit(EXIT_FAILURE, "Cannot create ring\n");

	init_port(port_id);

	/* Start consumer and producer routine on 2 different cores: consumer launched first... */
	ret =  rte_eal_mp_remote_launch(main_loop_consumer, NULL, SKIP_MASTER);
	if (ret != 0) 
		rte_exit(EXIT_FAILURE,"Cannot start consumer thread\n");	

	/* ... and then loop in consumer */
	main_loop_producer(NULL);	

	return 0;
}