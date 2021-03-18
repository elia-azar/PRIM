#!/bin/bash

cd $TRAFFIC_GEN

rate=10000
size=60
percentage=10
echo 'STARTING Moongen traffic generator'

while getopts ":s:r:p:" arg; do
	case "${arg}" in
		s)
			size=${OPTARG}
			;;
		r)
			rate=${OPTARG}
			;;
                p)
                        percentage=${OPTARG}
                        ;;
	esac
done

echo "$TRAFFIC_GEN/unidirectional_one_port-test.sh -r '${rate}' -s '${size}' -p '${percentage}'"

$TRAFFIC_GEN/unidirectional_one_port-test.sh -r "${rate}" -s "${size}" -p "${percentage}"
