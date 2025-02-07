import paho.mqtt.client as mqtt
import json
import time
import random
import sys


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


def on_publish(client, userdata, mid, reason_code=0, properties=None):
    print("In on_pub callback mid= ", mid)


# 새로운 클라이언트 생성 - 인자로 이름 지정?
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(
    client_id=client_id,
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect  # 연결시 콜백 함수
client.on_disconnect = on_disconnect
client.on_publish = on_publish


# 브로커에 연결되었는지 여부를 나타내기 위함.
client.connected_flag=False
client.bad_connection_flag=False


# 브로커가 인증을 요구시
# client.username_pw_set(username="steve",password="password")


# 브로커 연결 주소 및 포트 번호
# address : localhost, port: 1883 에 연결
try:
    client.connect('192.168.0.19', 1833) #connect to broker
    #client.connect('127.0.0.1', 1833) #connect to broker
    client.loop_start()
except:
    print("connection failed")
    exit(1) #Should quit or raise flag to quit or retry


# 연결되기를 기다림 - 연결이 오래걸리거나 안되는 경우 처리????
while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)

# 연결에 문제가 있는 경우 종료 처리
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()
   

# loop_start나 loop_forever를 사용한다면 3~6초 간격으로 재접속을 자동으로 해준다.
# client.loop_start()


for i in range(100):
    # momo/name topic 으로 메세지 발행
    topic = 'momo/name'
    msg_count = i
    msg = f"{msg_count}"
    # result = client.publish(topic, msg)
    result = client.publish(topic, json.dumps({"message": msg}))

    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    time.sleep(1)  

# 연결 종료
client.disconnect()

client.loop_stop()
