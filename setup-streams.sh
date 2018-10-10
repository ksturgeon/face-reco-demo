#!/bin/bash

# Create Stream

hadoop fs -rm -f /demo-stream
maprcli stream create -path /demo-stream -produceperm p -consumeperm p -topicperm p

# Create topic(s)

maprcli stream topic create -path /demo-stream -topic topic1 -partitions 3

maprcli stream topic list -path /demo-stream -json
