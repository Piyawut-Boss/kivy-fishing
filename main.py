import random
import pygame
from boat import Boat
from fish import Fish, Shark  # เพิ่มการนำเข้า Shark
from fishing_line import FishLine
from hook import Hook
from info_json import *
from menu import show_menu  # เพิ่มการนำเข้า show_menu

# Add color constants at the top after imports
DARK_GRAY = (40, 40, 40)
LIGHT_BLUE = (100, 200, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (50, 205, 50)

def random_fish_spawn():
    x = random.randrange(100, 1080)
    y = random.randrange(300, 720)
    return x, y

def spawn_fish(fish_type=None):
    if fish_type is None:
        fish_type = random.choice(["fish", "shark"])
    x_pos, y_pos = random_fish_spawn()

    return Fish(x_pos, y_pos) if fish_type == "fish" else Shark(x_pos, y_pos)

json_data = read_json()
SIZE = (1080, 720)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (10000, 900))

boat = Boat()

fishes = []
for _ in range(5):
    fishes.append(spawn_fish())

fisherman_line = FishLine(boat)
hook = Hook(boat)

left_picture_boat, right_picture_boat = boat.load_boat()
left_picture_fish, right_picture_fish = fishes[0].load_pictures()  # We can use any fish instance to load pictures

boat_look_direction = left_picture_boat
fish_directions = [left_picture_fish if fish.x_pos <= SIZE[0] // 2 else right_picture_fish for fish in fishes]

"""On screen shits"""
font = pygame.font.Font(None, 30)
caught_fishes_count = 0
# Remove fps calculation
# ------------------------
fish_hitbox = pygame.Rect((fishes[0].x_pos, fishes[0].y_pos, 0, 0))  # NOQA
hook_hitbox = pygame.Rect((fisherman_line.tip_of_the_rod, hook.y_pos, 0, 0))  # NOQA
# caught_fish ---------------
caught_fish = pygame.image.load("images/fish_1_left.png")
caught_fish = pygame.transform.scale(caught_fish, (80, 50))
caught_fish = pygame.transform.rotate(caught_fish, -90)
# ----------------------------

# Add a timer to display elapsed time
start_ticks = pygame.time.get_ticks()

running = True
is_fish_caught = False
caught_fish_index = None

# Display the menu first
menu_action = show_menu(screen)  # แสดงเมนู
if menu_action == "start":
    while running:
        pygame.time.Clock().tick(60)
        screen.blit(background, (0, 0))
        
        # Calculate seconds
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        # Draw stats directly without FPS
        text_fish = font.render(f"Fish: {boat.caught_fishes}", True, WHITE)
        text_record = font.render(f"Record: {json_data['best_result']}", True, WHITE)
        text_time = font.render(f"Time: {seconds}s", True, WHITE)
        
        # Adjust positions (removed FPS, moved others left)
        screen.blit(text_fish, (10, 10))
        screen.blit(text_record, (160, 10))
        screen.blit(text_time, (310, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hook.is_hook_moving = True

        if (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[
            pygame.K_LEFT]) and not hook.is_hook_moving:  # NOQA
            boat.move_left()
            fisherman_line.rotate_fisherman_left()
            boat_look_direction = left_picture_boat
        elif (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and not hook.is_hook_moving:
            boat.move_right(SIZE[0])
            fisherman_line.rotate_fisherman_right()
            boat_look_direction = right_picture_boat

        seconds = pygame.time.get_ticks() // 1000  # NOQA

        transparent_surface = pygame.Surface((1600, 900))
        hook_hitbox.x, hook_hitbox.y = fisherman_line.tip_of_the_rod - 10, hook.y_pos
        hook_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (hook_hitbox.x, hook_hitbox.y, 17, 33), 1)

        if not is_fish_caught:
            for i, fish in enumerate(fishes):
                fish_hitbox_draw = pygame.draw.rect(transparent_surface, (0, 0, 0), (fish.x_pos, fish.y_pos + 27, 120, 40), 1)
                if fish_directions[i] == left_picture_fish:
                    fish.swim_left(seconds, fish_hitbox)
                    if fish.check_left_wall():
                        fish_directions[i] = right_picture_fish
                elif fish_directions[i] == right_picture_fish:
                    fish.swim_right(seconds, fish_hitbox)
                    screen_width = SIZE[0]
                    if fish.check_right_wall(screen_width):
                        fish_directions[i] = left_picture_fish
                fish_image = fish.right_image if fish_directions[i] == right_picture_fish else fish.left_image
                screen.blit(fish_image, (fish.x_pos, fish.y_pos))
                
                # Update hitbox for each fish and check collision
                fish_hitbox = pygame.Rect((fish.x_pos, fish.y_pos + 27, 120, 40))
                if fish_hitbox.colliderect(hook_hitbox_draw):
                    is_fish_caught = True
                    caught_fish_index = i
                    break

            line = pygame.Rect((fisherman_line.tip_of_the_rod, boat.y + 17, 1, fisherman_line.advance_line))
            if not hook.is_hook_moving:
                pygame.draw.rect(screen, (255, 0, 0), line)
            else:
                if not hook.bottom_reached:
                    hook.drop_hook()
                elif hook.bottom_reached:
                    hook.get_hook_back(fisherman_line)

                pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                                 (fisherman_line.tip_of_the_rod, hook.y_pos))

        pygame.draw.line(screen, (255, 0, 0), (fisherman_line.tip_of_the_rod, boat.y + 17),
                         (fisherman_line.tip_of_the_rod, hook.y_pos))
        if is_fish_caught:
            if caught_fish_index is not None and 0 <= caught_fish_index < len(fishes):
                caught_fish = fishes[caught_fish_index].left_image  # หรือ right_image ตามทิศทาง
                caught_fish_rotated = pygame.transform.rotate(caught_fish, -90)  # หมุนปลาหัวขึ้น
                screen.blit(caught_fish_rotated, (hook_hitbox.x - 23, hook_hitbox.y + 20))
            hook.caught_fish(fisherman_line)
            if hook.is_caught:
                fishes[caught_fish_index].increase_speed_fish_after_caught()
                boat.caught_fish()

                # แทนที่ปลาตัวที่ถูกจับด้วยตัวใหม่
                if caught_fish_index is not None and 0 <= caught_fish_index < len(fishes):
                    fishes[caught_fish_index] = spawn_fish("shark" if isinstance(fishes[caught_fish_index], Shark) else "fish")

                is_fish_caught = False
                caught_fish_index = None  # รีเซ็ตค่าให้พร้อมสำหรับรอบต่อไป
                hook.fix_bug_fishing_every_second_time()

        # Add a game over condition when a certain number of fish are caught
        if boat.caught_fishes >= 10:
            game_over_text = font.render("Game Over! You Win!", True, (255, 0, 0))
            screen.blit(game_over_text, (SIZE[0] // 2 - 100, SIZE[1] // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        screen.blit(boat_look_direction, (boat.x, boat.y))
        """
        fisherman_line.tip_of_the_rod - 10 === hook knot position
        hook.y_pos if hook.is_hook_moving else fisherman_line.advance_line + 62
        hook.y_pos is the dynamic value
        boat.y + 160 is the value from the dynamically generated float boating
        """
        screen.blit(hook.picture, (fisherman_line.tip_of_the_rod - 10,
                                   hook.y_pos if hook.is_hook_moving else boat.y + 160))

        pygame.display.flip()

# เมื่อการเล่นเสร็จสิ้น, บันทึกข้อมูล
save_on_close(json_data, boat.caught_fishes)
pygame.quit()