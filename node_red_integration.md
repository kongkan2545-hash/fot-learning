# Node-RED Integration Summary

## 1. จุดเชื่อมต่อหลัก
- Node-RED ใช้ MQTT broker เดียวกับโค้ดใน workspace
- broker: `broker.emqx.io`
- ข้อมูลวิ่งผ่าน topic สองหัวข้อหลัก
  - `plant/env/raw`
  - `plant/env/predicted`

## 2. `publisher.py` ต่อกับ Node-RED อย่างไร
- `publisher.py` อ่านข้อมูลจาก `Data/synthetic_plant_train.csv`
- ส่งข้อมูลออกไปยัง topic:
  - `plant/env/raw`
- Node-RED สามารถ subscribe topic นี้เพื่อดูข้อมูล sensor ก่อนเข้าโมเดล

## 3. `rt_prediction.py` ต่อกับ Node-RED อย่างไร
- รับข้อมูลจาก topic:
  - `plant/env/raw`
- ทำนายผลด้วยโมเดลจาก:
  - `Data/xgb_plant_model.json`
- ส่งผลลัพธ์ prediction ออกไปที่ topic:
  - `plant/env/predicted`
- Node-RED สามารถ subscribe topic นี้เพื่อแสดงผล prediction แบบเรียลไทม์

## 4. `subscriber.ipynb` ต่อกับ Node-RED อย่างไร
- รับข้อมูลจาก topic:
  - `plant/env/predicted`
- บันทึกผล prediction ลงไฟล์:
  - `Data/received_plant_data.csv`
- Node-RED สามารถใช้ topic นี้เป็นแหล่งข้อมูลสำหรับ dashboard หรือการแจ้งเตือน

## 5. สรุปภาพรวมการเชื่อมต่อ
1. `publisher.py` → publish data ไปยัง `plant/env/raw`
2. `rt_prediction.py` → subscribe `plant/env/raw` และ publish ผลไปยัง `plant/env/predicted`
3. `subscriber.ipynb` → subscribe `plant/env/predicted`

## 6. หากต้องการใช้ Node-RED เป็น publisher แทน
- ให้ Node-RED publish ข้อความไปยัง topic:
  - `plant/env/raw`
- `rt_prediction.py` จะยังรับข้อมูลจาก topic เดิมและทำงานได้ปกติ

## 7. ตัวอย่างการใช้ Node-RED
- MQTT in node -> topic `plant/env/raw` : ดูข้อมูล sensor
- MQTT in node -> topic `plant/env/predicted` : ดูผล prediction
- MQTT out node -> topic `plant/env/raw` : ส่งข้อมูลเข้าสู่ pipeline
