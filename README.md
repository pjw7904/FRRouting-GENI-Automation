# GENI Automation
A collection of scripts to help in the installation, configuration, and testing of experiments on the GENI testbed, including those that utilize the FRR routing protocol suite. This assumes that the image installed on the GENI nodes is Ubuntu/Debian-based. Currently, only scripts and configurations to help with FRR EBGP (traditional, not data center) are included as a base to show how this collection of scripts can be used.

## Directories
1. local_scripts = scripts that are run on your local machine and reach out to the remote GENI nodes via SSH (Paramiko library).

2. remote_scripts = scripts that are uploaded and run on the remote node directly. No SSH connection is required once the script has been uploaded (with a script from local_scripts). GNU Screen or another command is used to push the script to the background.

## Setting up your Environment for GENI
1. **Reserve resources on a GENI slice, or utilize an existing one if desired.**
   1. Utilize a prefix naming structure to label a node as a client node or a forwarding/switch node. For example, a forwarding node might be in the form node-x, where x is the forwarding node number, and a client node might be in the form client-x, where x is the client node number. It is important to do this so that the automation scripts can handle each type of node appropriately.
   2. The topology itself does not matter, arraign it however you would like.
2. **Once the resources are ready to be used, download the Manfest RSPEC.**
   1. On the GENI slice page, click on the Details button at the bottom of the manage resources box.
   2. Once the resources have been refreshed and the status is noted as READY, scroll to the bottom of the screen and find the text "Show Raw XML Resource Specification (Manifest)."
   3. Click on that text, it will expand the window and show you the XML-compliant RSPEC file. Copy the contents of this file and save it somewhere on your local machine. It does not have to be in this directory.
3. **Populate the credentials file**
   1. Inside of the local_scripts directory, there should be a file named creds_sample.cnf. Populate the configuration options with your desired setup. Note the "Credentials File Breakdown" section for help understanding each option. If you run into an error while running a script, this should be the first place to check.
   2. Based on your prefix choices from step 1.1, make sure the prefixes are added as they are written. For example, if you went with node-x as a prefix, the input to that configuration would be "node-".
   3. When you're set, rename creds_sample.cnf to creds.cnf. It will not work otherwise.
4. **Install Python package requirements**
   1. Find the requirements.txt file in the directory.
   2. Note if you have the package(s) installed. If not, install them. Over time, this may change, so make sure to look for any updates to that file in future pulls or downloads.

## Credentials File Breakdown
* SwitchName: Prefix for forwarding nodes (ex: node-)
* endNodeName: Prefix for client nodes (ex: client-)
* remoteCodeDirectory: Default directory on remote GENI machines
* username: Your GENI username
* password: Your GENI password
* OSVersion: The version of Ubuntu you're running (ex: 18.04)
* RSPEC: Path to the manifest RSPEC you are workin on           
* privateKey: Path to the private key you use to connect to GENI nodes
* localWorkingDirectory: Path to this directory
* scriptLocation: Path to a script you wish to run on a remote GENI node
* scriptType: The type of script at scriptLocation (ex: bash, python)
* runOnAllNodes: Run your script/command/etc on all GENI nodes in the slice (True/False)
* runOnNodes: firstNodeName,secondNodeName, prefixOfName (comma-deliminated list of nodes to run a script/command). For example to get node-1 and all nodes that start with 's', you would enter: node-1, s
* routesToRedistribute: Type of route BGP needs to redistribute (ex: connected, ospf)

If runOnAllNodes is set to True, runOnNodes is not checked. If it is set to False, runOnNodes is checked for the node list.

Beyond what is presented here, you can take advantage of this system and add your own custom configuration options. Make sure to rename creds_sample.cnf to creds.cnf when you are all set.

## Getting the FRR BGP Implementation Running on GENI
1. **Update the creds file with BGP-appropriate settings**
   1. If you aren't running any other routing protocol, routesToRedistribute should be connected.
   2. If there are clients in your topology, make sure that runOnSwitches is set to True and runOnAllNodes is set to False. If there are no clients, set runOnAllNodes to True.
   3. Set scriptLocation to remote_scripts/install_frr.sh and scriptType to bash.
2. **Install FRR, remove existing static routes, and update user permissions**
   1. On a terminal, run the GENIScriptsExec.py script. If the creds.cnf file was updated correctly, this will upload the install_frr.sh script and run it in a GNU Screen (in the background) on each forwarding node. TShark will also be installed.
   2. Give this time to work, I would let it run for 15-30 minutes just in case. If you know how to get into a GNU Screen and look at the progress, you can do so as well.
