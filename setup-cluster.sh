#! /bin/bash


# Create Volumes
maprcli volume create -name demo-tables -path /demo-tables -readAce 'p' -writeAce 'p'
maprcli volume create -name demo-streams -path /demo-streams -readAce 'p' -writeAce 'p'
maprcli volume create -name demo-files -path /demo-files -readAce 'p' -writeAce 'p'

# Create Tables - expecting CDC since we need to be notified of a new image
maprcli table create -path /demo-tables/raw-images -tabletype json

# Create Streams - CDC and processed data
maprcli stream create -path /demo-streams/dbchanges -produceperm p -consumeperm p -topicperm p -ischangelog true
maprcli stream topic create -path /demo-streams/dbchanges -topic topic1 -partitions 3

maprcli stream create -path /demo-streams/processed-images -produceperm p -consumeperm p -topicperm p
maprcli stream topic create -path /demo-streams/processed-images -topic topic1 -partitions 3

# Set up table change propagation
maprcli table changelog add -path /demo-tables/raw-images -changelog /demo-streams/dbchanges:topic1 -useexistingtopic true
