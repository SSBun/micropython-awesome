import network, utime, upip

def connect_wifi():
    utime.sleep(2)
    retry_times = 10
    # 要连接的 Wifi 账号和密码
    wifis = {"SSID": "SSID_PASSWORD"}
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

# 检查是否安装了 umqtt
def check_umqtt_framework():
    try:
        import umqtt        
    except:
        print("umqtt not install, begain install umqtt...")
        upip.install('micropython-umqtt.simple')
    else:
        print("umqtt install successful.")

if __name__ == "__main__":
    # 先链接 Wifi
    connect_wifi()
    # 然后安装 umqtt framework
    check_umqtt_framework()
    
