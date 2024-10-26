import pygame

class Controls:
    def __init__(self):
        self.keys = None
        self.gravity = 0.5  # Gravity force applied to the character when falling
        self.jump_speed = -10  # The initial upward speed when the character jumps
        self.jump_allowed = True  # To prevent double jumps
        self.attack_delay = 500  # Time delay (in ms) between attacks
        self.last_attack_time = 0  # Track time of the last attack

    def handle_player_input(self, character):
        """
        Handles movement, jumping, crouching, and attacking for the character.
        :param character: The character object that will be controlled.
        """
        self.keys = pygame.key.get_pressed()

        dx, dy = 0, character.velocity_y  # Start with the character's current vertical velocity

        # Handle horizontal movement only if not attacking
        if not character.is_attacking:
            if self.keys[pygame.K_a]:  # Move left
                dx = -5
                character.direction = 'left'  # Set direction for animations
            elif self.keys[pygame.K_d]:  # Move right
                dx = 5
                character.direction = 'right'  # Set direction for animations

        # Handle crouching
        if self.keys[pygame.K_s] and character.position[1] >= character.screen_height - character.height - 50:  # Only crouch when on the ground
            character.set_animation('Idle')  # Change animation to crouch
        else:
            if character.velocity_y == 0 and not character.is_attacking:  # Switch to Idle when on the ground and not attacking
                character.set_animation('Idle')

        # Handle jumping
        if self.keys[pygame.K_w] and self.jump_allowed and not character.is_attacking:  # Jump
            character.velocity_y = self.jump_speed
            self.jump_allowed = False
            character.set_animation('Jump')

        # Apply gravity
        character.velocity_y += self.gravity
        dy = character.velocity_y

        # Ensure character stays on the ground
        if character.position[1] + character.height >= character.screen_height - 50:  # Simulate ground at 50px from the bottom
            character.position[1] = character.screen_height - character.height - 50
            character.velocity_y = 0  # Stop vertical movement
            self.jump_allowed = True  # Allow jumping again when the character is on the ground

        # Handle attacks (Attack 1, Attack 2, and Attack 3) with delay between attacks
        current_time = pygame.time.get_ticks()
        if self.keys[pygame.K_j] and current_time - self.last_attack_time > self.attack_delay and not character.is_attacking:
            character.attack('Attack_One')
            self.last_attack_time = current_time
        elif self.keys[pygame.K_k] and current_time - self.last_attack_time > self.attack_delay and not character.is_attacking:
            character.attack('Attack_Two')
            self.last_attack_time = current_time
        elif self.keys[pygame.K_l] and current_time - self.last_attack_time > self.attack_delay and not character.is_attacking:  # Attack 3 with "L" key
            character.attack('Attack_Three')
            self.last_attack_time = current_time

        # Move the character
        character.move(dx, dy)