3. **Activate BGP**
   1. Update creds.cnf to point to the script remote_scripts/turn_on_bgp.sh
   2. Run GENIScriptsExec.py again.
   3. At this point, BGP should be activated and ready to go. A good way to check if this is the case is by manually going into one of the nodes and running the command ```ps -aux | grep /usr/lib/frr```. The result of this command should look something like the following:

    ```console
    pjw7904@node-3:~$ ps -aux | grep /usr/lib/frr
    frr      21811  0.0  0.9 424588  9624 ?        S<sl Oct04   0:14 /usr/lib/frr/zebra -d -F traditional -A 127.0.0.1 -s 90000000
    frr      21816  0.0  0.4  42716  4900 ?        S<s  Oct04   0:10 /usr/lib/frr/staticd -d -F traditional -A 127.0.0.1
    root     27274  0.0  0.3  39492  3120 ?        S<s  Oct05   0:13 /usr/lib/frr/watchfrr -d -F traditional zebra bgpd staticd
    frr      27283  0.0  1.5 215620 15920 ?        S<sl Oct05   0:05 /usr/lib/frr/bgpd -d -F traditional -A 127.0.0.1
    ```

    If you do not see bgpd in the output, BGP was not successfully activated. If you do not see zebra, staticd, and watchfrr, FRR was not installed correctly. A good way to check to see if there were issues is by going into the GNU screens where the scripts were run. The name of a screen is the name of a script, so you should have two active, disconnected screens named install_frr.sh and turn_on_bgp.sh to look into. Getting in and out of a GNU Screen is not discussed here.

4. **Configure BGP**
   1. Run local_scripts/FrrBgpConfig.py
   2. Each node running BGP will be given a custom script file to configure, among other things, an ASN and neighbor information.
   3. After a minute or so, not only should each node be configured with BGP, but the topology should be converged. A good way to check the former is with the command ```sudo vtysh -c "show run"``` and the latter with the command ```sudo vtysh -c "show ip route"```. The output on each node will be different, but you should see something like:

    ```console
    pjw7904@node-3:~$ sudo vtysh -c "show run"
    Building configuration...

    Current configuration:
    !
    frr version 8.3.1
    frr defaults traditional
    hostname node-3.frr-bgp-automated.ch-geni-net.instageni.nysernet.org
    log syslog informational
    service integrated-vtysh-config
    !
    router bgp 64515
    neighbor GENI_NEIGHBORS peer-group
    neighbor 10.10.5.1 remote-as 64514
    neighbor 10.10.5.1 peer-group GENI_NEIGHBORS
    neighbor 10.10.6.1 remote-as 64517
    neighbor 10.10.6.1 peer-group GENI_NEIGHBORS
    neighbor 10.10.10.2 remote-as 64516
    neighbor 10.10.10.2 peer-group GENI_NEIGHBORS
    !
    address-family ipv4 unicast
    redistribute connected
    neighbor GENI_NEIGHBORS route-map GENI_MAP in
    neighbor GENI_NEIGHBORS route-map GENI_MAP out
    exit-address-family
    exit
    !
    ip prefix-list GENI_LIST seq 5 deny 172.16.0.0/12
    ip prefix-list GENI_LIST seq 10 permit any
    !
    route-map GENI_MAP permit 10
    match ip address prefix-list GENI_LIST
    exit
    !
    end
    ```

    ```console
    pjw7904@node-3:~$ sudo vtysh -c "show ip route"
    Codes: K - kernel route, C - connected, S - static, R - RIP,
        O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
        T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
        f - OpenFabric,
        > - selected route, * - FIB route, q - queued, r - rejected, b - backup
        t - trapped, o - offload failure

    K>* 0.0.0.0/0 [0/1024] via 172.16.0.1, eth0, src 172.17.1.20, 1d22h29m
    B>* 10.10.1.0/24 [20/0] via 10.10.5.1, eth3, weight 1, 13:29:08
    B>* 10.10.2.0/24 [20/0] via 10.10.5.1, eth3, weight 1, 13:29:08
    B>* 10.10.3.0/24 [20/0] via 10.10.5.1, eth3, weight 1, 13:29:08
    B>* 10.10.4.0/24 [20/0] via 10.10.5.1, eth3, weight 1, 13:29:08
    C>* 10.10.5.0/24 is directly connected, eth3, 1d22h29m
    C>* 10.10.6.0/24 is directly connected, eth2, 1d22h29m
    B>* 10.10.7.0/24 [20/0] via 10.10.10.2, eth1, weight 1, 13:29:05
    B>* 10.10.8.0/24 [20/0] via 10.10.6.1, eth2, weight 1, 13:29:02
    B>* 10.10.9.0/24 [20/0] via 10.10.5.1, eth3, weight 1, 13:29:08
    C>* 10.10.10.0/24 is directly connected, eth1, 1d22h29m
    C>* 172.16.0.0/12 is directly connected, eth0, 1d22h29m
    K>* 172.16.0.1/32 [0/1024] is directly connected, eth0, 1d22h29m
    ```