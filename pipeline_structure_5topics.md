# สรุประบบ Pipeline แบบ 5 หัวข้อหลัก

## 1. รับข้อมูลจากแหล่งข้อมูลแบบสตรีม (MQTT Protocol)

### ไฟล์ที่เกี่ยวข้อง
- **publisher.py** — ตัวส่ง (Publisher)

### ขั้นตอนการทำงาน
1. อ่านข้อมูลจากไฟล์ `Data/synthetic_plant_train.csv`
2. เชื่อมต่อกับ MQTT broker: `broker.emqx.io`
3. Publish ข้อมูล sensor ไปยัง topic: `plant/env/raw`

### ผลลัพธ์เมื่อรัน
- ข้อความ sensor ถูกส่งไปยัง MQTT broker ในรูปแบบ JSON
- ไม่มีไฟล์ output โดยตรง แต่ทำให้ downstream components (rt_prediction.py) สามารถรับข้อมูลได้

### Node-RED Integration (ขั้นตอนที่ 1)
- สร้าง node `MQTT in` → subscribe topic `plant/env/raw`
- เชื่อมต่อกับ `debug` หรือ `chart` node เพื่อดูข้อมูล sensor แบบเรียลไทม์
- ตัวเลือก: ให้ Node-RED เป็น publisher แทน `publisher.py` โดยใช้ `inject` / `function` → `MQTT out` (topic: `plant/env/raw`)

---

## 2. จัดการและเตรียมข้อมูล (Data Preprocessing)

### ไฟล์ที่เกี่ยวข้อง
- **Data/synthetic_plant_train.csv** — ข้อมูลฝึก
- **Data/synthetic_plant_test.csv** — ข้อมูลทดสอบ
- **train_model.ipynb** — Notebook สำหรับฝึกโมเดล (รวมขั้นตอน preprocessing)

### ขั้นตอนการทำงาน
1. ตรวจสอบความสมบูรณ์ของข้อมูล
   - ลบค่า missing (NaN)
   - ตรวจและกรองค่าผิดปกติ (outliers)
2. เลือก/สร้างฟีเจอร์ที่สำคัญ เช่น:
   - `temperature`
   - `humidity` → แปลงเป็น `humidity_bin` (categorical)
   - `soil_moisture`
3. ปรับมาตราส่วนข้อมูล (Normalization/Standardization) ด้วย `StandardScaler`
4. แบ่ง data เป็น training/testing set (80/20)

### ผลลัพธ์เมื่อรัน
- ข้อมูลที่สะอาดและพร้อมใช้สำหรับฝึก
- Output: ไม่มีไฟล์ใหม่เป็นผลลัพธ์โดยตรง (เป็นส่วนของ training pipeline)
- ผู้ใช้สามารถดูรายงาน preprocessing ในตัว notebook

---

## 3. พัฒนาโมเดล Machine Learning ที่มีประสิทธิภาพ

### ไฟล์ที่เกี่ยวข้อง
- **train_model.ipynb** — ฝึกโมเดล (สร้าง/บันทึก)
- **test_model.ipynb** — ประเมินโมเดล (ถ้าต้องการ retrain ให้ใช้ train_model.ipynb)
- **Data/xgb_plant_model.json** — โมเดลที่บันทึก (XGBoost format)
- **Data/xgb_plant_model_meta.json** — Metadata ของโมเดล

### ขั้นตอนการทำงาน
1. เลือกโมเดล: XGBoost (หรืออื่น ๆ ตามที่เหมาะสม)
2. ตั้งค่าพารามิเตอร์เหมาะสม
   - `n_estimators`, `max_depth`, `learning_rate`, เป็นต้น
3. ฝึกโมเดลด้วยข้อมูล training set
4. ประเมินผลด้วยเมตริก:
   - **Accuracy**
   - **Classification Report** (Precision, Recall, F1-Score)
   - **Confusion Matrix**
5. บันทึกโมเดลเป็น `Data/xgb_plant_model.json`

### ผลลัพธ์เมื่อรัน
- ไฟล์ `Data/xgb_plant_model.json` — โมเดลที่พร้อมใช้งาน
- ไฟล์ `Data/xgb_plant_model_meta.json` — ข้อมูล metadata (เช่น feature names, scaler parameters)
- Output ใน notebook: รายงานเมตริก (Accuracy, Classification Report)

---

## 4. แสดงผลข้อมูลแบบเรียลไทม์ผ่าน Dashboard

### ไฟล์ที่เกี่ยวข้อง
- **rt_prediction.py** — ตัวทำนาย (ทำหน้าที่กลาง)
- **subscriber.ipynb** — ตัวเก็บผล
- **index.py** — Dashboard (Streamlit หรือ framework อื่น)
- **Data/received_plant_data.csv** — ข้อมูลผลลัพธ์ที่เก็บ

### ขั้นตอนการทำงาน
1. **rt_prediction.py** ทำการ:
   - Subscribe topic `plant/env/raw` เพื่อรับข้อมูล sensor
   - โหลดโมเดลจาก `Data/xgb_plant_model.json`
   - ทำการทำนายผล
   - Publish ผลไปยัง topic `plant/env/predicted`
   - บันทึกผล prediction เป็น `predicted_result_1.csv`

2. **subscriber.ipynb** ทำการ:
   - Subscribe topic `plant/env/predicted`
   - เขียนผล prediction ลง `Data/received_plant_data.csv`

