#!/usr/bin/env python
from collections import defaultdict
import csv
import  networkx
import yaml
import json
import copy

def calculate_path(source, target, g, cutoff = 4):
    paths=networkx.all_simple_paths(g, source=source, target=target, cutoff=cutoff)
    path_list = list(paths)
    return path_list

def expand_path (source, source_ip, path_list, g):
    udp_port = 32768
    path_probing = {'head_end_rtr': source,
                    'ip_address' : source_ip,
                    'path':[]   }
    for path in path_list:
        print ("path", path)
        hops = {}
        hops={'name': "-".join(path),
            'udp_port': udp_port,
            'hops': [] }
        i=0
        udp_port = udp_port + 1
        while i < (len(path)-1):
            hops["hops"].append(g.edges[path[i],path[i+1]]['ip_info']['r_ip'])
            i=i+1
        path_probing['path'].append(hops)
    return path_probing

links= csv.DictReader(open('links.csv'))
nodes= csv.DictReader(open('nodes.csv'))

# changing object type for easy mainuplation
links_list = list(links)
nodes_list = list(nodes)

# adding node name in links_list
for link in links_list:
     for node in nodes_list:
             if link["id"] == node["id"]:
                     link["name"] = node["name"]
                     link["rtr_ip"] = node ["rtr_ip"]
             elif link["r_id"] == node["id"]:
                     link["r_name"] = node["name"]
                     link["r_rtr_ip"] = node ["rtr_ip"]


# links_list
print ("\n print list of links \n")
for link in links_list:
    print (link)

# initializing graph object
g = networkx.Graph()

# adding edges to graph
for link in links_list:
     # if a edge already exist skip it
     if g.has_edge(link['name'],link['r_name']):
             continue
     g.add_edge(link["name"], link["r_name"], ip_info={ 'ip':  link["ip"], 'r_ip': link["r_ip"] })

dict = { 'defaults': {'return_address': '20.0.0.2/32',
                    'src_pkt_address_range': '1.1.0.0/32'},
        'path_probing': []}

sources = ['r1']
target = 'r6'
cutoff = 4
#copy_graph1 = copy.deepcopy(g)
#copy_graph2 = copy.deepcopy(g)
for source in sources:
    for node in nodes_list:
        if source == node["name"]:
            source_ip = node["rtr_ip"]
    path_list=calculate_path (source , target , g , cutoff)    
    path_probing = expand_path (source, source_ip, path_list, g)
    dict['path_probing'].append(path_probing)


ff = open('meta.yaml', 'w+')
if dict:
    output_data = eval(json.dumps(dict)) 
    yaml.dump(output_data, ff, allow_unicode=True)
