coins = 0  # ตัวแปรเก็บจำนวนเหรียญ

def add_coins(amount):
    global coins
    coins += amount  # เพิ่มเหรียญ

def get_coins():
    return coins  # คืนค่าจำนวนเหรียญทั้งหมด
