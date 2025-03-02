import random
import pygame
from boat import Boat
from fish import Fish
from fishing_line import FishLine
from hook import Hook
from info_json import *

# Add color constants at the top after imports
DARK_GRAY = (40, 40, 40)
LIGHT_BLUE = (100, 200, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (50, 205, 50)

# Add new colors for menu
MENU_BLUE = (65, 105, 225)
MENU_WHITE = (255, 255, 255)
MENU_HOVER = (100, 149, 237)

def random_fish_spawn():
    x = random.randrange(100, 1080)
    y = random.randrange(300, 720)
    return x, y


json_data = read_json()
SIZE = (1080, 720)
pygame.init()
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background,(10000,900))

boat = Boat()

fishes = []
for _ in range(5):
    x_spawn, y_spawn = random_fish_spawn()
    fishes.append(Fish(x_spawn, y_spawn))

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

def draw_menu_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, MENU_WHITE)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

# Add menu loop before main game
def show_menu():
    menu_running = True
    while menu_running:
        screen.blit(background, (0, 0))
        
        # Draw title
        title_font = pygame.font.Font(None, 74)
        title = title_font.render("Fisherman", True, MENU_WHITE)
        screen.blit(title, (SIZE[0]//2 - title.get_width()//2, 200))

        # Create buttons
        play_button = draw_menu_button(screen, "Play", SIZE[0]//2 - 100, 350, 200, 50, MENU_BLUE)
        quit_button = draw_menu_button(screen, "Quit", SIZE[0]//2 - 100, 450, 200, 50, MENU_BLUE)

        # Handle mouse hover
        mouse_pos = pygame.mouse.get_pos()
        if play_button.collidepoint(mouse_pos):
            draw_menu_button(screen, "Play", SIZE[0]//2 - 100, 350, 200, 50, MENU_HOVER)
        if quit_button.collidepoint(mouse_pos):
            draw_menu_button(screen, "Quit", SIZE[0]//2 - 100, 450, 200, 50, MENU_HOVER)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    return False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Add menu before main game loop
should_start_game = show_menu()
running = should_start_game

is_fish_caught = False
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
        fisherman_line.rotate_fisherman_left(boat)
        boat_look_direction = left_picture_boat
    elif (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and not hook.is_hook_moving:
        boat.move_right(SIZE[0])
        fisherman_line.rotate_fisherman_right(boat)
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
            fish_image = screen.blit(fish_directions[i], (fish.x_pos, fish.y_pos))
            
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
        screen.blit(caught_fish, (hook_hitbox.x - 23, hook_hitbox.y + 20))
        hook.caught_fish(fisherman_line)
        if hook.is_caught:
            fishes[caught_fish_index].increase_speed_fish_after_caught()
            boat.caught_fish()
            is_fish_caught = False
            hook.fix_bug_fishing_every_second_time()
            x_spawn, y_spawn = random_fish_spawn()
            fishes[caught_fish_index].x_pos, fishes[caught_fish_index].y_pos = x_spawn, y_spawn

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
pygame.quit()
save_on_close(json_data, boat.caught_fishes)