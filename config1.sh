#! /bin/bash

echo ""
read -p "Enter the name of the conda environment to create (will try to delete already existing ones) " envname
echo ""
echo "name of new conda environment: $envname"
echo ""

#delete old
#this does not work properly on Fedora <= V42
conda remove -n "$envname" --all

#create env
conda create -n "$envname"


