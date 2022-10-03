# Remove potential log file that was already there if this is being rerun
rm -f ~/removed_static_routes.log

# Place result of the ip route command in a variable
tableOutput=$(ip route)

# Change Internal Field Seperator to be a newline
IFS='
'

# Loop through each route entry, look for the static routes GENI added
for entry in $tableOutput
do
	if [[ $entry == *"via 10."* ]]; then
		echo "$entry" >> ~/removed_static_routes.log
		prefix=$(echo "$entry" | cut -d" " -f1)
		echo "$prefix" >> ~/removed_static_routes.log
		sudo ip route delete $prefix
	fi
done