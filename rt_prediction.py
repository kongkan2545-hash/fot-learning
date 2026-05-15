#Import Libraries
import json                                                         #แปลงข้อมูล MQTT (string ↔ dict)
import os                                                           #ตรวจสอบไฟล์ว่ามีอยู่หรือไม่
import csv                                                          #บันทึกผลลัพธ์ลงไฟล์ CSV
import paho.mqtt.client as mqtt                                     #เชือมต่อและสือสารกับ MQTT Broker 
import numpy as np                                                  #จัดรูปแบบข้อมูลเปน array สําหรับโมเดล
from xgboost import XGBClassifier                                   #XGBClassifier → ใช้โหลดโมเดล XGBoost

#กําหนดค่าการเชื่อมต่อ MQTT
BROKER_HOST = "broker.emqx.io"                                      #กำหนด broker ทีจะเชือมต่อ
BROKER_PORT = 1883                                                  #ใช้ port 1883 (MQTT แบบไม่เข้ารหัส)

#กําหนด Topic
TOPIC_IN = "plant/env/raw"                                          #รับข้อมูล sensor
TOPIC_OUT = "plant/env/predicted"                                   #ส่งผลการทํานายกลับออกไป

#กําหนด Path โมเดลและไฟลบันทึก
MODEL_PATH = r"F:\for-learning\Data\xgb_plant_model.json"           #ไฟล์โมเดล XGBoost (.json)
OUTPUT_CSV = "predicted_result_1.csv"                               #ไฟล์ CSV สําหรับบันทึก prediction #ชื่อไฟล์ของเรา

#กําหนด label mapping
label_map = {0: "normal", 1: "alert", 2: "alarm"}                   #แปลง class ตัวเลข → ชือสถานะ

#ตัวแปรสําหรับจัดการ CSV
fieldnames = None                                                   #การสร้าง header ครังแรก
writer_initialized = False                                          #ป้องกันการเขียน header ซ้ำ

#ฟังก์ชันโหลดโมเดล
def load_model():
    model = XGBClassifier()                                         #สร้าง object XGBClassifier()
    model.load_model(MODEL_PATH)                                    #โหลดไฟล์โมเดลจาก MODEL_PATH
    print(f"Loaded model from {MODEL_PATH}")                        #แสดงข้อความว่าโหลดสําเร็จ
    return model                                                    #คืนค่าโมเดลกลับ

model = load_model()                                                #โมเดลถูกโหลดทันทีตอนเริมโปรแกรม

#ฟังก์ชันบันทึกผลลง CSV
def save_prediction_row(data: dict):
    global fieldnames, writer_initialized
    
    if not writer_initialized:                                          #ทำงานเมื่อยังไม่เคยตั้งค่าคอลัมน์ (รันครั้งแรก)
        fieldnames = list(data.keys())                                  #เอาชื่อ Key ทั้งหมดจากข้อมูลมาตั้งเป็นชื่อคอลัมน์
        
        file_exits = os.path.isfile(OUTPUT_CSV)                         #ตรวจสอบดูว่าไฟล์ CSV นี้เคยถูกสร้างไว้แล้วหรือยัง
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:  #เปิดไฟล์โหมด "a" (Append - เขียนต่อท้าย)
            writer = csv.DictWriter(f, fieldnames=fieldnames)           #สร้างตัวเขียนข้อมูลลง CSV
            if not file_exits:                                          #ถ้ายังไม่เคยมีไฟล์นี้
                writer.writeheader()                                    #ให้เขียนชื่อคอลัมน์ (Header) ไว้บรรทัดแรกสุด
            writer.writerow(data)                                       #เขียนข้อมูลเซ็นเซอร์และผลการทำนายลงไป 1 บรรทัด
            
        writer_initialized = True                                       #เปลี่ยนสถานะว่าทำการตั้งค่าและเขียน Header เรียบร้อยแล้ว
    else:                                                               #ทำงานในครั้งต่อๆ ไป (เมื่อตั้งค่าไปแล้ว)
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:  #เปิดไฟล์โหมดเขียนต่อท้าย
            writer = csv.DictWriter(f, fieldnames=fieldnames)           #สร้างตัวเขียนข้อมูล
            writer.writerow(data)                                       #เขียนข้อมูลบรรทัดใหม่ลงไปได้เลยโดยไม่ต้องสน Header แล้ว

#ฟังก์ชัน on_connect            
def on_connect (client, userdata, flags, rc):
    if rc == 0:                                                 #rc ย่อมาจาก Return Code ถ้าเท่ากับ 0 แปลว่าเชื่อมต่อสำเร็จ
        print("Connected to MQTT broker.")                      #พิมพ์แจ้งว่าเชื่อมต่อแล้ว
        client.subscribe(TOPIC_IN)                              #สั่งให้ติดตาม (Subscribe) ข้อมูลจาก TOPIC_IN ทันที
        print(f"Subscribed to {TOPIC_IN}")
    else:                                                       #ถ้ารหัสไม่ใช่ 0
        print(f"Failed to connect, rc={rc}")                    #พิมพ์แจ้งเตือนว่าเชื่อมต่อไม่สำเร็จ