3. **index.py / Dashboard** ทำการ:
   - อ่านข้อมูลแบบเรียลไทม์จาก MQTT topics
   - แสดงกราฟ (line chart) สำหรับ temperature, soil_moisture
   - แสดงตารางข้อมูลล่าสุด (tail 10 rows)
   - ให้ปุ่ม "Predict latest" เพื่อทำนายแบบทันที

### ผลลัพธ์เมื่อรัน
- **rt_prediction.py** → ไฟล์ `predicted_result_1.csv` (บันทึกผล prediction)
- **subscriber.ipynb** → ไฟล์ `Data/received_plant_data.csv` (เก็บผล prediction เป็นระยะ)
- **Dashboard** → หน้าแสดงผลแบบ interactive ใน web browser (เช่น http://localhost:8501 สำหรับ Streamlit)

### Node-RED Integration (ขั้นตอนที่ 2-5)
1. Subscribe `plant/env/predicted` ด้วย node `MQTT in`
2. เชื่อมต่อ `debug` / `function` เพื่อแปลงข้อมูลถ้าต้องการ
3. เชื่อมต่อ `file` node เพื่อบันทึกลง CSV (ทำงานเหมือน subscriber.ipynb)
4. เชื่อมต่อ Dashboard UI nodes (`ui_chart`, `ui_table`, `ui_gauge`) เพื่อแสดงค่า temperature, soil_moisture, prediction
5. ตั้งค่า `ui_chart` ให้อัปเดต real-time จากข้อมูล MQTT

---

## 5. ทดสอบโมเดลด้วยข้อมูลที่ไม่เคยเห็นมาก่อน (Unseen Data)

### ไฟล์ที่เกี่ยวข้อง
- **Data/synthetic_plant_test.csv** — ข้อมูล Unseen
- **test_model.ipynb** — Notebook สำหรับทดสอบ

### ขั้นตอนการทำงาน
1. อ่านข้อมูล Unseen จาก `Data/synthetic_plant_test.csv`
2. ทำ preprocessing เดียวกับ training data (ใช้ scaler เดียวกัน)
3. โหลดโมเดลจาก `Data/xgb_plant_model.json`
4. ทำการทำนายบน Unseen data
5. ประเมินผลด้วยเมตริก:
   - **Unseen Accuracy**
   - **Classification Report**
   - **Confusion Matrix**

### ผลลัพธ์เมื่อรัน
- Output ใน notebook: รายงานเมตริก (Accuracy, Precision, Recall, F1-Score)
- ข้อมูลยืนยันความสามารถของโมเดลบนข้อมูลใหม่
- ไม่มีไฟล์ output ใหม่เป็นผลลัพธ์โดยตรง (เป็นการประเมินเท่านั้น)

---

## สรุปลำดับการรันทั้งระบบ

| ขั้นตอน | ไฟล์ | ผลลัพธ์ |
|--------|------|--------|
| 1. สตรีม | `publisher.py` | ส่ง raw sensor → topic `plant/env/raw` |
| 2. Preprocessing + ฝึก | `train_model.ipynb` | สร้าง `Data/xgb_plant_model.json` |
| 3. ทำนาย | `rt_prediction.py` | สร้าง `predicted_result_1.csv`, ส่ง → topic `plant/env/predicted` |
| 4. เก็บผล | `subscriber.ipynb` | สร้าง `Data/received_plant_data.csv` |
| 5. Dashboard | `index.py` | หน้า web interactive |
| 6. ทดสอบ Unseen | `test_model.ipynb` | รายงานเมตริก |

---

## วิธีการรันทดลอง (Local Quick Test)

### ขั้นตอนบน PowerShell:
```powershell
# 1. ฝึกโมเดล (ถ้ายังไม่มี xgb_plant_model.json)
# เปิด Jupyter notebook train_model.ipynb และรัน

# 2. เริ่ม publisher
python publisher.py

# 3. เปิด terminal ใหม่ แล้วเริ่ม rt_prediction
python rt_prediction.py

# 4. เปิด terminal ใหม่ แล้วเปิด subscriber.ipynb ใน Jupyter
jupyter notebook subscriber.ipynb

# 5. เปิด terminal ใหม่ แล้วรัน dashboard
python index.py

# 6. ทดสอบ Unseen data
# เปิด test_model.ipynb ใน Jupyter แล้วรัน
```

---

## Node-RED Flow Summary

### Flow 1: ดูข้อมูล Raw (MQTT in from plant/env/raw)
```
MQTT in (plant/env/raw) → debug / ui_chart
```

### Flow 2: ดูผลทำนาย (MQTT in from plant/env/predicted)
```
MQTT in (plant/env/predicted) → file / ui_chart / ui_table
```

### Flow 3: (ตัวเลือก) Publisher แทน publisher.py
```
inject / function → MQTT out (plant/env/raw)
```

---

## หมายเหตุสำคัญ
- ให้ MQTT broker (`broker.emqx.io`) ยังคงทำงาน ตลอดเวลา
- topics ที่ใช้: `plant/env/raw` (input) และ `plant/env/predicted` (output)
- โมเดลต้องบันทึกเป็น `Data/xgb_plant_model.json` เพื่อให้ `rt_prediction.py` โหลดได้
- Scaler parameters ควรบันทึกด้วย เพื่อให้ real-time data ได้รับการ normalize อย่างถูกต้อง

จบสรุป
