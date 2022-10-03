from xml.dom import minidom
import ipaddress
from GENIutils import uploadToGENINode, getConfigInfo, buildDictonary, orchestrateRemoteCommands
from collections import defaultdict

rspec = getConfigInfo("Local Utilities", "RSPEC")
xmlInfo = minidom.parse(rspec)

GENIInfo = {}
addressingInfo = defaultdict(list) # [('node-x', a.b.c.d), ('node-y', e.f.g.h)]

node_lst = xmlInfo.getElementsByTagName('node')

for node in node_lst:
    print("NODE:")
    nodeName = node.attributes['client_id'].value
    print(nodeName)

    print("LOGIN INFO:")
    login_info = node.getElementsByTagName("login") # login is the tag name
    for elem in login_info:
        hostname = (elem.attributes["hostname"]).value
        port = (elem.attributes["port"]).value
        print(hostname)
        print(port)

    GENIInfo[nodeName] = (hostname, port, {})

    print("IP ADDRESSING INFO:")
    addr_info = node.getElementsByTagName("ip")
    for elem in addr_info:
        ipv4addr = (elem.attributes["address"]).value
        mask = (elem.attributes["netmask"]).value
        print(ipv4addr)
        print(mask)
        fulladdr = "{}/{}".format(ipv4addr, mask)
        networkAddress = ipaddress.ip_network(fulladdr, strict=False)
       
        addressingInfo[networkAddress].append((nodeName, ipv4addr))

for entry in GENIInfo.values():
    print(entry)

for subnet in addressingInfo.items():
    print(subnet[1])
    for entry in subnet[1]:
        currentNode = entry[0]
        currentAddr = entry[1]
        for otherEntry in subnet[1]:
            if(otherEntry[0] != currentNode):
                newInfo = {"remoteIPAddr": otherEntry[1], "localIPAddr": currentAddr, "subnet": subnet[0]}
                GENIInfo[currentNode][2][otherEntry[0]] = newInfo


print("\n\n\n")
for thing in GENIInfo.items():
    print("node name: {}".format(thing[0]))
    print("hostname: {}".format(thing[1][0]))
    print("port: {}".format(thing[1][1]))
    print("neighbors: {}".format(thing[1][2]))