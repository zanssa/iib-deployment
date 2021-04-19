#!/bin/bash

echo "Verify all arguments have been passed"
if [ $# -lt 4 ]
then
    echo "One or more of the required arguments is not passed"
else
    echo "host" $1
    echo "'$4'"
    awx --conf.host $1 \
        --conf.token $2 \
        --conf.username $3 \
        -k workflow_job_templates launch "$4" -f human
fi