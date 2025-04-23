#! /bin/bash


#activate env
conda activate "$envname"

#add channel and make it the first one 
conda config --add channels defaults

#install uptodate python
conda install python

#install subprocess
conda install conda_subprocess




