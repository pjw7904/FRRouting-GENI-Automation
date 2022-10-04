# Get the FRR Repository added to the node.
curl -s https://deb.frrouting.org/frr/keys.asc | sudo apt-key add -
FRRVER="frr-stable"
echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) $FRRVER | sudo tee -a /etc/apt/sources.list.d/frr.list

# Install whatever the stable version of FRR is as a package from that repository.
sudo apt-get update && sudo apt-get -y install frr frr-pythontools

# Give permissions to user to access frr files (this requires a logout after to take effect)
sudo usermod -a -G frr,frrvty $(logname)

# Install tshark for packet-level inspections
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark

# Remove static routes from the nodes so it does not mess with routing protocol updates

## Place result of the ip route command in a variable
tableOutput=$(ip route)

## Change Internal Field Seperator to be a newline
IFS='
'

## Loop through each route entry, look for the static routes GENI added and deleting them
for entry in $tableOutput
do
	if [[ $entry == *"via 10."* ]]; then
		echo "$entry" >> ~/removed_static_routes.log
		prefix=$(echo "$entry" | cut -d" " -f1)
		echo "$prefix" >> ~/removed_static_routes.log
		sudo ip route delete $prefix
	fi
done