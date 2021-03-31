#include<stdio.h>
#include "pkt-filter.h"

extern FILE* pFile;

void open_pcap_file();
void pkts_save(headers hdr);
void close_pcap_file();