# ลำดับการรันไฟล์ในโปรเจกต์

## 1. publisher.py
- เริ่มจากไฟล์นี้เป็นอันดับแรก
- อ่านข้อมูลจาก `Data/synthetic_plant_train.csv`
- ส่งข้อมูลเป็น MQTT message ไปที่ topic `plant/env/raw`
- ผลลัพธ์: ไม่มีไฟล์ CSV ใหม่สร้างจากไฟล์นี้โดยตรง แต่เป็นจุดเริ่มต้นของข้อมูลเพื่อให้ระบบอื่นใช้งานต่อ

## 2. rt_prediction.py
- ถัดมารันไฟล์นี้
- รับข้อมูลจาก topic `plant/env/raw`
- โหลดโมเดลจาก `Data/xgb_plant_model.json`
- ทำการทำนายและส่งข้อมูลผลลัพธ์กลับไปที่ topic `plant/env/predicted`
- ผลลัพธ์: สร้างไฟล์ `predicted_result_1.csv`

## 3. subscriber.ipynb
- หากต้องการเก็บข้อมูลผลลัพธ์จาก topic `plant/env/predicted`
- รับข้อมูลจาก MQTT topic นี้
- บันทึกลงไฟล์ `Data/received_plant_data.csv`
- ผลลัพธ์: สร้างหรือเพิ่มข้อมูลใน `Data/received_plant_data.csv`

## สรุป
- เริ่มที่ `publisher.py`
- ต่อด้วย `rt_prediction.py` เพื่อได้ไฟล์ `predicted_result_1.csv`
- ถ้าต้องการเก็บผลลัพธ์ MQTT เพิ่มเติม ให้ใช้ `subscriber.ipynb` เพื่อได้ไฟล์ `Data/received_plant_data.csv`
