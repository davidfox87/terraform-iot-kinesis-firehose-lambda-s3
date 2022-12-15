#!/bin/bash

aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 880572800141.dkr.ecr.us-west-1.amazonaws.com

[ $? -eq 0 ] && docker build -t kinesis-lambda .
[ $? -eq 0 ] && docker tag kinesis-lambda:latest 880572800141.dkr.ecr.us-west-1.amazonaws.com/kinesis-lambda:latest
[ $? -eq 0 ] && docker push 880572800141.dkr.ecr.us-west-1.amazonaws.com/kinesis-lambda:latest




