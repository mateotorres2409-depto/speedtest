import subprocess
import json
from prometheus_client import start_http_server, Gauge
import time
import os

ping_latency_metric = Gauge('ping_latency', 'ping_latency_metric')
download_bandwidth_metric = Gauge('download_bandwidth', 'download_bandwidth_metric')
upload_bandwidth_metric = Gauge('upload_bandwidth', 'upload_bandwidth_metric')

def speedtest(units):
    response = subprocess.Popen('./speedtest --accept-gdpr -u '+units+' -f json-pretty', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    return json.loads(response)

def getMetrics(units):
    response = speedtest(units)
    ping_latency_metric.set(response['ping']['latency'])
    download_bandwidth_metric.set(response['download']['bandwidth'])
    upload_bandwidth_metric.set(response['upload']['bandwidth'])

if __name__ == "__main__":
    units =  os.environ.get("UNITS_SPEEDTEST", "bps")
    sleep = os.environ.get("SLEEP_SPEEDTEST", 120)
    port = os.environ.get("PORT_METRICS", 8000)
    start_http_server(int(port))
    getMetrics(units)
    while True:
        time.sleep(int(sleep))
        getMetrics(units)
else:
    print("File one executed when imported")