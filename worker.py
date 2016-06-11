import redis
import gevent
from gevent.subprocess import Popen, PIPE
import re
from datetime import datetime
import time
import uuid

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ping.settings'
from detect.models import Ping

from detect.config import REDIS_SERVER, REDIS_PORT, REDIS_DB

def ping(ip, task_id):
    loss = latency = None
    p = Popen(['ping', '-c', '3', ip], stdout=PIPE, stderr=PIPE) 
    out, err = p.communicate()
    out = out.split('\n')
    for line in out:
	line = line.rstrip()
        match = re.match('.* ([0-9]+)% packet loss.*', line)
        if match:
	    loss = match.group(1)

        match = re.match('.*([0-9\.]+)/([0-9\.]+)/([0-9\.])+/([0-9\.]+) ms.*', line)
        if match:
	    latency = match.group(2)
    ping = Ping()
    ping.ip = ip
    ping.task_id = uuid.UUID(task_id)

    if loss:
        ping.loss = loss

    if latency:
        ping.latency = float(latency)

    ping.save()

if __name__  == "__main__":
    threads = []
    conn = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)
    task_id = conn.get("task_id")
    while True:
        if task_id:
            ip = conn.rpop(task_id)
            while ip:
	        threads.append(gevent.spawn(ping, ip, task_id))	
                ip = conn.rpop(task_id)
    	    gevent.joinall(threads)
            conn.delete(task_id)
	    conn.delete("task_id")
        time.sleep(0.5)
        task_id = conn.get("task_id")
