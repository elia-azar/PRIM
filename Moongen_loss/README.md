# Measuring packet loss vs filter size

## Overview
In this section, we describe how packet loss varies with regard to throughput varying from 1 Mpps to 14.8 Mpps.

The results were saved in a txt file inside data/. Inside this repository, we have 2 type of files:

* results_dump${i}.txt, if 1 <= $i <= 11, this file contains the results of the receiving interface for a throughput of $i Mpps. If 12 <= $i, then the file will contain the results for a throughput of min(14.8, $(11 + ($i-11)/2)) Mpps approx.

* results_generator${i}.txt, this file contains throughput value for 50 tests.

To run the tests, open a terminal and run the following:

```
$ sudo ../src/automate.sh
```

## Result Analysis
We ran 50 tests per throughput. The obtained results in results_dump${i}.txt have the following format:

```
New results
[1;36m[Capture, thread #1] RX[0m: 0.87 (StdDev 0.34) Mpps, 444 (StdDev 173) Mbit/s (583 Mbit/s with framing), total 58100424 packets with 3718427136 bytes (incl. CRC)
[1;36m[Filter reject, thread #1] RX[0m: 0.00 (StdDev 0.00) Mpps, 0 (StdDev 0) Mbit/s (0 Mbit/s with framing), total 0 packets with 0 bytes (incl. CRC)
[1;36m[Device: id=0] RX[0m: 0.87 (StdDev 0.33) Mpps, 447 (StdDev 169) Mbit/s (587 Mbit/s with framing), total 58129596 packets with 3720294144 bytes (incl. CRC)
...
```

* New results indicates that the following is the result of a new test.

* [Capture, thread #1] indicates the total number of packets that were captured by the filter; the number of packets can be seen after the keyword 'total' (58100424 packets).

* [Filter reject, thread #1] indicates the total number of packets that were rejected by the filter; the number of packets can be seen after the keyword 'total' (0 packets).

* [Device: id=0] indicates the total number of packets that were received by the listening interface, the number of packets can be seen after the keyword 'total' (58129596 packets).


The obtained results in results_generator${i}.txt have the following format:

```
New results ${i}
[0;34m[Device: id=0] TX[0m: 0.97 (StdDev 0.00) Mpps, 498 (StdDev 2) Mbit/s (653 Mbit/s with framing), total 56521092 packets with 3617349568 bytes (incl. CRC)
[0;34m[Device: id=0] TX[0m: 0.01 (StdDev 0.00) Mpps, 7 (StdDev 0) Mbit/s (9 Mbit/s with framing), total 774534 packets with 49571136 bytes (incl. CRC)
[0;34m[Device: id=0] TX[0m: 0.01 (StdDev 0.00) Mpps, 7 (StdDev 1) Mbit/s (10 Mbit/s with framing), total 833970 packets with 53373440 bytes (incl. CRC)
...
```

* New results indicates that the following is the result of a new test.

* We have 3 [Device: id=0] because we created 3 TX queues. To get the otal number of packets sent, we compute the sum of the 3 devices by taking the number after the keyword 'total'. In this example, total_packets = 56521092 + 774534 + 833970 = 58129596 packets.

## Data to plot

To transform raw data to a plot, we use plot.py that reads and parses the data insisde a given file in data/, and then plot the packet loss over the throughput by averaging over 50 for a given value of the throughput. We also include the 95% confidence interval in the plot.