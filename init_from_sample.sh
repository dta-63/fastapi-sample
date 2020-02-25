#!/bin/bash

read -p "Project name (snack case): "  name
read -p "Project full name: "  fullname
read -p "Project description: "  description
read -p "Repository path: "  remote

cd ..
git clone https://github.com/david-talabard/fastapi-sample.git $name
cd $name
git remote set-url origin $remote
./make.sh
mv .env-sample .env
echo "env file configure .env"
sed -i "s/SERVICE_NAME/$fullname/g" main.py
sed -i "s/SERVICE_DESCRIPTION/$description/g" main.py
