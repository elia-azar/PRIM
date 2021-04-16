# Measuring packet loss vs filter size

## Overview
In this section, we describe how packet loss varies with regard to the filter size.

We created 7 filters in filters.txt that were used to match the incoming packets.

The results were saved in a txt file inside data/. 

For a given file results_dump${i}_.txt, $i*10 represents the percentage of packets that matches the filter. For example, results_dump4_.txt contains the results for 40% packets matching the filter.

The data inside the file is organized in such way that the first 50 results are for tests that were performed against the first filter, the second 50 results for tests against the second filter, and so forth.

To run the tests, open a terminal and run the following:

```
$ sudo ./automate_filter.sh
```

This will take approx. 24 hours to finish.

## Result Analysis
We ran 50 tests per filter in the list. The obtained results have the following format:

```
New results
[1;36m[Capture, thread #1] RX[0m: 2.53 (StdDev 0.95) Mpps, 1296 (StdDev 485) Mbit/s (1701 Mbit/s with framing), total 167074511 packets with 10692768704 bytes (incl. CRC)
[1;36m[Filter reject, thread #1] RX[0m: 4.05 (StdDev 1.52) Mpps, 2073 (StdDev 776) Mbit/s (2720 Mbit/s with framing), total 267190572 packets with 17100196608 bytes (incl. CRC)
[1;36m[Device: id=0] RX[0m: 12.93 (StdDev 4.91) Mpps, 6620 (StdDev 2515) Mbit/s (8689 Mbit/s with framing), total 860973498 packets with 55102303872 bytes (incl. CRC)
...
```

* New results indicates that the following is the result of a new test.

* [Capture, thread #1] indicates the total number of packets that were captured by the filter; the number of packets can be seen after the keyword 'total' (167074511 packets).

* [Filter reject, thread #1] indicates the total number of packets that were rejected by the filter; the number of packets can be seen after the keyword 'total' (267190572 packets).

* [Device: id=0] indicates the total number of packets that were received by the listening interface, the number of packets can be seen after the keyword 'total' (860973498 packets).


## Data to plot

To transform raw data to a plot, we use plot.py that reads and parses the data insisde a given file in data/, and then plot the packet loss over the filter size by averaging over 50 for each filter. We also include the 95% confidence interval in the plot.