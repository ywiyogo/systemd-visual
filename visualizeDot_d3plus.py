#!/usr/bin/env python

"""
Visualizing the systemd dependency and execution using D3plus

Author: Yongkie Wiyogo
date: 2016-10-14
"""

import sys
import os,re

# This script needs an argument which is a dot file that is generated
# by systemd-analyze dot
script, filename  = sys.argv

#setNodes to avoid duplicate node
setNodes=set()
#ldNodes=[{"name": "alpha", "size": 10}]
#ldConnections = [{"source": "alpha", "target": "beta"}]
# adding: ldNodes.append({'a':'b','c':12}) or ldNodes = ldNodes + [{'a':'b','c':12}]
# access connections[0]['source']
ldNodes=[]
ldConnections=[]


#create regex to detect the source and target in a line
#e.g.:"multi-user.target"->"Early.target" [color="grey66"];
dotRegex = re.compile(r'''(
    \"(.*\.[a-z]+)\"       # source group(2)
    ->
    \"(.*\.[a-z]+)\"\s*       # target group(3)
    \[color=\"(.*)\"\];    # connection type group(4)
    )''', re.VERBOSE)

# Read dot content line-by-line
with open(filename) as content:
   for line in content:
      if not "->\"systemd-journald.socket\"" in line :   #ignore systemd-journald.socket
         if "shutdown.target" in line or "color=\"red\"" in line:      #ignore shutdown.target
            continue
         else:
            objResult = dotRegex.search(line)

            if objResult:
               srcNode= objResult.group(2)
               trgNode=objResult.group(3)
               color= objResult.group(4)
               if "grey" in color:  # only takes "Wants" connections
                setNodes.add(srcNode)
                setNodes.add(trgNode)
                ldConnections.append({"source": srcNode, "target": trgNode})

for node in setNodes:
   size= 5
   if 'target' in node:
      size = 20
   ldNodes.append({"name": node, "size": size})

#Read the template
htmlContent=""
with open("d3plus_network_template.html", "r") as templFile:
   htmlContent= templFile.read()

# Substitute the template content
htmlContent = re.sub(r'var nodes = (.*)', "var nodes = "+str(ldNodes), htmlContent)
htmlContent = re.sub(r'var connections = (.*)', "var connections = "+str(ldConnections), htmlContent)
print(htmlContent)
# Write in on another file
with open("d3plus_network.html", "w") as templFile:
   templFile.write(htmlContent)


