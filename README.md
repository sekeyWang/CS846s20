# CS846s20

This project is to analyse how Java developers who use maven as their version control update their dependencies.

Environment: Python3
Packages: gitpython, pandas, numpy, matplotlob

parser.py: clone repositories from github, mine the maven file, save to project_dependency.csv
maven.py: Module that provides functions for analyzing Maven dependencies across one or more pom.xml files.
analysis.py: Script to analyse on the result file and plot figures.
