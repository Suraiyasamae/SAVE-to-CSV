import requests
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# อ่านไฟล์ CSV
data = pd.read_csv('thermal_data.csv', header=None)

# ฟังก์ชันในการพล็อตภาพความร้อน
def plot_thermal_image(row_data, timestamp):
    # แปลงข้อมูลแถวเป็นตัวเลข โดยข้ามเวลา
    row_data_numeric = pd.to_numeric(row_data[1:], errors='coerce')
    # ตรวจสอบว่าการแปลงเป็นตัวเลขสำเร็จหรือไม่
    if row_data_numeric.isnull().any():
        print("ข้อผิดพลาด: ข้อมูลที่ไม่ใช่ตัวเลขถูกพบ.")
        return

    # แปลงข้อมูลเป็นอาร์เรย์ขนาด 24x32 (ข้ามเวลา)
    thermal_data = np.array(row_data_numeric).reshape(24, 32)

    # สร้างรูปภาพและแกน
    fig, ax = plt.subplots()

    # พล็อตภาพความร้อน
    im = ax.imshow(thermal_data, cmap='hot', interpolation='nearest')

    # เพิ่มแถบสี
    cbar = plt.colorbar(im)
    cbar.set_label('อุณหภูมิ (°C)')

    # ตั้งชื่อเรื่องด้วยเวลาที่บันทึก
    plt.title(f'ภาพความร้อนที่ {timestamp}')

    # แสดงภาพ
    plt.show()

# พล็อตข้อมูลแต่ละแถว
for index, row in data.iterrows():
    timestamp = row[0]
    plot_thermal_image(row, timestamp)

ESP32_IP = "192.168.0.14"  # เปลี่ยนเป็น IP ของ ESP32 ของคุณ
URL = f"http://{ESP32_IP}/save"

def get_thermal_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"ข้อผิดพลาด: {response.status_code}")
        return None

def save_to_csv(data, filename="thermal_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data)

# การทำงานหลัก
data = get_thermal_data()
if data:
    save_to_csv(data)
    print("ข้อมูลถูกบันทึกลงใน CSV")
else:
    print("ไม่สามารถรับข้อมูลได้")
