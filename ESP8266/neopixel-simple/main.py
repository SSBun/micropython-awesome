from machine import Pin
import uasyncio as asyncio
from umqtt.simple import MQTTClient
import neopixel

# 客户端 ID
CLIENT_ID = b'light1_'
# 你的 mqtt 服务器地址
SERVER = 'csl.cool'
# 你的 matt 服务端口号
SERVER_PORT = 1883

# LED 灯泡的个数
LED_COUNT = 16

# mqtt 订阅的主题内容
TOPIC_SET_ON = CLIENT_ID + b"setOn"
TOPIC_GET_ON = CLIENT_ID + b"getOn"
TOPIC_SET_RGB = CLIENT_ID + b"setRGB"
TOPIC_GET_RGB = CLIENT_ID + b"getRGB"
TOPIC_SET_WHITE = CLIENT_ID + b"setWhite"
TOPIC_GET_WHITE = CLIENT_ID + b"getWhite"
TOPIC_GET_ONLINE = CLIENT_ID + b"getOnline"


np = neopixel.NeoPixel(Pin(4), LED_COUNT)

lightColor = (255, 255, 255)

def led_clean():
    for i in range(0, LED_COUNT):
        np[i] = (0, 0, 0)
    np.write()

def mqtt_callback(topic, msg):
    print(topic)
    print(msg)
    global lightColor
    # `topic` 接收到的主题
    # `msg` 主题下更新的信息
    if topic == TOPIC_SET_ON:
        if msg == b'1':
            np.fill(lightColor)
        else:
            np.fill((0, 0, 0))
    elif topic == TOPIC_SET_RGB:
        lightColor = tuple(map(lambda x: int(x), msg.decode().split(",")))
        np.fill(lightColor)
        print(lightColor)
    np.write()

async def check_message(mqtt):    
    while True:
        # 检查主题是否有更新，会调用 `mqtt_callback`
        mqtt.check_msg()
        # 休眠 1s 再检查
        await asyncio.sleep(1)

async def ping_server(mqtt):
    while True:
        # ping mqtt 服务器保持连接
        mqtt.ping()
        print("ping server ...")
        await asyncio.sleep(30)

def main():
    # 初始化 mqtt 客户端
    # `60` 是指在一次通信后，保持连接 60s 的时间，如果超过这个时间没有和服务器通信
    # 服务器会认为连接已经断开，这里我们每 30s 钟 ping 一下服务器保持连接
    print("Ready to connect mqtt...")
    mqtt = MQTTClient(CLIENT_ID, SERVER, SERVER_PORT, "mqtt server account", "mqtt server password", 60)
    # 设置回调
    mqtt.set_callback(mqtt_callback)
    # 连接服务器
    mqtt.connect()
    print("Connect to mqtt server")
    # 订阅主题
    mqtt.subscribe(TOPIC_SET_ON)
    mqtt.subscribe(TOPIC_GET_ON)
    mqtt.subscribe(TOPIC_SET_RGB)
    mqtt.subscribe(TOPIC_GET_RGB)
    mqtt.subscribe(TOPIC_SET_WHITE)
    mqtt.subscribe(TOPIC_GET_WHITE)
    mqtt.subscribe(TOPIC_GET_ONLINE)

    # uasyncio 是 micropython 下的多线程工具
    loop = asyncio.get_event_loop()
    # 开始监听
    loop.create_task(check_message(mqtt))
    # 每 30s ping 一下服务器
    loop.create_task(ping_server(mqtt))
    loop.run_forever()

if __name__ == "__main__":
    main()