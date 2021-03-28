typedef struct ethernet_hdr_s {
   uint8_t dst[6];    /* destination host address */
   uint8_t src[6];    /* source host address */
   uint8_t type;     /* IP? ARP? RARP? etc */
} ethernet_hdr_t;

typedef struct ip_hdr_s {
   uint8_t ip_hl:4;
   uint8_t ip_v:5;
   uint8_t ip_tos;
   uint8_t ip_len;
   uint8_t ip_id;
   uint8_t ip_off;
   uint8_t ip_ttl;
   uint8_t ip_p;
   uint8_t ip_sum;
   uint8_t ip_src;
   uint8_t ip_dst;
}ip_hdr_t;

typedef struct udp_header{
    uint8_t src;
    uint8_t dst;
    uint8_t length;
    uint8_t checksum;
} udp_header_t;

void pkts_save(headers* hdr){
    pcaprec_hdr_t pcaprec_hdr;
    // fill pcaprec_hdr with valid info

    FILE* pFile = NULL;
    pFile = fopen ("myfile.pcap" , "wb"); // open for writing in binary mode

    fwrite (&pcaprec_hdr, 1, sizeof(pcaprec_hdr_t) , pFile);

    fclose(pFile);
}