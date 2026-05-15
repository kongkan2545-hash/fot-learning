# สรุปงานรวมทั้ง Pipeline และ Node-RED Integration

## 1. รับข้อมูลจากแหล่งข้อมูลแบบสตรีม (MQTT Protocol)
- เชื่อมต่อกับ MQTT broker: `broker.emqx.io`
- รับข้อมูลสตรีมแบบเรียลไทม์
- ใช้ `publisher.py` ส่งข้อมูล sensor ไปยัง topic:
  - `plant/env/raw`

### ตัวอย่างการเชื่อมต่อ MQTT
```python
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = 'broker.emqx.io'
MQTT_TOPIC = 'plant/env/raw'

received_messages = []

def on_connect(client, userdata, flags, rc):
    print('Connected with result code', rc)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    print('Received:', data)
    received_messages.append(data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()
```

## 2. จัดการและเตรียมข้อมูล (Data Preprocessing)
- ทำความสะอาดข้อมูล: กรองค่า missing และข้อมูลผิดปกติ
- แปลงรูปแบบข้อมูลให้โมเดลใช้งานได้
- สร้างฟีเจอร์ที่สำคัญ และปรับมาตราส่วนข้อมูล

### โค้ดตัวอย่าง preprocessing
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

raw_df = pd.DataFrame(received_messages)
raw_df = raw_df.dropna()
raw_df = raw_df[raw_df['temperature'].between(0, 50)]

raw_df['humidity_bin'] = pd.cut(raw_df['humidity'], bins=5, labels=False)
features = ['temperature', 'humidity_bin', 'soil_moisture']
X = raw_df[features]
y = raw_df['plant_status']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

## 3. พัฒนาโมเดล Machine Learning ที่มีประสิทธิภาพ
- เลือกและฝึกโมเดลที่เหมาะสม
- ปรับพารามิเตอร์เพื่อลดข้อผิดพลาด
- ประเมินผลด้วยเมตริกเช่น Accuracy และ Classification Report

### โค้ดตัวอย่างสร้างโมเดล
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print('Accuracy:', accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
```

## 4. แสดงผลข้อมูลแบบเรียลไทม์ผ่าน Dashboard
- สร้างมุมมองข้อมูลและผลลัพธ์แบบเรียลไทม์
- อัปเดตกราฟและตารางเมื่อมีข้อมูลใหม่
- ใช้ Streamlit หรือ Node-RED dashboard ได้ตามต้องการ

### ตัวอย่าง dashboard
```python
import streamlit as st
import pandas as pd

st.title('Plant Monitoring Dashboard')

live_df = pd.DataFrame(received_messages)
if not live_df.empty:
    st.line_chart(live_df[['temperature', 'soil_moisture']])
    st.dataframe(live_df.tail(10))

if st.button('Predict latest'):
    latest = live_df.iloc[-1:]
    latest_X = scaler.transform(latest[features])
    pred = model.predict(latest_X)
    st.write('Prediction:', pred[0])
```

## 5. ทดสอบโมเดลด้วยข้อมูลที่ไม่เคยเห็นมาก่อน (Unseen Data)
- ใช้ไฟล์ทดสอบแยกต่างหากเช่น `Data/synthetic_plant_test.csv`
- ประเมินโมเดลบนข้อมูลใหม่เพื่อวัดความสามารถทั่วไป

### ตัวอย่างทดสอบ Unseen Data
```python
unseen_df = pd.read_csv('Data/synthetic_plant_test.csv')
unseen_df = unseen_df.dropna()
unseen_X = scaler.transform(unseen_df[features])
unseen_y = unseen_df['plant_status']

unseen_pred = model.predict(unseen_X)
print('Unseen Accuracy:', accuracy_score(unseen_y, unseen_pred))
print(classification_report(unseen_y, unseen_pred))
```

## 6. ไฟล์สำคัญในระบบ
### `publisher.py`
- อ่านจาก: `Data/synthetic_plant_train.csv`
- ส่งข้อมูล sensor เข้า MQTT topic: `plant/env/raw`
- หน้าที่: เป็นต้นทางของ data stream

### `rt_prediction.py`
- รับจาก topic: `plant/env/raw`
- โหลดโมเดลจาก: `Data/xgb_plant_model.json`
- ทำนายผลและ publish ไปยัง topic: `plant/env/predicted`
- บันทึกผล prediction ลง: `predicted_result_1.csv`
- หน้าที่: ตัวกลางทำนายและส่งผลกลับ

### `subscriber.ipynb`
- รับจาก topic: `plant/env/predicted`
- บันทึกผล prediction ลง: `Data/received_plant_data.csv`
- หน้าที่: เก็บข้อมูลผลลัพธ์สำหรับวิเคราะห์ต่อ

### ข้อมูล Unseen
- ใช้ไฟล์: `Data/synthetic_plant_test.csv`
- ใช้สำหรับประเมินโมเดลบนข้อมูลใหม่

## 7. Node-RED Integration แบบเข้าใจง่าย
- Node-RED ใช้ MQTT broker เดียวกัน: `broker.emqx.io`
- สามารถเชื่อมต่อกับ topic ต่อไปนี้:
  - `plant/env/raw` : ข้อมูล sensor ก่อนโมเดล
  - `plant/env/predicted` : ผล prediction หลังโมเดล

### Node-RED ทำอะไรได้บ้าง
- Subscribe `plant/env/raw` เพื่อดูข้อมูล sensor
- Subscribe `plant/env/predicted` เพื่อดูผลทำนาย
- Publish ไปยัง `plant/env/raw` หาก Node-RED ต้องการเป็น publisher แทน `publisher.py`

### สรุปการเชื่อมต่อ Node-RED
1. `publisher.py` → publish data ไปยัง `plant/env/raw`
2. `rt_prediction.py` → subscribe `plant/env/raw` และ publish ผลไปยัง `plant/env/predicted`
3. `subscriber.ipynb` → subscribe `plant/env/predicted`

### ตัวอย่าง code comment สำหรับ Node-RED
```python
# publisher.py: ส่งข้อมูล sensor ไปที่ MQTT broker
client.publish(MQTT_CONFIG['TOPIC'], payload)
# TOPIC = 'plant/env/raw'

# rt_prediction.py: รับ raw data แล้ว publish prediction กลับ
client.subscribe(TOPIC_IN)  # TOPIC_IN = 'plant/env/raw'
client.publish(TOPIC_OUT, out_payload)  # TOPIC_OUT = 'plant/env/predicted'

# subscriber.ipynb: รับ prediction แล้วเก็บลง CSV
client.subscribe(MQTT_CONFIG['TOPIC'])  # TOPIC = 'plant/env/predicted'
```

## 8. สรุปการไหลของข้อมูลทั้งหมด
1. `publisher.py` อ่าน CSV → ส่งไป MQTT `plant/env/raw`
2. `rt_prediction.py` รับจาก `plant/env/raw` → ทำนาย → ส่งออก `plant/env/predicted`
3. `subscriber.ipynb` รับจาก `plant/env/predicted` → เขียนลง `Data/received_plant_data.csv`
4. ข้อมูล Unseen ใช้ `Data/synthetic_plant_test.csv` เพื่อประเมินโมเดล
