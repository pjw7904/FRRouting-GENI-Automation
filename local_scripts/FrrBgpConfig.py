from GENIutils import getConfigInfo, buildDictonary, orchestrateRemoteCommands
from GENIScriptExec import executeScriptOnNode
import os

PRIVATE_ASN_RANGE_START = 64512
ADD_CONFIG = "-c {}"

def main():
    # Grabbing configuration info from GENI config file
    rspec = getConfigInfo("Local Utilities", "RSPEC")
    routeType = getConfigInfo("BGP Traditional", "routesToRedistribute")
    scriptType = getConfigInfo("Local Utilities", "scriptType")
    scriptDestination = getConfigInfo("GENI Credentials", "remoteCodeDirectory")

    # Build a dictonary of GENI node information based on user-defined filters
    GENIDict = buildDictonary(rspec)

    # Give every node in the dictonary a private Autonomous System Number (ASN)
    ASNValues = {}
    modifier = 0
    for node in sorted(GENIDict):
        ASNValues[node] = PRIVATE_ASN_RANGE_START + modifier
        modifier += 1
 
    # Necessary commands for a minimal BGP configuration
    configModeConfig = "conf t"
    enterBGPConfig = "router bgp {ASN}"
    peerGroupConfig = "neighbor GENI_NEIGHBORS peer-group"
    neighborConfig = "neighbor {neighborIP} remote-as {neighborASN}"
    neighborPeerGroupConfig = "neighbor {neighborIP} peer-group GENI_NEIGHBORS"
    addressFamilyConfig = "address-family ipv4 unicast"
    redistributionConfig = "redistribute {routeType}".format(routeType=routeType)
    applyRouteMapInConfig = "neighbor GENI_NEIGHBORS route-map GENI_MAP in"
    applyRouteMapOutConfig = "neighbor GENI_NEIGHBORS route-map GENI_MAP out"

    # Necessary list-matching commands
    prefixListConfig = ["ip prefix-list GENI_LIST seq 5 deny 172.16.0.0/12", "ip prefix-list GENI_LIST seq 10 permit any"]
    routeMapDefConfig = "route-map GENI_MAP permit 10"
    routeMapRuleConfig = "match ip address prefix-list GENI_LIST"

    for node in sorted(GENIDict):
        enterBGPConfig = "router bgp {ASN}".format(ASN=ASNValues[node])

        with open('{}_bgp.sh'.format(node), 'w') as configFile:
            # 1. Create the prefix-list
            for config in prefixListConfig:
                configFile.write(createVtyshCommand([configModeConfig, config], isList=True))

            # 2. Create the route map, point it towards the prefix-list
            configFile.write(createVtyshCommand([configModeConfig, routeMapDefConfig], isList=True))
            configFile.write(createVtyshCommand([configModeConfig, routeMapDefConfig, routeMapRuleConfig], isList=True))

            # 3. Define the router's ASN
            configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig], isList=True))

            # 4. Create a peer group for all potential neighbors to share configurations
            configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, peerGroupConfig], isList=True))

            # 5. Define who the node's neighbors are, their IP address on the shared network with the current node, and their ASN
            neighborDict = GENIDict[node][2]
            for neighbor in neighborDict:
                neighborIP = neighborDict[neighbor]["remoteIPAddr"]
                neighborASN = ASNValues[neighbor]

                configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, neighborConfig.format(neighborIP=neighborIP, neighborASN=neighborASN)], isList=True))
                configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, neighborPeerGroupConfig.format(neighborIP=neighborIP)], isList=True))

            # 6. Apply the route map to the peer group to accept routes and allow routes out
            configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, addressFamilyConfig, applyRouteMapInConfig], isList=True))
            configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, addressFamilyConfig, applyRouteMapOutConfig], isList=True))

            # 7. Define the type of route to redistribute based on user configuration
            configFile.write(createVtyshCommand([configModeConfig, enterBGPConfig, addressFamilyConfig, redistributionConfig], isList=True))

        # Upload config file and execute FRR commands
        executeScriptOnNode(node, GENIDict, '{}_bgp.sh'.format(node), scriptType, scriptDestination)

        # Remove the file created for the node now that it has been uploaded
        os.remove('{}_bgp.sh'.format(node)) 

    return

def createVtyshCommand(configs, isList=False):
    command = "sudo vtysh"
    addCommand = ' -c "{}"'

    if(isList):
        for config in configs:
            command += addCommand.format(config)
    else:
        command += addCommand.format(configs)

    command += "\n"

    return command

if __name__ == "__main__":
    main() # run main