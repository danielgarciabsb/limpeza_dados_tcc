#!/bin/bash

# USAGE: domultiple [command] [argument array]
function domultiple {
    typeset -n array=$2
    for m in $array; do eval $1 $m; done;
}

arr=$(ls *.csv);

domultiple "python ./arquivo_csv.py" "arr"
