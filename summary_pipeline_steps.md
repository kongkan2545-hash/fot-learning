# สรุปขั้นตอนงาน

## 1. รับข้อมูลจากแหล่งข้อมูลแบบสตรีม (MQTT Protocol)
- เริ่มต้นด้วยการเชื่อมต่อและดึงข้อมูลจากระบบสตรีมมิ่ง MQTT
- รับข้อความหรือข้อมูลเซนเซอร์แบบเรียลไทม์จากอุปกรณ์หรือโหนดต่าง ๆ
- ตรวจสอบความถูกต้องของการเชื่อมต่อและการรับข้อมูลเพื่อให้ข้อมูลสดใหม่พร้อมใช้งาน

```python
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = 'broker.hivemq.com'
MQTT_TOPIC = 'sensor/plant'

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
- ทำความสะอาดข้อมูล: กรองข้อมูลผิดพลาด ค่า missing หรือค่าผิดปกติ
- แปลงรูปแบบข้อมูลให้อยู่ในรูปที่โมเดลสามารถใช้งานได้ เช่น การเข้ารหัสค่าสัญลักษณ์ และการปรับมาตราส่วน
- สร้างฟีเจอร์ที่สำคัญ หรือเลือกฟีเจอร์ที่มีผลต่อการทำนาย
- แบ่งข้อมูลออกเป็นชุดฝึกอบรมและชุดทดสอบ (หากจำเป็น)

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

# สมมติ received_messages มาจาก MQTT
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
- เลือกอัลกอริทึมที่เหมาะสมกับปัญหาและข้อมูล
- ปรับแต่งพารามิเตอร์ของโมเดลเพื่อเพิ่มประสิทธิภาพ
- ฝึกสอนโมเดลด้วยข้อมูลที่ผ่านการเตรียมแล้ว
- ตรวจสอบประสิทธิภาพด้วยเมตริกที่เหมาะสม เช่น ความแม่นยำ, ความผิดพลาดของการทำนาย ฯลฯ

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
- สร้างแดชบอร์ดสำหรับแสดงข้อมูลสตรีมและผลลัพธ์การทำนาย
- อัปเดตกราฟและตัวชี้วัดแบบเรียลไทม์เมื่อมีข้อมูลใหม่เข้ามา
- รองรับการแสดงผลที่เข้าใจง่าย เช่น แผนภูมิ, ตาราง, และภาพรวมสถานะ

```python
import streamlit as st
import pandas as pd

st.title('Plant Monitoring Dashboard')

# สมมติ df อัปเดตจาก MQTT แบบเรียลไทม์
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
- ใช้ชุดข้อมูลที่แยกไว้สำหรับทดสอบหรือข้อมูลใหม่จากระบบจริง
- ประเมินความสามารถของโมเดลในการทั่วไปกับข้อมูลใหม่
- ตรวจสอบประสิทธิภาพและความเสถียรของโมเดลก่อนใช้งานจริง
- ปรับปรุงโมเดลหรือกระบวนการหากพบว่าความแม่นยำลดลง

## ไฟล์และเส้นทางข้อมูล
### `publisher.py`
- อ่านข้อมูลจากไฟล์: `Data/synthetic_plant_train.csv`
- แปลงแต่ละแถวเป็น JSON แล้วส่งไปที่ MQTT broker `broker.emqx.io`
- topic ส่งออก: `plant/env/raw`
- หน้าที่: สร้าง data stream สำหรับระบบเรียลไทม์

### `rt_prediction.py`
- รับข้อมูลจาก topic `plant/env/raw`
- โหลดโมเดลจากไฟล์: `Data/xgb_plant_model.json`
- ใช้โมเดลทำนายแล้วสร้างผลลัพธ์ใหม่
- ส่งผลลัพธ์ prediction ออกไปที่ topic: `plant/env/predicted`
- บันทึกผล prediction ลงไฟล์: `predicted_result_1.csv`
- หน้าที่: เป็นตัวกลางรับข้อมูล raw → ทำนาย → ส่งผลลัพธ์กลับ

### `subscriber.ipynb`
- รับข้อมูลจาก topic: `plant/env/predicted`
- บันทึกข้อมูล prediction ที่ได้รับลงไฟล์: `Data/received_plant_data.csv`
- หน้าที่: เก็บข้อมูลผลลัพธ์ที่โมเดลสร้างขึ้น พร้อมใช้งานสำหรับวิเคราะห์ต่อ

### ข้อมูล Unseen
- ใช้ไฟล์: `Data/synthetic_plant_test.csv`
- ใช้ในการทดสอบโมเดลโดยตรงเพื่อวัด performance กับข้อมูลใหม่
- สามารถทดสอบใน `test_model.ipynb` หรือ `train_model.ipynb`

## สรุปการไหลของข้อมูล
1. `publisher.py` อ่าน CSV → ส่งไป MQTT `plant/env/raw`
2. `rt_prediction.py` รับจาก `plant/env/raw` → ทำนาย → ส่งออก `plant/env/predicted`
3. `subscriber.ipynb` รับจาก `plant/env/predicted` → เขียนลง `Data/received_plant_data.csv`
4. ข้อมูล Unseen ใช้ `Data/synthetic_plant_test.csv` เพื่อประเมินโมเดล

## Node-RED Integration
- Node-RED สามารถเชื่อมต่อกับ broker เดียวกัน: `broker.emqx.io`
- Node-RED สามารถทำงานได้ทั้งแบบ
  - Subscribe ข้อมูลจาก topic `plant/env/raw` เพื่อดู data stream ก่อนเข้าโมเดล
  - Subscribe ข้อมูลจาก topic `plant/env/predicted` เพื่อแสดงผล prediction แบบเรียลไทม์
  - Publish ข้อมูลเข้า topic `plant/env/raw` หากต้องการให้ Node-RED เป็น publisher แทน `publisher.py`

### ตัวอย่างการเชื่อมต่อ Node-RED
- node MQTT input: topic `plant/env/raw` → รับค่าจาก `publisher.py`
- node MQTT input: topic `plant/env/predicted` → รับค่าจาก `rt_prediction.py`
- node MQTT output: topic `plant/env/raw` → ส่งค่า sensor ใหม่เข้า pipeline

### comment code สำหรับ Node-RED
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

```python
unseen_df = pd.read_csv('Data/synthetic_plant_test.csv')
unseen_df = unseen_df.dropna()
unseen_X = scaler.transform(unseen_df[features])
unseen_y = unseen_df['plant_status']

unseen_pred = model.predict(unseen_X)
print('Unseen Accuracy:', accuracy_score(unseen_y, unseen_pred))
print(classification_report(unseen_y, unseen_pred))
```

