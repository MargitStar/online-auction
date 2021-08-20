#!/bin/sh

amazon_key=../AmazoniTechArt.pem

cd devops || exit

chmod 600 ../AmazoniTechArt.pem
chmod 0775 ..
cd ~/.casher && tar -xvzf backend_auction-fetch.tgz
cd ~/build/andreybulygin-ita/margarita-b-online-auction-be/devops
ls 
pwd
export $(grep -v '^#' .env | xargs)

ansible-playbook -i hosts deploy_app.yml --private-key "$amazon_key" -b