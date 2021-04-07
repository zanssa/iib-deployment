#!/bin/bash

echo "Verify all arguments have been passed"
if [ $# -lt 4 ]
then
    echo "One or more of the required arguments is not passed"
else
    awx --conf.host "$tower_host" \
        --conf.token "$tower_oauth" \
        --conf.username "$tower_user" \
        -k job_templates launch "$tower_job" --monitor -f human
fi