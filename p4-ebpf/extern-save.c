#include "extern-save.h"

FILE* pFile = NULL;

void open_pcap_file(){
    // open for writing in binary mode
    pFile = fopen ("myfile.pcap" , "wb");
    return;
}

void pkts_save(headers hdr){
    fwrite (&hdr, 1, sizeof(headers) , pFile);
}

void close_pcap_file(){
    fclose(pFile);
    return
}