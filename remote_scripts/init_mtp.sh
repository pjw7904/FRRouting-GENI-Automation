#!/bin/bash

# Refresh packages
sudo apt-get update

# TShark installation
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark

# Chrony installation and configuration
sudo apt-get -y install chrony
sudo sed -i '/^$/d; /#/d; s/pool/#pool/g; $ a\\n#MTP/FRR Research Time Server Information (questions? pjw7904@rit.edu)\nserver time.google.com iburst' /etc/chrony/chrony.conf
sudo invoke-rc.d chrony restart && sudo chronyc -a 'burst 4/4' && sudo chronyc -a makestep

# NOTE: For Leaf and Spine nodes, make sure to turn off IP forwarding at some point!