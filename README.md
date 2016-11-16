# build-light

build-light.py
Python script to poll jenkins jobs status and change the color of the Philips hue light bulb depending on the status of the job. The script makes use of jenkins API and threading library to poll the jenkins containing multiple projects. Thus this script can scale very well.

config.yml
This is file contains the configurations for each project in jenkins, for instance jeknkins url, bulb id for that project. As we add more bulbs and project in the jenkins, this file needs to be updated with the respective configuration.

The script is deployed in AWS using Ansible (under template/ directory):
1. configure and launch an EC2 instance 
2. download the zip file including the build light project from the git repository
3. unzips the file and run the script
