# -*- coding: utf-8 -*-
"""Copia de Assignment-Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19VQIGQehcNDZCK06GhAc1rkVWHU6vt5h
"""

!pip install kgtk==1.0.1

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
!apt-get install libcairo2-dev

"""## Preamble: set up the environment and files used in the assignment (remember to restart runtime)"""

import io
import os
import subprocess
import sys

import math
import numpy as np
import pandas as pd
from graph_tool.all import *
from IPython.display import display, HTML

from kgtk.configure_kgtk_notebooks import ConfigureKGTK
from kgtk.functions import kgtk, kypher

# Parameters

# Folder on local machine where to create the output and temporary folders
input_path = None
output_path = "/tmp/projects"
project_name = "assignment"

"""The following command will download all the files you  need for the assignment:"""

files = [
    "all",
    "label",
    "alias",
    "description",
    "external_id",
    "monolingualtext",
    "quantity",
    "string",
    "time",
    "item",
    "wikibase_property",
    "qualifiers",
    "datatypes",
    "p279",
    "p279star",
    "p31",
    "in_degree",
    "out_degree",
    "pagerank_directed",
    "pagerank_undirected"
]
ck = ConfigureKGTK(files)
ck.configure_kgtk(input_graph_path=input_path,
                  output_path=output_path,
                  project_name=project_name)

"""The KGTK setup command defines environment variables for all the files so that you can reuse the Jupyter notebook when you install it on your local machine."""

ck.print_env_variables()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# ck.load_files_into_cache()

"""# About this assignment.
This assignment is based on https://github.com/usc-isi-i2/kgtk-notebooks/tree/main/tutorial. If you have any questions or doubts, it is encouraged to look how the tutorial performs the different operations.

Additional information can be found in https://kgtk.readthedocs.io/

## Simple graph statistics

Let's calculate first some statistics about the KG. Count the number of instances:
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#    query -i all
#         --match '(instance)-[:P31]->(class)'
#         --return 'count(distinct instance) as count_instances'
# """)

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(instance)-[l {label: property}]->(class)'
#         --return 'count(distinct property) as count_property'
# """)

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#        --match '(instance)-[l {label: property}]->(class)'
#                 --return 'l.label, count(distinct instance) as frequency'
# """)

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
# TO DO 
# sparql.setQuery('''
  # SELECT ?actor ?movie ?actorLabel ?movieLabel WHERE {
   #?movie wdt:P161 wd:Q2685.
   #?movie wdt:P161 ?actor.
   #FILTER (?actor != wd:Q2685)
   #SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
# }
#''')
# results: https://query.wikidata.org/#%0A%20%20%20SELECT%20%3Factor%20%3Fmovie%20%3FactorLabel%20%3FmovieLabel%20WHERE%20%7B%0A%20%20%20%3Fmovie%20wdt%3AP161%20wd%3AQ2685.%0A%20%20%20%3Fmovie%20wdt%3AP161%20%3Factor.%0A%20%20%20FILTER%20%28%3Factor%20%21%3D%20wd%3AQ2685%29%0A%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%7D%0A%0A

# In Kypher:
kgtk("""
query -i all
     --match '(:Q2685)<-[:P161]-(movie)-[:P161]->(actor)'
        --where 'actor != "Q2685"'
        --return 'actor, movie'
    / add-labels

""")

# How many awards does Schwarzenegger have?

# SPARQL:
# TO DO
#sparql.setQuery('''
 #   SELECT (
 #   COUNT(?award) AS ?count_awards) 
 #   WHERE {    
 #   wd:Q2685 wdt:P166 ?award
 #   }
 #   ''')
 # results:https://query.wikidata.org/#%20%20%20SELECT%20%28%0A%20%20%20%20COUNT%28%3Faward%29%20AS%20%3Fcount_awards%29%20%0A%20%20%20%20WHERE%20%7B%20%20%20%20%0A%20%20%20%20wd%3AQ2685%20wdt%3AP166%20%3Faward%0A%20%20%20%20%7D

