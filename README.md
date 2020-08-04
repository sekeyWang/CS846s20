# CS846s20

This project is to analyse how Java developers who use maven as their version control update their dependencies.

Environment: Python3

Packages: gitpython, pandas, numpy, matplotlob

##Code

find_repo.py: use github API to obtain targeting project url.

parser.py, parser2019.py: clone repositories from github, mine the maven file, save to project_dependency.csv

maven.py: Module that provides functions for analyzing Maven dependencies across one or more pom.xml files.

analysis.py: Script to analyse on the result file and plot figures.

##File

LU_metricsLMP.csv, Projects.csv, Projects2019.csv: all dependencies and repositories

project_dependency.csv, project_dependency2019.csv: generated dependency-repo pairs
