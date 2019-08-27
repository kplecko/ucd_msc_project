# Abracadata IBM cloud deployment application

import subprocess
import os
import time
import argparse
import threading


def executeCommand(command):
    """
    Execute linux command
    """
    print('Executing: ' + command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    print(output)
    print('Return code: ', p.returncode)
    if p.returncode > 0:
        print(f'Error executing command: {command} ')
        return False
    print('Command successful.')
    return True


def deploy_app(threadName, command):
    """
    Deploy application
    """
    print(f'Thread name: {threadName}')
    executeCommand(command)


class myThread (threading.Thread):
    """
    Thread class
    """
    def __init__(self, thread_Name, command):
        threading.Thread.__init__(self)
        self.thread_Name = thread_Name
        self.command = command

    def run(self):
        # print("Starting " + self.thread_Name)
        deploy_app(self.thread_Name, self.command)
        print("Exiting " + self.thread_Name)


def main():
    # get input parameters
    parser = argparse.ArgumentParser(description='IBM Cloud application deployment')
    parser.add_argument('-apiKey', type=str, help='#Cloud API Key', required=False)
    args, unknown_args = parser.parse_known_args()
    apiKey = args.apiKey

    apiKey = "xxxxxxxxxxxxxx"

    # get application path
    application_path = os.path.dirname(os.path.abspath(__file__))

    # IBM Cloud login command
    login_command = f'curl -fsSL https://clis.cloud.ibm.com/install/linux | sh; ibmcloud api https://api.eu-gb.bluemix.net; ibmcloud login --apikey "{apiKey}" -o xxxxxxxxx -s dev'

    # set deployment commands for all apps
    deploy_analyticsAI = f'cd {application_path}/analyticsAI; ibmcloud app push -k 2GB'
    deploy_youtubeData = f'cd {application_path}/youtubeData; ibmcloud app push'
    deploy_eventsAPI = f'cd {application_path}/eventsAPI; ibmcloud app push'
    deploy_yousights_fe = f'cd {application_path}/yousights-fe; ibmcloud app push'

    # Create new threads
    start = time.time()
    executeCommand(login_command)
    thread1 = myThread("Deploy FrontEnd", deploy_yousights_fe)
    thread2 = myThread("Deploy Events", deploy_eventsAPI)
    thread3 = myThread("Deploy YoutubeData", deploy_youtubeData)
    thread4 = myThread("Deploy AnalyticsAI", deploy_analyticsAI)

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    print("Exiting Main Thread")
    end = time.time()
    total_time = round((end - start), 2)
    print(f'Execution time: {total_time} seconds')


merge_request = os.environ.get('MERGE_PULL_REQUEST')
print(f'merge_request: {merge_request}')
if merge_request:
    main()
