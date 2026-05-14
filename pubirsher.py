#w2 ct5
import time
import json
import random
import pandas as pd
from paho.mqtt import client as mqtt_client                                 #Library หลักที่ใช้ติดต่อสื่อสารผ่านโปรโตคอล MQTT

# TODO: UPDATE PATH CSV_FILE IN HERE --- r"/Synthetic-Data Path "
File_csv_Path = r"F:\for-learning\Data\synthetic_plant_train.csv"           #กำหนดที่อยู่ของไฟล์  #copy path จากไฟล์Data/synthetic

# NOTE: MQTT Configuration
MQTT_CONFIG = {
    "BROKER" : 'broker.emqx.io',
    "PORT"   : 1883,
    "TOPIC": "idt/plant/env",                                               #topicต้องตรงกับSubscriberที่ตั้งไว้
    "CLIENT_ID" : f'ALPHA-I-{random.randint(0,100)}'
}

def connect_mqtt():                                                                                             
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, MQTT_CONFIG["CLIENT_ID"])      # สร้างตัวแทน (Client) สำหรับติดต่อ MQTT
    client.on_connect = lambda client, userdata, flags, rc: print("CONNECTED TO MQTT BROKER!") if rc ==0 else print("FAILED TO CONNECT")    # กำหนดว่าถ้าเชื่อมต่อสำเร็จ (rc=0)"CONNECTED" ถ้าไม่สำเร็จ "FAILED"
    client.connect(MQTT_CONFIG["BROKER"], MQTT_CONFIG["PORT"], 120)         # สั่งให้เชื่อมต่อไปยัง Broker ตามที่ตั้งค่าไว้
    return client

def publisher(PUBLISH_INTERVAL_SEC= 0.5):                                   #กำหนดช่วงเวลาส่งข้อมูล
    df = pd.read_csv(File_csv_Path)                                         #อ่านไฟล์
    df = df.iloc[:10]                                                      #กำหนดให้อ่านแค่10แถวแรก
    print(f"Loaded {len(df)} rows from {File_csv_Path}")
    client = connect_mqtt()                                                 #เปิด loop เพือให้ MQTT ทํางานเบืองหลัง
    client.loop_start()                                                     #เริ่มการทำงาน

    try:
        for idx, row in df.iterrows():                                      #วนลูปทีละแถวใน CSV
            data = row.to_dict()                                            #แปลงpandas row → dict
            if "timestamp" in data:
                data["timestamp"] = str(data["timestamp"])

            payload = json.dumps(data)                                      #แปลงdict → JSON
            result = client.publish(MQTT_CONFIG["TOPIC"], payload)          #ส่งข้อมูลไปที topic ทีsubscribe จะได้รับข้อมูลทันที
            status = result[0]                                              #เช็คstatus 
            if status == 0:
                print(f"[{idx}] Published to {MQTT_CONFIG["TOPIC"]}: {payload}")    #ถ้าstatus0ผ่าน
            else:
                print(f"[{idx}] Failed to send message to {MQTT_CONFIG["TOPIC"]}")  #ถ้าstatusไม่เป็น0ไม่ผ่าน

            time.sleep(PUBLISH_INTERVAL_SEC)                                #ควบคุมความเร็วการส่ง

    except KeyboardInterrupt:
        print("\nStopping publisher...")                                    #ถ้ากดปุ่มอะไรก็ตามจะหยุดการทำงาน

    finally:
        client.loop_stop()                                                  #ปิด loop
        client.disconnect()                                                 #ตัดการเชือมต่อ
        print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    publisher()