# Kypher:
kgtk("""
   query -i all 
     --match '(:Q2685)-[:P166]->(x)'
     
              
     --return 'count(x) as awards'
""")

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
# TO DO
#sparql.setQuery('''
#SELECT ?other ?party ?otherLabel ?partyLabel WHERE {
  # wd:Q2685 wdt:P102 ?party.
  # ?other wdt:P102 ?party.
  # ?other wdt:P31 wd:Q5.
  #SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
   #FILTER (?other != wd:Q2685)
 #}''')
 #results: 


# Kypher:
kgtk("""
   query -i all
    --match '(:Q2685)-[:P102]->(party)<-[:P102]-(other)-[:P31]->(:Q5)'
    --where 'other != "Q2685"'
    --return 'other, party'
    / add-labels
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
# TO DO
#sparql.setQuery('''
 #   SELECT DISTINCT ?property WHERE {
 #  ?class rdfs:subClassOf* wd:Q483501.
 #  ?element wdt:P106 ?class.
 #  ?element ?property ?p.
 #}''')
 #results: https://query.wikidata.org/#%20%20%20SELECT%20DISTINCT%20%3Fproperty%20WHERE%20%7B%0A%20%20%20%3Fclass%20rdfs%3AsubClassOf%2a%20wd%3AQ483501.%0A%20%20%20%3Felement%20wdt%3AP106%20%3Fclass.%0A%20%20%20%3Felement%20%3Fproperty%20%3Fp.%7D


# In Kypher:
kgtk("""
query -i all
        --match '()<-[l {label: property}]-(element)-[:P106]->(class)-[:P279star]->(:Q483501)'
        --return 'distinct property'
    / add-labels
""")

# And a film director?
# SPARQL: 
# TO DO
#sparql.setQuery('''
#  SELECT DISTINCT ?prop ?val
#  WHERE {
 #     wd:Q2526255 ?prop ?val .
 #     ?wdprop wikibase:directClaim ?prop .
  #    ?wdprop wdt:P31+ wd:Q107649491
  #}
#''')
#results: https://query.wikidata.org/#%20%20%20SELECT%20DISTINCT%20%3Fprop%20%3Fval%0A%20%20WHERE%20%7B%0A%20%20%20%20%20%20wd%3AQ2526255%20%3Fprop%20%3Fval%20.%0A%20%20%20%20%20%20%3Fwdprop%20wikibase%3AdirectClaim%20%3Fprop%20.%0A%20%20%20%20%20%20%3Fwdprop%20wdt%3AP31%2B%20wd%3AQ107649491%0A%20%20%7D

# In Kypher:
kgtk("""
query -i all
        --match '()<-[l {label: property}]-(element)-[:P106]->(class)-[:P279star]->(:Q2526255)'
        --return 'distinct property'
    / add-labels
""")

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
# TO DO
print("0. Arnold Schwarzenegger")
print("1. Hugh O\'Brian")
print("2. John Larroquette" )
print("3. Carl Reiner")
print("4. Harvey Fierstein")
print("5. Tom Sizemore ")
print("6 Randy Quaid ")
print("7. Gene Kelly")
print("8. DeForest Kelley")
print("9. Robert Stack")

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**

"""

#%%bash
#cat <<EOF >$TEMP/path-query.tsv
#node1	node2	label
#Q2685	Q22686	path

kgtk("""
    add-labels -i $TEMP/path-query.tsv
""")

# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)
# TO DO    
kgtk("""
add-labels -i $TEMP/path-query.tsv
   
""")

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)
# TO DO  
kgtk("""
 reachable-nodes -i all
        --root Q2685
        --props P40 P3373 P26 P22 P25
    / add-labels
        

""")

# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
# TO DO  
kgtk("""
 graph-statistics -i all -o /tmp/projects/assignment/metadata.pagerank.undirected.tsv.gz
    --compute-pagerank True
    --compute-hits False
    --page-rank-property P_pagerank
    --output-pagerank True
    --output-statistics-only
    --output-hits False 
    --undirected True
    --log-file /tmp/projects/assignment/metadata.pagerank.undirected.summary.txt
""")

# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
query -i item -i $OUT/metadata.pagerank.undirected.tsv.gz
        --match '
            item: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:Pdirected_pagerank]->(pagerank)'
        --return 'actor as node1, pagerank as node2'
        --order-by 'cast(pagerank, float) desc'
        --limit 10
    / add-labels
""")