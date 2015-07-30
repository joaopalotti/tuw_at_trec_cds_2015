# tuw_at_trec_cds_2015

This repository contains all the required files to reproduce the submissions made by TUW for TREC-CDS 2015.

Explanations:
=============


processTopics.py:
-----------------
This file takes as input the original topic file (first parameter) from TREC and generates a topic file to be used by Terrier (second parameter).
There are multiple configurations that must be set in the code itself.

Usage example: 
-------------
$python processTopic.py ../topics2015B.xml 2015B_summary_noexpansion_1_1_1.gz