#ฟังก์ชัน on_message
def on_message (client, userdata, msg):                         #จะถูกเรียกทุกครังทีมี message ใหม่เข้ามา
    try:
        #แปลง payload เปน dict
        payload_str = msg.payload.decode("utf-8")               #แปลงข้อมูลดิบ (Bytes) ที่รับมาจาก MQTT เป็นข้อความ (String)
        data = json.loads(payload_str)                          #แปลงข้อความ JSON ให้เป็น Dictionary ของ Python

        #ดึง feature ออกมา
        temp = data.get("temp_c", None)                         #ดึงค่าอุณหภูมิ (ถ้าไม่มีให้เป็น None)
        hum = data.get("humidity_pct", None)                    #ดึงค่าความชื้น
        lux = data.get("lux", None)                             #ดึงค่าความสว่าง 
        vpd = data.get("vpd_kpa", None)                         #ดึงค่า VPD (Vapor Pressure Deficit)

        #ตรวจสอบข้อมูลครบไหม
        if None in (temp, hum, lux, vpd):                                   #ตรวจสอบว่ามีข้อมูลตัวไหนขาดหายไปหรือไม่
            print("Missing features in message, skipping:", data)           #ถ้า feature ขาด → ไม่ทํานาย
            return
        
        #เตรียม input สําหรับโมเดล
        x_input = np.array([[temp, hum, lux, vpd]], dtype=float)            #จัดรูปแบบเป็น 2D array

        #ทํานายผล
        y_pred = model.predict(x_input)[0]                                  #class ทีทํานาย
        y_prob = model.predict_proba(x_input)[0]                            #ความน่าจำเป็นแต่ละ class
        
        #แปลง class เป็น label
        label = label_map.get(int(y_pred), "unknown")                       #แปลงเลขผลลัพธ์ที่ได้ เป็นข้อความสถานะ ("normal", "alert", "alarm")
        
        #เพิมผลลัพธ์เข้า dict                                                   #เพิ่ม key ใหม่ เช่น
        data["y_pred"] = int(y_pred)                                        #เลขสถานะ (0, 1, 2)
        data["y_label_pred"] = label                                        #ชื่อสถานะ   
        data["y_pred_prob_normal"] = float(y_prob[0])                       #โอกาสที่จะเป็น normal (%)
        data["y_pred_prob_alert"] = float(y_prob[1])                        #โอกาสที่จะเป็น alert (%)
        data["y_pred_prob_alarm"] = float(y_prob[2])                        #โอกาสที่จะเป็น alarm (%) 
        
        if "timestamp" in data:                                             #เช็คว่ามีเวลา (timestamp) ส่งมาด้วยไหม
            data["timestamp"] = str(data["timestamp"])                      #แปลงเวลาเป็นข้อความเพื่อป้องกัน Error ตอนแปลงกลับเป็น JSON
        
        out_payload = json.dumps(data)                                      #แพ็คข้อมูลชุดใหม่ (ที่มีผลทำนายแล้ว) กลับเป็นรูปแบบข้อความ JSON

        #Publish ผลลัพธ์กลับไป MQTT
        client.publish(TOPIC_OUT, out_payload)                              #ส่งไป topic: plant/env/predicted
        
        #บันทึกลง CSV
        save_prediction_row(data)                                           #เรียกใช้ฟังก์ชันเซฟข้อมูลลงไฟล์ CSV
        print(f"Saved prediction to {OUTPUT_CSV}")                          #แจ้งว่าบันทึกสำเร็จ

    #หากเกิด error    
    except Exception as e:                                                  #ป้องกันโปรแกรมค้างหากเกิดข้อผิดพลาด
        print("Error in on_message", e)                                     #แสดง error

#ฟังก์ชัน main()
def main():
    client = mqtt.Client()                                                  #สร้างตัวแทน (Client) สำหรับสื่อสาร MQTT
    client.on_connect = on_connect                                          #ผูกฟังก์ชัน on_connect เข้ากับเหตุการณ์ "เมื่อเชื่อมต่อสำเร็จ"
    client.on_message = on_message                                          #ผูกฟังก์ชัน on_message เข้ากับเหตุการณ์ "เมื่อมีข้อความเข้ามา"

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)                  #สั่งเริ่มการเชื่อมต่อไปยังเซิร์ฟเวอร์ (Broker) พร้อมระบุว่าให้เช็คสถานะการเชื่อมต่อทุก 60 วินาที
    print("Starting predictior loop. Ctrl+C to stop.")

    try:
        client.loop_forever()                                               #สั่งให้โปรแกรมวนลูปทำงานไปเรื่อยๆ เพื่อรอรับข้อความโดยไม่จบการทำงาน
    except KeyboardInterrupt:                                               #ดักจับเหตุการณ์เมื่อผู้ใช้กด Ctrl+C ที่คีย์บอร์ด
        print('\nStopping predictor...')                                    #พิมพ์แจ้งว่ากำลังหยุดการทำงาน
    finally:
        client.disconnect()                                                 #ตัดการเชื่อมต่อจาก Broker อย่างสมบูรณ์
        print("Disconnected from MQTT broker.")
        
#Entry Point        
if __name__ == "__main__":                                                  #เป็นบรรทัดมาตรฐานของ Python ตรวจสอบว่าไฟล์นี้ถูกรันโดยตรง (ไม่ได้ถูก import จากไฟล์อื่น)
    main()                                                                  #เรียกฟังก์ชัน main() เพื่อสตาร์ทโปรแกรม