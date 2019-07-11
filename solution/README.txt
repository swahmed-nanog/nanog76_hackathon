################################
# NANOG 76 HACKATHON 
# ACTIVE MONITORING
# Sponsored by ORACLE and TESUTO
# Presented by Syed W Ahmed and Deepak Padliya
# Date : 6/9/2019
################################
Disclaimer: This Hackathon Project was meant to be a POC and not coded for production use. It is coded as to get task completed rather using efficient methods. 
###########################
#Step 1a: 
#Get topology Information from router
###########################
* Router R1 and R6 had already BGP - LS configured. 
* exabgp_config.conf has exabgp config for host dev1. 
* parser.py makes sure route updates we receive are properly formatted in json and saves it in routes.txt file

###########################
#Step 1b:
#parse routes.txt to get nodes and link information
###########################
* once you have routes.txt you can use jq scripts to extract link and nodes info. 
* jqNodes.sh extract node information and output is in csv format. (check nodes.csv for sample output)
* jqLinks.sh extract link information and output is in csv format. (check links.csv for sample output)
Usage:
> ./jqNodes.sh # expects a json file routes.txt in same directory and output is in csv format
> ./jqLinks.sh # expects a json file routes.txt in same directory and output is in csv format

###########################
#Step 2:
#calculate possible best paths between endpoints
###########################
* consumes information in nodes.csv and links.csv to build a graph and extract all possible best path. 
* saves information in meta.yaml file for all paths and next hop to construct probe packet
Usage:
> ./all_paths.py # expects nodes.csv and links.csv files in same folder

###########################
#Step 3:
# Generate Probe packets and probe all possible paths
###########################
* Consume information in meta.yaml to create probe packets
* Send and receive packets and use information in payload to calculate RTT and account for any packet loss. 
* Expect scapy library installed in python
* Expect dev1 host conencted to topology to send and receive packets. 
Usage:
> ./prober.py  # expect meta.yaml in same folder and topology to send probe packet
