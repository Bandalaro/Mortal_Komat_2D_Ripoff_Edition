import pygame
import numpy as np
from environment import Environment
from Utils.Selection import selection_flow
from Mech.Controls import Controls
from Character.character import Character
from Mech.Battle_AI import BattleAI
from Mech.BattleMechanics import BattleMechanics
from Extras.Title_Screen import show_title_screen  # Ensure correct path

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fighting Game')

# Show the title screen before the game starts
if not show_title_screen(screen):  # Pass screen to title screen
    pygame.quit()
    quit()

# Initialize environment with the base folder and screen dimensions
base_folder = 'Assets/Background'
environment = Environment(base_folder, screen_width, screen_height)

# Load characters data
characters_data = {
    'Fighter': 'Assets/Characters/Fighter',
    'Shinobi': 'Assets/Characters/Shinobi',
    'Archer': 'Assets/Characters/Archer',
}

# Selection flow: Select a background and a character for the player
selected_background, selected_character_data = selection_flow(environment, characters_data, screen, screen_width, screen_height)

# Set the selected background
environment.set_background_set(selected_background)

# Create the selected player character
player_character = Character(
    name=selected_character_data['name'],
    base_folder=selected_character_data['base_folder'],
    screen_width=screen_width,
    screen_height=screen_height
)

# Set initial player position (left side)
player_character.position = np.array([100, screen_height])  # Example: 100px from left, close to ground

# Define parameters for BattleAI
state_size = 10  # Number of features for state representation
action_size = 6  # Number of possible actions for the AI
character_names = list(characters_data.keys())  # AI character options

# Initialize AI agent
ai_agent = BattleAI(character_names, state_size, action_size, screen_width, screen_height)

# Select and load AI character based on player's position
ai_character = ai_agent.select_character(player_character.position)

# Set initial AI position (right side of the screen)
ai_character.position = np.array([screen_width - 200, screen_height])  # Example: 200px from right, close to ground

# Initialize battle mechanics
battle_mechanics = BattleMechanics(screen_width, screen_height)

# Game loop
running = True
clock = pygame.time.Clock()

# Game control logic (using a separate class for player controls)
controls = Controls()  # Assuming this handles the player's movement, jump, and attack inputs

while running:
    screen.fill((0, 0, 0))  # Clear screen to avoid frame artifacts
    environment.draw(screen)  # Draw the background

    # Handle player inputs
    controls.handle_player_input(player_character)  # Process player controls

    # AI logic
    state = ai_agent.update_state(player_character)  # AI state update based on player and AI positions
    ai_agent.rational_behavior(player_character)  # AI takes an action based on its state

    # Apply gravity to both player and AI
    player_character.apply_gravity()  # Apply gravity to player character
    ai_agent.apply_gravity()  # Apply gravity to AI character

    # Update player and AI characters
    player_character.update()
    ai_character.update()

    # Ensure both characters stay within screen bounds
    environment.constrain_character_position(player_character)
    environment.constrain_character_position(ai_character)

    # Update battle mechanics (health reduction, attack checks)
    battle_mechanics.update(player_character, ai_character)

    # Check for collisions (attacks, positions)
    if battle_mechanics.check_attack_collision(player_character, ai_character):
        ai_character.take_damage(1)  # AI takes damage if hit
    if battle_mechanics.check_attack_collision(ai_character, player_character):
        player_character.take_damage(1)  # Player takes damage if hit

    # Draw player and AI characters
    player_character.draw(screen)
    ai_character.draw(screen)

    # Draw health bars
    battle_mechanics.draw_health_bar(screen, player_character, ai_character, 20)

    # Update display
    pygame.display.flip()

    # Event handling (closing the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control the frame rate
    clock.tick(60)

# Exit Pygame
pygame.quit()
