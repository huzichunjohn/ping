from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PingForm
from .models import Ping
import json
from netaddr import iter_iprange
import redis
import uuid

from .config import REDIS_SERVER, REDIS_PORT, REDIS_DB

def index(request):
    if request.method == 'POST':
	form = PingForm(request.POST)
	if form.is_valid():
	    start_ip, end_ip = form.cleaned_data.get('network_range').split('-')
	    ip_list = [str(ip) for ip in iter_iprange(start_ip, end_ip)]
	    task_id = str(uuid.uuid4())
	    conn = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)
            conn.set("task_id", task_id)
	    for ip in ip_list:
		conn.lpush(task_id, ip)
	    return HttpResponseRedirect('/task/'+task_id+'/')
    else:
	form = PingForm()

    return render(request, 'index.html', {'form': form})

def detail(request, task_id):
    pings = Ping.objects.filter(task_id=uuid.UUID(task_id))
    return render(request, 'detail.html', {'pings': pings})
