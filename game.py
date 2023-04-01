import pygame
import random

pygame.init()

# Set up the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

background_music = pygame.mixer.music.load('backgroundmusic.mp3')
score_sound = pygame.mixer.Sound('coincatch.wav')

# Set up the game objects
player_x = screen_width // 2
player_y = screen_height // 2
player_speed = 0.3
player_size = 40
player_image = pygame.image.load(f'sprites/wnv2_lf1.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))

sprite_images = []
for i in range(1, 2):
    sprite_image = pygame.image.load(f'sprites/wnv2_lf{i}.png')
    sprite_image = pygame.transform.scale(
        sprite_image, (player_size, player_size))
    sprite_images.append(sprite_image)

sprite_index = 0
sprite_timer = 0
sprite_delay = 5

coin_x = random.randint(0, screen_width)
coin_y = random.randint(0, screen_height)
coin_size = 30
coin_image = pygame.image.load('coin.png')
coin_image_small = pygame.transform.scale(coin_image, (20, 20))
coin_image = pygame.transform.scale(coin_image, (coin_size, coin_size))

enemy_x = random.randint(0, screen_width)
enemy_y = random.randint(0, screen_height)
enemy_speed = 0.04
enemy_size = 40
enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

score = 0
font = pygame.font.Font(None, 30)

# Set up the game loop
game_state = "playing"
game_over_text = font.render("Failed to call police", True, (255, 0, 0))
game_over_text_rect = game_over_text.get_rect(
    center=(screen_width/2, screen_height/2))
running = True
pygame.mixer.music.play(-1)
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            pygame.mixer.music.stop()
            quit()

        if game_state == "win":
            screen.fill((0, 0, 139))  # Fill the screen with dark blue color
            win_text = font.render(
                "Police is here, Good Job", True, (255, 255, 255))
            win_text_rect = win_text.get_rect(
                center=(screen_width/2, screen_height/2))
            screen.blit(win_text, win_text_rect)

            restart_text = font.render(
                "Press R to restart", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(
                center=(screen_width/2, screen_height/2 + 50))
            screen.blit(restart_text, restart_text_rect)

            pygame.display.update()

            # Wait for the player to press the R key
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        pygame.mixer.music.stop()
                        quit()
                    # check if the event in R key
                    if event.key == pygame.K_r:
                        # Restart the game
                        game_state = "playing"
                        score = 0
                        # Add your code to reset the game here
                        break
                    if event.key == pygame.K_q:
                        quit()
                else:
                    continue
                break

        if game_state == "game over":
            # Show the game over text
            screen.fill((0, 0, 0))  # Fill the screen with black color
            screen.blit(game_over_text, game_over_text_rect)
            restart_text = font.render(
                "Press R to restart", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(
                center=(screen_width/2, screen_height/2 + 50))
            screen.blit(restart_text, restart_text_rect)
            pygame.display.update()

            # Wait for the player to click the mouse button
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        pygame.mixer.music.stop()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        # Restart the game
                        game_state = "playing"
                        score = 0
                        # Add your code to reset the game here
                        player_x = screen_width / 2
                        player_y = screen_height / 2
                        coin_x = random.randint(0, screen_width)
                        coin_y = random.randint(0, screen_height)
                        enemy_x = random.randint(0, screen_width)
                        enemy_y = random.randint(0, screen_height)
                        break
                else:
                    continue
                break

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
        player_y += player_speed

    # Update sprite animation
    sprite_timer += 1
    if sprite_timer >= sprite_delay:
        sprite_timer = 0
        sprite_index = (sprite_index + 1) % len(sprite_images)
        pygame.display.update()


    sprite_image = sprite_images[sprite_index]
    screen.blit(sprite_image, (player_x, player_y))
    screen.blit(sprite_images[sprite_index], (player_x, player_y))


    # Update game state
    coin_distance = ((coin_x - player_x)**2 + (coin_y - player_y)**2)**0.5
    if coin_distance < player_size + coin_size:
        score_sound.play()
        score += 1
        coin_x = random.randint(0, screen_width)
        coin_y = random.randint(0, screen_height)

    enemy_dx = player_x - enemy_x
    enemy_dy = player_y - enemy_y
    enemy_dist = ((enemy_dx)**2 + (enemy_dy)**2)**0.5
    enemy_vx = enemy_speed * enemy_dx / enemy_dist
    enemy_vy = enemy_speed * enemy_dy / enemy_dist
    enemy_x += enemy_vx
    enemy_y += enemy_vy

    if coin_x < 0 or coin_x > screen_width or coin_y < 0 or coin_y > screen_height:
        coin_x = random.randint(0, screen_width)
        coin_y = random.randint(0, screen_height)

    if enemy_x < 0 or enemy_x > screen_width or enemy_y < 0 or enemy_y > screen_height:
        enemy_x = random.randint(0, screen_width)
        enemy_y = random.randint(0, screen_height)

    # Check if the enemy has caught the player
    enemy_distance = ((enemy_x - player_x)**2 + (enemy_y - player_y)**2)**0.5
    if enemy_distance < enemy_size + player_size:
        game_state = "game over"

    if score == 10:
        game_state = "win"

    # Draw game objects
    screen.fill((0, 0, 0))
    score_text = font.render(f" {score}", True, (255, 255, 255))
    screen.blit(score_text, (40, 10))
    screen.blit(coin_image_small, (10, 10))
    coin_text = coin_image.copy()
    score_coin_image = pygame.Surface((score_text.get_width(
    ) + coin_text.get_width() + 10, max(score_text.get_height(), coin_text.get_height())))
    score_coin_image.fill((0, 0, 0))
    score_coin_image.blit(score_text, (0, 0))
    score_coin_image.blit(coin_text, (score_text.get_width() + 10, 0))

    # Draw the score and coin image
    screen.blit(coin_image, (coin_x, coin_y))
    screen.blit(enemy_image, (int(enemy_x), int(enemy_y)))
    screen.blit(player_image, (player_x, player_y))
    pygame.display.update()

pygame.quit()
