import paho.mqtt.client as mqtt
import random
import sys
import json
import signal

def signal_handler(signum, frame):
    print("\nSignal received. Performing cleanup...")
    client.disconnect()
    client.loop_stop()
    sys.exit(0)

# SIGINT 시그널(Ctrl+C)을 처리하는 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

# Connection Return Codes
# 0: Connection successful
# 1: Connection refused - incorrect protocol version
# 2: Connection refused - invalid client identifier
# 3: Connection refused - server unavailable
# 4: Connection refused - bad username or password
# 5: Connection refused - not authorised
# 6-255: Currently unused.
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.connected_flag = True
        print("connected OK Returned code=", reason_code)
    else:
        print("Bad connection Returned code=", reason_code)
        client.bad_connection_flag = True

def on_disconnect(client, userdata, reason_code, properties=None, reasoncode=0):
    print("disconnecting reason " + str(reason_code))
    client.connected_flag = False
    client.disconnect_flag = True


def on_subscribe(client, userdata, mid, reason_codes, properties): 
    print("subscribed: " + str(mid) + " " + str(reason_codes))


def on_message(client, userdata, message, properties=None):
    my_dict = json.loads(message.payload.decode())
    print(f"Received {my_dict} {len(my_dict['message'])}bytes from `{message.topic}` topic")


# 새로운 클라이언트 생성
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(
    client_id=client_id,
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)


# 콜백 함수 설정
client.on_connect = on_connect          # 브로커에 접속
client.on_disconnect = on_disconnect  # 브로커에 접속중료
client.on_subscribe = on_subscribe      # topic 구독
client.on_message = on_message        # 발행된 메세지가 들어왔을 때(메시지 수신시)

# 브로커에 연결되었는지 여부를 나타내기 위함.
client.connected_flag=False
client.bad_connection_flag=False

# 브로커가 인증을 요구시
# client.username_pw_set(username="steve",password="password")

# 브로커 주소
# 브로커(address : ost, port: 1883)에 연결
try:
    client.connect('192.168.0.19', 1833)
    #client.connect('127.0.0.1', 1833)
    # client.loop_start()
except:
    print("connection failed")
    exit(1) #Should quit or raise flag to quit or retry

# 연결되기를 기다림
# count = 0
# while not client.connected_flag and not client.bad_connection_flag: #wait in loop
#     print(f"In wait loop {count}")
#     time.sleep(1)
#     count = count + 1

# # 연결에 문제가 있는 경우 종료 처리
# if client.bad_connection_flag:
#     client.loop_stop()    #Stop loop
#     sys.exit()

# momo/name  topic 으로 메세지 수신함.
topic = 'momo/name'
client.subscribe(topic)

# loop_start나 loop_forever를 사용한다면 3~6초 간격으로 재접속을 자동으로 해준다.
try:

    client.loop_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Cleaning up...")
    client.disconnect()
    client.loop_stop()
    sys.exit(0)
