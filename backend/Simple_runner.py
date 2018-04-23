
import os
import json
import socket
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
    loc =(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)),s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    pub = str(origin_requset.json()['tunnels'][0]['public_url'])
    print("----------Ngrok Location:---------")
    print("   loc:{}     pub:{}  ".format(loc,pub))
    print("-----------------------------")
    data = {"pub": pub, "loc": loc, "time": time}
    logging.info(time,data)
    remote_requset = r.post(remote,data=json.dumps(data),headers=headers)
    if(remote_requset.status_code == r.codes.ok):
        http_server = WSGIServer(('', 5001), app)
        print("----------Server Start---------")
        http_server.serve_forever()
        print("----------Server Close---------")
    else:
        logging.error(remote_requset.raise_for_status())
else:
    logging.error(origin_requset.raise_for_status())


