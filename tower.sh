#!/bin/bash

echo "Verify all arguments have been passed"
if [ $# -lt 4 ]
then
    echo "One or more of the required arguments is not passed"
else
    awx --conf.host "$TOWER_HOST" \
        --conf.token "$TOWER_OAUTH" \
        --conf.username "$TOWER_USER" \
        -k job_templates launch "$TOWER_JOB" --monitor -f human
fi