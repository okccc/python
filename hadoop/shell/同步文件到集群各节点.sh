#!/usr/bin/env bash

file_path=$1

echo "Begin! file_path is: $file_path"

if [ ! -f ${file_path} ] ; then
    echo "Failed! file_path does not exist"
    exit 1
fi

hosts=(cdh25 cdh26 cdh27 cdh28 cdh29 cdh30 cdh31 cdh32 cdh33)

for host in ${hosts[*]}
do
    scp ${file_path} ${host}:${file_path}

	if [ $? -eq 0 ] ; then
			echo "Sync success; Target host is: $host."
	else
			echo "Sync failed; Target host is: $host."
			exit 1
	fi
done