
import os
import json
import logging
import subprocess
import requests as r

from Server_standalone import app
from datetime import datetime
from gevent.wsgi import WSGIServer


time = str(datetime.now())[:19]
# list of strings representing the command
args = ['/home/pi/ngrok', 'http', '5001']
logging.basicConfig(filename='run.log', level=logging.INFO)
logging.info(time+' Ngrok Start')
try:
    # stdout = subprocess.PIPE lets you redirect the output
    res = subprocess.Popen(args, stdout=subprocess.PIPE)
except OSError:
    logging.error("error: popen")
    exit(-1) # if the subprocess call failed, there's not much point in continuing

#res.wait() # wait for process to finish; this also sets the returncode variable inside 'res'
if res.returncode != 0:
    logging.warn("exit processer\n")
else:
    logging.info("wait processer:({},{})".format(res.pid, res.returncode))

# access the output from stdout

#logging.info("after read: {}".format(result))
logging.info("exiting")
time = str(datetime.now())[:19]
print("----------Ngrok Start---------")
print("          At {}          ".format(time))
origin = 'http://127.0.0.1:4040/api/tunnels'
remote = 'https://nvh.monius.top/api/ngrok'
headers = {'Content-Type': 'application/json'}
origin_requset = r.get(origin)
if(origin_requset.status_code != r.codes.bad_gateway):
    url = str(origin_requset.json()['tunnels'][0]['public_url'])
    print("----------Ngrok Location:---------")
    print("           {}          ".format(url))
    print("-----------------------------")
    data = {"url":url,"time":time}
    logging.info(time,data)
    remote_requset = r.post(remote,data=data,headers=headers)
    if(remote_requset.status_code == r.codes.ok):
        http_server = WSGIServer(('', 5001), app)
        print("----------Server Start---------")
        http_server.serve_forever()
        print("----------Server Close---------")
    else:
        logging.error(remote_requset.raise_for_status())
else:
    logging.error(origin_requset.raise_for_status())