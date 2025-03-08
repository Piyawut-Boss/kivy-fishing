import random # นำเข้าโมดูล random เพื่อใช้สำหรับสุ่มตำแหน่งของปลา
import pygame # นำเข้าโมดูล pygame
from boat import Boat # นำเข้าคลาส Boat จากไฟล์ boat.py
from fish import Fish, Shark  # เพิ่มการนำเข้า Shark
from fishing_line import FishLine # นำเข้าคลาส FishLine จากไฟล์ fishing_line.py
from hook import Hook # เพิ่มการนำเข้า Hook
from info_json import * # เพิ่มการนำเข้าทุกอย่างจาก info_json
from menu import show_menu  # เพิ่มการนำเข้า show_menu

# Add color constants at the top after imports
DARK_GRAY = (40, 40, 40) # เพิ่มสีเทาเข้ม
LIGHT_BLUE = (100, 200, 255) # เพิ่มสีฟ้าอ่อน
WHITE = (255, 255, 255) # เพิ่มสีขาว
ORANGE = (255, 165, 0) # เพิ่มสีส้ม
GREEN = (50, 205, 50) # เพิ่มสีเขียว

def random_fish_spawn(): # สร้างฟังก์ชันสำหรับสุ่มตำแหน่งของปลา
    x = random.randrange(100, 1080) # สุ่มตำแหน่ง x ของปลา
    y = random.randrange(300, 600) # สุ่มตำแหน่ง y ของปลา
    return x, y # ส่งค่า x และ y กลับ

def spawn_fish(fish_type=None): # สร้างฟังก์ชันสำหรับสร้างปลา
    if fish_type is None: # ถ้าประเภทของปลาไม่ได้ระบุ
        fish_type = random.choice(["fish", "shark"]) # สุ่มประเภทของปลา
    x_pos, y_pos = random_fish_spawn() # สุ่มตำแหน่งของปลา

    return Fish(x_pos, y_pos) if fish_type == "fish" else Shark(x_pos, y_pos) # สร้างปลาประเภท common หรือปลาประเภท shark แล้วส่งกลับ

json_data = read_json() # อ่านข้อมูลจากไฟล์ JSON
SIZE = (1080, 720) # กำหนดขนาดหน้าจอ
pygame.init() # เริ่มต้นใช้งาน pygame
screen = pygame.display.set_mode(SIZE) # สร้างหน้าต่างแสดงผลขนาด 1080x720

background = pygame.image.load("images/background.png") # โหลดภาพพื้นหลัง
background = pygame.transform.scale(background, SIZE)  # ปรับขนาดให้พอดีกับหน้าจอ (1080, 720)

boat = Boat() # สร้างเรือ

fishes = [] # สร้างลิสต์เก็บปลา
# Initialize fish counts
fish_counts = {"fish": 0, "shark": 0}

# Adjust initial fish spawning to keep track of counts
for _ in range(5): # วนลูป 5 รอบ
    fish = spawn_fish()
    fishes.append(fish)
    if isinstance(fish, Fish):
        fish_counts["fish"] += 1
    else:
        fish_counts["shark"] += 1

fisherman_line = FishLine(boat) # สร้างเส้นตกปลาจากเรือ
hook = Hook(boat) # สร้างเบ็ด

left_picture_boat, right_picture_boat = boat.load_boat() # โหลดภาพเรือ
left_picture_fish, right_picture_fish = fishes[0].load_pictures()  # We can use any fish instance to load pictures

boat_look_direction = left_picture_boat # กำหนดทิศทางของเรือเริ่มต้นเป็นซ้าย
fish_directions = [left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish for fish in fishes] # กำหนดทิศทางของปลา

"""On screen shits""" # แสดงผลบนหน้าจอ
font = pygame.font.Font(None, 30) # สร้างฟอนต์ขนาด 30 
caught_fishes_count = 0 # กำหนดจำนวนปลาที่ถูกจับเป็น 0 ตั้งแต่เริ่มต้น
# Remove fps calculation
# ------------------------
fish_hitbox = pygame.Rect((fishes[0].x_pos, fishes[0].y_pos, 0, 0))  # NOQA
hook_hitbox = pygame.Rect((fisherman_line.tip_of_the_rod, hook.y_pos, 0, 0))  # NOQA
# caught_fish ---------------
caught_fish = pygame.image.load("images/fish_1_left.png") # โหลดภาพปลาที่ถูกจับ
caught_fish = pygame.transform.scale(caught_fish, (80, 50)) # ปรับขนาดภาพปลาที่ถูกจับ
caught_fish = pygame.transform.rotate(caught_fish, -90) # หมุนภาพปลาที่ถูกจับ
# ----------------------------

# Add a timer to display elapsed time
start_ticks = pygame.time.get_ticks() # นับเวลาเริ่มต้น

