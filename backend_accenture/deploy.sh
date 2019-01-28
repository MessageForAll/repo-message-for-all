#!/bin/bash
cd pav-oi
git pull origin master
docker-compose down
docker-compose up -d