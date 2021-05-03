# Measuring packet loss vs pkts matching the filter

## Overview
In this section, we describe how packet loss varies with regard to the percentage of packets matching the filter by maitaining a stable throughput of 14.8 Mpps.

The results were saved in a txt file inside data/.

* results_${method}${i}.txt, with $i*10 representing the percentage of packets that matches the filter. For example, results_moongen5.txt contains the results for 50% packets matching the moongen's filter.

To run the tests, open a terminal and run the following:

```
$ sudo ../src/automate_percentage.sh
```

## Result Analysis
We ran 50 tests per throughput. The obtained results in results_${method}${i}.txt have the following format (The files were manually edited to have a file that's easy to read):

```
Capture 253228727 
Filter  260630008 
Device: 862932105

...
```

* Capture indicates the total number of packets that were captured by the filter, 253228727 packets in this case.

* Filter indicates the total number of packets that were rejected by the filter, 260630008 packets in this case.

* Device indicates the total number of packets that were received by the interface, 862932105 packets in this case.


## Data to plot

To transform raw data to a plot, we use plot_loss.py that reads and parses the data insisde data/, and then plot the packet loss over the percentage of packets matching the filter. We also include the 95% confidence interval in the plot.

To obtain the graph of captured, rejected and received packets over the percentage of packets matching the filter, we use plot.py.