import subprocess
import json
from prometheus_client import start_http_server, Gauge
import time
import os

ping_latency_metric = Gauge('ping_latency', 'ping_latency_metric')
download_bandwidth_metric = Gauge('download_bandwidth', 'download_bandwidth_metric')
upload_bandwidth_metric = Gauge('upload_bandwidth', 'upload_bandwidth_metric')
download_bytes_metric = Gauge('download_bytes', 'download_bytes_metric')
upload_bytes_metric = Gauge('upload_bytes', 'upload_bytes_metric')
download_elapsed_metric = Gauge('download_elapsed', 'download_elapsed_metric')
upload_elapsed_metric = Gauge('upload_elapsed', 'upload_elapsed_metric')

def speedtest():
    response = subprocess.Popen('./speedtest -f json-pretty', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    try:
        rsJson = json.loads(response) 
    except:
        rsJson = {}
    
    return rsJson

def getMetrics():    
    response = speedtest()
    if response != {}:        
        ping_latency_metric.set(response['ping']['latency'])
        download_bandwidth_metric.set(response['download']['bandwidth'])
        upload_bandwidth_metric.set(response['upload']['bandwidth'])
        download_bytes_metric.set(response['download']['bytes'])
        upload_bytes_metric.set(response['upload']['bytes'])
        download_elapsed_metric.set(response['download']['elapsed'])
        upload_elapsed_metric.set(response['upload']['elapsed'])
        print(response['type']+" - "+response['timestamp'])
    else:
        print("Se genero error!")

if __name__ == "__main__":
    sleep = os.environ.get("SLEEP_SPEEDTEST", 900)
    port = os.environ.get("PORT_METRICS", 9090)
    start_http_server(int(port))
    getMetrics()
    while True:
        time.sleep(int(sleep))
        getMetrics()
else:
    print("File one executed when imported")