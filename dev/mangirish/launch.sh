#!/bin/bash
# TODO: once your python prg wors remove this script

if [[ -z $1 ]]
then
   echo "Argument missing [ launch.sh <no_of_workers>  ]"
   exit 1
fi

##### Specific to this laptop
# TODO: ;-) remove this as specific to your machine
if [[ $1 -gt 2 ]] && [[ `hostname` == "MangoLap" ]]
then
  echo "SORRY, This Machine cannot handle more than 2 VMs"
  exit 1
fi
##############################

no_of_workers=$1
workers_ip_subnet_bytes="10.10.10"
workers_init_offset=4
spec_file="spec.yaml"

workers_final_offset=`echo "$workers_init_offset+$no_of_workers" | bc`

cat /dev/null > $spec_file

### Create Master Spec
echo "master:" >> $spec_file
echo "  - name: master" >> $spec_file
echo "    hostname: \"master\"" >> $spec_file
echo "    ipaddress: \"10.10.10.3\"" >> $spec_file

### Create Workers Specs
echo "worker:" >> $spec_file
for (( i="$workers_init_offset"; i<"$workers_final_offset"; i++ ))
do
  worker_num=`echo "$i-$workers_init_offset+1" | bc`
  echo "  - name: worker00$worker_num" >> $spec_file
  echo "    hostname: \"worker00$worker_num\"" >> $spec_file
  echo "    ipaddress: \"10.10.10.$i\"" >> $spec_file
done

### Initialize vagrant
#vagrant up
