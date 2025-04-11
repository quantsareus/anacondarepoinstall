#! /bin/bash


# Activate env qdev
conda activate qdev

# add conda-forge and set it as preferred one; comment out if you want preferably to install from channel base 
conda config --add channels conda-forge

# Update conda
conda update conda
# conda update -n base -c conda-forge conda

# Install subprocess
conda install conda_subprocess



