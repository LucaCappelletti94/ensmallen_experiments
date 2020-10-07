#!/bin/bash

GRAPHS=$(run.py graphs_list)
LIBRARIES=('ensmallen' 'networx' 'csrgraph')

for G in GRAPHS; do
    for L in LIBRARIES; do
        (python run.py $G $L $T)
    done
done