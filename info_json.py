import json # นำเข้าโมดูล json เพื่อใช้ในการจัดการข้อมูล json


def read_json(): # ฟังก์ชัน read_json ใช้ในการอ่านข้อมูลจากไฟล์ json
    with open("fishing_info.json", "a+") as file: # เปิดไฟล์ fishing_info.json ในโหมดการเขียนและการอ่าน
        try: # ใช้ try เพื่อจัดการข้อผิดพลาด
            file.seek(0) # ใช้ seek เพื่อกลับไปที่ตำแหน่ง 0
            take_from_file = json.load(file) # ใช้ json.load เพื่ออ่านข้อมูลจากไฟล์
        except: # ถ้าเกิดข้อผิดพลาด
            return app_information # ส่งค่า app_information กลับ
    return take_from_file # ส่งค่า take_from_file กลับ


def save_on_close(program_data, current_fishes): # ฟังก์ชัน save_on_close ใช้ในการบันทึกข้อมูลเมื่อปิดโปรแกรม
    if program_data["best_result"] <= current_fishes: # ถ้าค่า best_result ในไฟล์น้อยกว่าหรือเท่ากับค่า current_fishes
        program_data["best_result"] = current_fishes # กำหนดค่า best_result ในไฟล์เป็นค่า current_fishes
        with open('fishing_info.json', 'w') as data: # เปิดไฟล์ fishing_info.json ในโหมดการเขียน
            json.dump(program_data, data, indent=2) # ใช้ json.dump เพื่อบันทึกข้อมูลลงไฟล์


app_information = { # สร้างดิกชันนารี app_information เพื่อเก็บข้อมูลเริ่มต้นของโปรแกรม
    "best_result": 0,
}
