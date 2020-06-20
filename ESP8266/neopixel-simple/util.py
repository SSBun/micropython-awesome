import network
import utime
from umqtt.simple import MQTTClient

def connect_wifi():
    utime.sleep(2)
    print("")
    retry_times = 10
    wifis = {"No,thankyou-2": "beijing_newhome_11.3", "SSBun": "Bz123456"}
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    while not wifi.isconnected():
        for ssid, password in wifis.items():
            print("ready connect to wifi: " + ssid)
            wifi.connect(ssid, password)
            retry = retry_times
            success = True
            while not wifi.isconnected():
                retry -= 1
                utime.sleep(1)
                print("...")
                if retry <= 0:
                    success = False
                    break
            if success:
                print("connect WiFi:" + ssid + " success")
                break
            else:
                print("connnect WiFi:" + ssid + " failure")
    print(wifi.ifconfig())
    return wifi

# MQTT client
class MQTTManager(object):
    def __init__(self, name: str, server: str, port: str, topics: list, callback):
        self.name = name
        self.server = server
        self.port = port
        self.topics = topics
        self.callback = callback
        client = MQTTClient(name, server, port, "ssbun", "Bz550527534")
        client.set_callback(callback)
        client.connect()
        for topic in topics:
            client.subscribe(topic)
        self.client = client

    def send(self, topic: str, msg: str):
        self.client.publish(topic, msg)
    
    def loop_msg(self, block):
        while True:            
            self.client.check_msg()
            block()
            self.client.ping()     
            utime.sleep(1)
    def disconnect(self):
        self.client.disconnect()