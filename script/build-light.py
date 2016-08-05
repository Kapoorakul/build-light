import yaml
import json
import sys
import urllib2
import ssl
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from jenkinsapi.jenkins import Jenkins
import threading

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_endpoint = 'http://10.120.18.175/api/'
bridge_user = 'bgl3VFxsl9rQcJbFZ7iqX4kdCULQlpnhIGrRtAnB'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def check_jobs(job_list,URL):

# return a list of enabled build jobs
        joblist = []
        for jobName in job_list:
            try:
                jenkinsStream   = urllib2.urlopen( URL + 'job/' + jobName + "/api/json", context=ctx )
                buildStatusJson = json.load( jenkinsStream )
            except urllib2.HTTPError, e:
                continue

            if buildStatusJson.has_key( "buildable" ):
               status=buildStatusJson["buildable"]
               str_status=str(status)
               if str_status == "True":
                  joblist.append(jobName)
               else:
                  pass
        return joblist


def check_build(URL,Light):

# initialize the build-lights 
    requests.put(api_endpoint + bridge_user + '/lights/' + Light +'/state',data=json.dumps({ "hue":46920 }))

# check the lastBuild status of the enabled build jobs
    while True:
      job_list = jenkins_jobs(URL)
      joblist = check_jobs(job_list,URL)
      FLAG = 0
      for jobName in joblist:
          try:
             jenkinsStream   = urllib2.urlopen( URL + 'job/' + jobName + "/lastBuild/api/json", context=ctx )
             buildStatusJson = json.load( jenkinsStream )
          except urllib2.HTTPError, e:
             continue
# Set the flag if the buildStatus is not Success
          if buildStatusJson.has_key( "result" ):
             status=buildStatusJson["result"]
             print("[{}] build status: {}".format(jobName,status))
             if buildStatusJson["result"] != "SUCCESS" :
                FLAG=1
             else:
                pass
# Set the build light color to red if the Flag is set
      if FLAG==0:
         print('*********************ALL JOBS PASSED***********************************')
         requests.put(api_endpoint + bridge_user + '/lights/' + Light +'/state',data=json.dumps({ "hue":46920 }))
      else:
         requests.put(api_endpoint + bridge_user + '/lights/' + Light +'/state',data=json.dumps({ "hue":0 }))

# sleep for 300 seconds
      time.sleep(300)

def jenkins_jobs(jenkins_url):

# connect to the Jenkins, and return a list of builds
    jenkins_conn = Jenkins(jenkins_url,ssl_verify=False)
    return jenkins_conn.keys()


def main():

# read config file
    with open('config.yml','r') as f:
         config = yaml.load(f)

# iterate over each team, check if the bulb is connected, if True then check the build
    for key in config.keys():
        if config[key]['Connected'] == True:
           check_build_thread = threading.Thread(target=check_build, args=(config[key]['URL'],str(config[key]['Light'])))
           check_build_thread.start()

if __name__ == "__main__":
   main()