running = True # กำหนด running เป็น True เพื่อให้โปรแกรมทำงาน
is_fish_caught = False # กำหนด is_fish_caught เป็น False เพื่อให้ปลาไม่ถูกจับ
caught_fish_index = None # กำหนด caught_fish_index เป็น None เพื่อให้ปลาไม่ถูกจับ

# Display the menu first
menu_action = show_menu(screen)  # แสดงเมนู
if menu_action == "start": # ถ้าผู้เล่นเลือกเริ่มเกม
    while running: # วนลูปเมื่อ running เป็น True
        pygame.time.Clock().tick(60) # กำหนด FPS ให้เป็น 60
        screen.blit(background, (0, 0)) # แสดงภาพพื้นหลัง
        
        # Calculate seconds
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000 # นับเวลาทีเมื่อเริ่มเกม

        # Draw stats directly without FPS
        text_fish = font.render(f"Fish: {boat.caught_fishes}", True, WHITE) # แสดงจำนวนปลาที่ถูกจับ
        text_record = font.render(f"Record: {json_data['best_result']}", True, WHITE) # แสดงคะแนนสูงสุด
        text_time = font.render(f"Time: {seconds}s", True, WHITE) # แสดงเวลาที่ใช้
        
        # Adjust positions (removed FPS, moved others left)
        screen.blit(text_fish, (10, 10)) # แสดงจำนวนปลาที่ถูกจับ
        screen.blit(text_record, (160, 10)) # แสดงคะแนนสูงสุด
        screen.blit(text_time, (310, 10)) # แสดงเวลาที่ใช้

        for event in pygame.event.get(): # วนลูปเมื่อมีการเกิดเหตุการณ์
            if event.type == pygame.QUIT: # ถ้าเกิดการปิดหน้าต่าง
                running = False # หยุดการทำงาน
            if event.type == pygame.KEYDOWN: # ถ้ามีการกดปุ่ม 
                if event.key == pygame.K_SPACE: # ถ้ากดปุ่ม SPACE
                    hook.is_hook_moving = True # เปลี่ยนค่า is_hook_moving เป็น True

        if (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[ # ถ้ากดปุ่ม A
            pygame.K_LEFT]) and not hook.is_hook_moving:  # NOQA
            boat.move_left() # เรือเคลื่อนที่ไปทางซ้าย
            fisherman_line.rotate_fisherman_left() # หมุนเส้นตกปลาไปทางซ้าย
            boat_look_direction = left_picture_boat # กำหนดทิศทางของเรือเป็นซ้าย
        elif (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and not hook.is_hook_moving: # ถ้ากดปุ่ม D
            boat.move_right(SIZE[0]) # เรือเคลื่อนที่ไปทางขวา
            fisherman_line.rotate_fisherman_right() # หมุนเส้นตกปลาไปทางขวา
            boat_look_direction = right_picture_boat # กำหนดทิศทางของเรือเป็นขวา

        seconds = pygame.time.get_ticks() // 1000  # NOQA

        transparent_surface = pygame.Surface((1600, 900)) # สร้างพื้นผิวโปร่งใสขนาด 1600x900
        hook_hitbox.x, hook_hitbox.y = fisherman_line.tip_of_the_rod - 10, hook.y_pos # กำหนดตำแหน่งของ hitbox ของเบ็ด
        hook_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (hook_hitbox.x, hook_hitbox.y, 17, 33), 1) # วาด hitbox ของเบ็ด

        if not is_fish_caught: # ถ้าปลาไม่ถูกจับ
            for i, fish in enumerate(fishes): # วนลูปเมื่อมีการเลี้ยงปลา
                fish_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (fish.x_pos, fish.y_pos + 27, 120, 40), 1) # วาด hitbox ของปลา
                if fish_directions[i] == left_picture_fish: # ถ้าทิศทางของปลาเป็นซ้าย
                    fish.swim_left(seconds, fish_hitbox) # ปลาว่ายไปทางซ้าย
                    if fish.check_left_wall(): # ถ้าปลาชนขอบซ้าย
                        fish_directions[i] = right_picture_fish # กำหนดทิศทางของปลาเป็นขวา
                elif fish_directions[i] == right_picture_fish: # ถ้าทิศทางของปลาเป็นขวา
                    fish.swim_right(seconds, fish_hitbox) # ปลาว่ายไปทางขวา
                    screen_width = SIZE[0] # กำหนดความกว้างของหน้าจอ
                    if fish.check_right_wall(screen_width): # ถ้าปลาชนขอบขวา
                        fish_directions[i] = left_picture_fish # กำหนดทิศทางของปลาเป็นซ้าย
                fish_image = fish.right_image if fish_directions[i] == right_picture_fish else fish.left_image # กำหนดภาพของปลา
                screen.blit(fish_image, (fish.x_pos, fish.y_pos)) # แสดงภาพปลา
                
                # Update hitbox for each fish and check collision
                fish_hitbox = pygame.Rect((fish.x_pos, fish.y_pos + 27, 120, 40)) # อัพเดท hitbox ของปลา
                if fish_hitbox.colliderect(hook_hitbox_draw): # ถ้า hitbox ของปลาชนกับ hitbox ของเบ็ด
                    is_fish_caught = True # กำหนดให้ปลาถูกจับ
                    caught_fish_index = i  # กำหนดค่า index ของปลาที่ถูกจับ
                    break # ออกจากลูป

            line = pygame.Rect((fisherman_line.tip_of_the_rod, boat.y + 17, 1, fisherman_line.advance_line)) # สร้างเส้นตกปลา
            if not hook.is_hook_moving: # ถ้าเบ็ดไม่เคลื่อนที่
                pygame.draw.rect(screen, (255, 0, 0), line) # วาดเส้นตกปลา
            else: # ถ้าเบ็ดเคลื่อนที่
                if not hook.bottom_reached: # ถ้าเบ็ดยังไม่ชนด้านล่าง
                    hook.drop_hook() # ให้เบ็ดตกลง
                elif hook.bottom_reached: # ถ้าเบ็ดชนด้านล่าง
                    hook.get_hook_back(fisherman_line) # ให้เบ็ดยกขึ้นมา

                pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17), 
                                 (fisherman_line.tip_of_the_rod, hook.y_pos)) # วาดเส้นตกปลา

        pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                         (fisherman_line.tip_of_the_rod, hook.y_pos)) # วาดเส้นตกปลา
        if is_fish_caught:
            if caught_fish_index is not None and 0 <= caught_fish_index < len(fishes): # ตรวจสอบว่า index ของปลาถูกจับอยู่ในช่วงของลิสต์ปลาหรือไม่
                caught_fish = fishes[caught_fish_index].left_image  # หรือ right_image ตามทิศทาง
                caught_fish_rotated = pygame.transform.rotate(caught_fish, -90)  # หมุนปลาหัวขึ้น
                screen.blit(caught_fish_rotated, (hook_hitbox.x - 23, hook_hitbox.y + 20))
            hook.caught_fish(fisherman_line) # เบ็ดจับปลา
            if hook.is_caught: # ถ้าเบ็ดจับปลาได้
                fishes[caught_fish_index].increase_speed_fish_after_caught() # เพิ่มความเร็วของปลาหลังจับ
                boat.caught_fish() 

                # Update fish counts
                if isinstance(fishes[caught_fish_index], Fish):
                    fish_counts["fish"] -= 1
                else:
                    fish_counts["shark"] -= 1

                # แทนที่ปลาตัวที่ถูกจับด้วยตัวใหม่
                if caught_fish_index is not None and 0 <= caught_fish_index < len(fishes):
                    new_fish_type = "shark" if fish_counts["shark"] < 2 else "fish"
                    new_fish = spawn_fish(new_fish_type)
                    fishes[caught_fish_index] = new_fish
                    fish_counts[new_fish_type] += 1

                is_fish_caught = False 
                caught_fish_index = None  # รีเซ็ตค่าให้พร้อมสำหรับรอบต่อไป
                hook.fix_bug_fishing_every_second_time() # แก้บัคการตกปลาทุกๆครั้งที่เริ่มต้นเกมใหม่

        # Add a game over condition when a certain number of fish are caught
        if boat.caught_fishes >= 10: # ถ้าจำนวนปลาที่ถูกจับมากกว่าหรือเท่ากับ 10
            game_over_text = font.render("Game Over! You Win!", True, (255, 0, 0)) # แสดงข้อความ Game Over! You Win!
            screen.blit(game_over_text, (SIZE[0] // 2 - 100, SIZE[1] // 2)) # แสดงข้อความ Game Over! You Win!
            pygame.display.flip() # แสดงผลบนหน้าจอ
            pygame.time.wait(3000) # หยุดการทำงานเป็นเวลา 3 วินาที
            running = False # หยุดการทำงาน

        screen.blit(boat_look_direction, (boat.x, boat.y)) # แสดงภาพเรือ
        """
        fisherman_line.tip_of_the_rod - 10 === hook knot position
        hook.y_pos if hook.is_hook_moving else fisherman_line.advance_line + 62
        hook.y_pos is the dynamic value
        boat.y + 160 is the value from the dynamically generated float boating
        """
        screen.blit(hook.picture, (fisherman_line.tip_of_the_rod - 10, # แสดงภาพเบ็ด
                                   hook.y_pos if hook.is_hook_moving else boat.y + 160)) # แสดงภาพเบ็ด

        pygame.display.flip() # แสดงผลบนหน้าจอ

# เมื่อการเล่นเสร็จสิ้น, บันทึกข้อมูล
save_on_close(json_data, boat.caught_fishes) # บันทึกข้อมูลเมื่อปิดโปรแกรม
pygame.quit() # หยุดใช้งาน pygame