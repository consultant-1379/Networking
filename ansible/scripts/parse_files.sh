#!/bin/bash
for file in /etc/ansible/scripts/*.log; do
    echo "networks:" > "${file%.*}".yml
    while read p; do
	#~# Assign Variables
	VLAN=$(echo  $p | awk '{print $1}' | grep -v 2018-08-15 | grep -v 'Default' | grep -v 'Mgmt')# >> "${file%.*}".yml
	TAG=$(echo  $p | awk '{print $2}' | grep -v 2018-08-15 | grep -v 'Default' | grep -v 'Mgmt')# >> "${file%.*}".yml
	IP_ADDR=$(echo  $p | awk '{print $3}' | grep -v 2018-08-15 | grep -v 'Default' | grep -v 'Mgmt')# >> "${file%.*}".yml
	MASK=$(echo  $p | awk '{print $4}' | grep -v 2018-08-15 | grep -v 'Default' | grep -v 'Mgmt')# >> "${file%.*}".yml
	#~# Now echo vars to file
        echo "  - name: " $VLAN >> "${file%.*}".yml
        echo "    tag:" $TAG >> "${file%.*}".yml
	if [[ $IP_ADDR != *"-"* ]]; then
           echo "    ip:" $IP_ADDR$MASK >> "${file%.*}".yml
        fi
    done < $file
done
