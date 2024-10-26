# title_screen.py
import pygame
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Function to draw the title screen
def draw_title_screen(screen):
    screen.fill(BLACK)  # Fill the background with black

    font = pygame.font.Font(None, 74)
    title_text = font.render("Fighting Game", True, WHITE)
    screen.blit(title_text, (200, 250))  # Center the text

    font = pygame.font.Font(None, 36)
    prompt_text = font.render("Press any button to start", True, WHITE)
    screen.blit(prompt_text, (220, 350))  # Prompt for start

    pygame.display.flip()


# Function to display the title screen
def show_title_screen(screen):
    running = True
    draw_title_screen(screen)  # Render the title screen

    # Wait for a button press to exit the title screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit if the user closes the window
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return True  # Exit the title screen when any key/button is pressed

        pygame.display.update()

    return True  # Move forward to the main game

# Uncomment this if you are using a video
# def get_video_frame(player):
#     """Retrieves the next frame of the video."""
#     frame, val = player.get_frame()
#     if val == 'eof':
#         return None, val
#     elif frame is not None:
#         img, t = frame
#         img = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), 'RGB')
#         return img, val
#     return None, val

pygame.quit()
