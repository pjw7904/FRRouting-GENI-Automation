# Turn on BGP, but it is not active yet
sudo sed -i 's/bgpd=no/bgpd=yes/g' /etc/frr/daemons

# Reload FRR, which also turns on previously turned-off protocols (in our case BGP)
sudo service frr reload

