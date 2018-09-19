#!/bin/sh

for a in 1 2 3 4
do
   echo $a
   `nosetests test$a.py`
done
