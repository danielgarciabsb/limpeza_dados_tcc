#!/bin/bash

# USAGE: domultiple [command] [argument array]
function domultiple {
    typeset -n array=$2
    for m in $array; do eval $1 $m; done;
}

arr=$(ls *.csv);

domultiple "python ./inserir_dados_sql.py" "arr"
