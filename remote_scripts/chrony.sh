#!/bin/bash

sudo apt-get update
sudo apt-get -y install chrony
sudo sed -i '/^$/d; /#/d; s/pool/#pool/g; $ a\\n#MTP/FRR Research Time Server Information (questions? pjw7904@rit.edu)\nserver time.google.com iburst' /etc/chrony/chrony.conf
sudo invoke-rc.d chrony restart && sudo chronyc -a 'burst 4/4' && sudo chronyc -a makestep