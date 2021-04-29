#include <rte_>

struct rte_eth_xstat_name *xstats_names;
uint64_t *values;
int len, i;
/* Get number of stats */
len = rte_eth_xstats_get_names_by_id(port_id, NULL, NULL, 0);
if (len < 0) {
    printf("Cannot get xstats count\n");
    goto err;
}
xstats_names = malloc(sizeof(struct rte_eth_xstat_name) * len);
if (xstats_names == NULL) {
    printf("Cannot allocate memory for xstat names\n");
    goto err;
}
/* Retrieve xstats names, passing NULL for IDs to return all statistics */
if (len != rte_eth_xstats_get_names_by_id(port_id, xstats_names, NULL, len)) {
    printf("Cannot get xstat names\n");
    goto err;
}
values = malloc(sizeof(values) * len);
if (values == NULL) {
    printf("Cannot allocate memory for xstats\n");
    goto err;
}
/* Getting xstats values */
if (len != rte_eth_xstats_get_by_id(port_id, NULL, values, len)) {
    printf("Cannot get xstat values\n");
    goto err;
}
/* Print all xstats names and values */
for (i = 0; i < len; i++) {
    printf("%s: %"PRIu64"\n", xstats_names[i].name, values[i]);
}



uint64_t id;
uint64_t value;
const char *xstat_name = "rx_errors";
if(!rte_eth_xstats_get_id_by_name(port_id, xstat_name, &id)) {
rte_eth_xstats_get_by_id(port_id, &id, &value, 1);
printf("%s: %"PRIu64"\n", xstat_name, value);
}
else {
printf("Cannot find xstats with a given name\n");
goto err;
}


#define APP_NUM_STATS 4
/* application cached these ids previously; see above */
uint64_t ids_array[APP_NUM_STATS] = {3,4,7,21};
uint64_t value_array[APP_NUM_STATS];
/* Getting multiple xstats values from array of IDs */
rte_eth_xstats_get_by_id(port_id, ids_array, value_array, APP_NUM_STATS);
uint32_t i;
for(i = 0; i < APP_NUM_STATS; i++) {
printf("%d: %"PRIu64"\n", ids_array[i], value_array[i]);
}