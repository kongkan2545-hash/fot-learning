# สรุปลำดับการทำงานสำหรับฮัน

ต่อไปนี้เป็นแนะนำลำดับไฟล์ที่ควรเริ่มและทำต่อ, ขั้นตอน Node-RED ที่ควรตั้งค่า, และผลลัพธ์เมื่อรันแต่ละไฟล์

## แผนสั้น (Steps)
1. ตรวจสอบข้อมูล (Data)
2. ฝึกหรือโหลดโมเดล
3. เริ่ม data stream (publisher)
4. ทำนายแบบเรียลไทม์ (rt_prediction)
5. เก็บผลลัพธ์ (subscriber)
6. แสดงผล / Dashboard และ Node-RED

---

## รายละเอียดตามลำดับ

### 1) ตรวจสอบข้อมูล
- ไฟล์: `Data/synthetic_plant_train.csv`, `Data/synthetic_plant_test.csv`
- ทำอะไร: เปิดดูความสมบูรณ์ของข้อมูล, ลบค่า missing, ตรวจความเป็นไปได้ของค่าผิดปกติ, สร้าง/เลือกฟีเจอร์
- ผลลัพธ์เมื่อรัน: Data ที่พร้อมใช้สำหรับฝึก/ทดสอบ (ไม่มีไฟล์ใหม่เป็นผลลัพธ์โดยตรง)

### 2) ฝึกหรือโหลดโมเดล
- ไฟล์: `train_model.ipynb` หรือ `test_model.ipynb` (ถ้าต้องการ retrain ให้ใช้ `train_model.ipynb`)
- ทำอะไร: ฝึกโมเดลหรือประเมินโมเดล, ปรับพารามิเตอร์
- ผลลัพธ์เมื่อรัน: โมเดลที่บันทึก เช่น `Data/xgb_plant_model.json` และรายงานเมตริก (accuracy, classification report)

### 3) เริ่ม data stream (publisher)
- ไฟล์: `publisher.py`
- ทำอะไร: อ่านข้อมูลจาก CSV และ publish ข้อมูล sensor ไปยัง MQTT topic `plant/env/raw`
- ผลลัพธ์เมื่อรัน: ข้อความ sensor ถูกส่งไปยัง MQTT broker (ไม่มีไฟล์ output; ทำให้ downstream ทำงานได้)

### 4) ทำนายแบบเรียลไทม์
- ไฟล์: `rt_prediction.py`
- ทำอะไร: subscribe `plant/env/raw`, โหลดโมเดลจาก `Data/xgb_plant_model.json`, ทำการทำนาย แล้ว publish ผลไปยัง `plant/env/predicted`
- ผลลัพธ์เมื่อรัน: ข้อความ prediction ถูก publish และบันทึกเป็น `predicted_result_1.csv`

### 5) เก็บผลลัพธ์
- ไฟล์: `subscriber.ipynb`
- ทำอะไร: subscribe `plant/env/predicted` และเขียนผลลง `Data/received_plant_data.csv`
- ผลลัพธ์เมื่อรัน: เกิดไฟล์ `Data/received_plant_data.csv` เพื่อใช้วิเคราะห์ต่อ

### 6) Dashboard / วิเคราะห์ผล
- ไฟล์: `index.py` หรือโค้ด Streamlit (ตัวอย่างอยู่ใน `combined_summary.md`)
- ทำอะไร: แสดงกราฟแบบเรียลไทม์, ให้ปุ่ม `Predict latest` ช่วยตรวจผลลัพธ์ทันที
- ผลลัพธ์เมื่อรัน: หน้า dashboard (interactive) และการพรีวิวผลทำนาย

---

## Node-RED — แนะนำขั้นตอนการตั้งค่า
1. ตั้งค่า MQTT broker เป็น `broker.emqx.io` ให้ตรงกับ Python scripts
2. สร้าง flow: `MQTT in` (topic: `plant/env/raw`) → `debug` / `chart` เพื่อดู sensor แบบเรียลไทม์
3. สร้าง flow: `MQTT in` (topic: `plant/env/predicted`) → `file` หรือ `function` เพื่อแปลงแล้วเก็บผล (หรือแสดงใน dashboard)
4. ถ้าต้องการให้ Node-RED เป็น publisher แทน `publisher.py`: ใช้ `inject` / `function` → `MQTT out` (topic: `plant/env/raw`)
5. เพิ่ม `ui_chart`, `ui_table` (จาก Dashboard nodes) เพื่อแสดง `temperature`, `soil_moisture`, และ `prediction`

---

## วิธีทดสอบแบบไม่ใช้ MQTT ภายนอก (local quick test)
1. แก้ `publisher.py` ให้ loop อ่าน CSV และเรียกฟังก์ชันที่ `rt_prediction.py` ได้โดยตรง (หรือให้ `publisher.py` publish ไปที่ localhost broker)
2. รัน `rt_prediction.py` แล้วสังเกตว่า `predicted_result_1.csv` ถูกสร้าง
3. รัน `subscriber.ipynb` เพื่อเขียนผลลง `Data/received_plant_data.csv`

ตัวอย่างคำสั่งรันทดสอบ (PowerShell):
```powershell
python publisher.py
python rt_prediction.py
# เปิด subscriber.ipynb ใน Jupyter/VSCode และรัน
```

## ไฟล์ที่เกี่ยวข้อง (สรุป)
- `publisher.py` — ส่ง raw sensor → `plant/env/raw`
- `rt_prediction.py` — รับ raw → ทำนาย → ส่ง `plant/env/predicted` + เขียน `predicted_result_1.csv`
- `subscriber.ipynb` — รับ predicted → เขียน `Data/received_plant_data.csv`
- `Data/xgb_plant_model.json` — โมเดลที่ใช้ในการทำนาย
- `Data/synthetic_plant_test.csv` — ข้อมูล Unseen สำหรับประเมิน

---

ถ้าต้องการ ผมสามารถ:
- รันชุดทดสอบ local (publisher + rt_prediction) ให้ดูผลตัวอย่าง
- หรือช่วยสร้าง Node-RED flow JSON ให้ import เข้า Node-RED ได้ทันที

จบสรุป
