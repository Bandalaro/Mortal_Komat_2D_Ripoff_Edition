import pygame
import os

class Character:
    GRAVITY = 2  # Constant gravity to apply each frame
    JUMP_STRENGTH = -15  # Negative value to move upwards

    def __init__(self, name, base_folder, screen_width, screen_height, health=100, attack_range_width=50):
        self.name = name
        self.health = health
        self.max_health = health  # Max health for the character
        self.animations = {}
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_animation = 'Idle'
        self.current_frame = 0

        # Adjust initial position to move the character down
        self.position = [screen_width // 4, screen_height - 120]  # Example: moved down from 100 to 120
        self.velocity_y = 0  # Vertical velocity (used for jumping and falling)
        self.frame_delay = 5
        self.frame_count = 0
        self.direction = 'right'
        self.is_attacking = False
        self.is_jumping = False  # Indicates if the character is jumping
        self.is_dead = False  # Indicates if the character is dead
        self.is_hurt = False  # Indicates if the character is hurt
        self.attack_frame_indices = []  # To define which frames correspond to attacks
        self.attack_range_width = attack_range_width  # The width of the attack hitbox

        self.load_animations(base_folder)
        self.width, self.height = self.animations['Idle'][0].get_size()  # Get the size of the first frame

        # Define the ground level a bit higher if needed
        self.ground_level = screen_height - 120  # Adjusted ground level to allow for the new Y position



    def load_animations(self, base_folder):
        for action_folder in os.listdir(base_folder):
            action_path = os.path.join(base_folder, action_folder)
            if os.path.isdir(action_path):
                self.animations[action_folder] = []
                for filename in sorted(os.listdir(action_path)):
                    if filename.endswith('.png') or filename.endswith('.jpg'):
                        path = os.path.join(action_path, filename)
                        image = pygame.image.load(path).convert_alpha()
                        scaled_image = pygame.transform.scale(image, (self.screen_width // 5, self.screen_height // 3))
                        self.animations[action_folder].append(scaled_image)

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_count = 0
            self.width, self.height = self.animations[animation_name][0].get_size()  # Update size when switching animations
        else:
            raise ValueError(f"Animation {animation_name} not found for character {self.name}.")

    def move(self, dx, dy):
        if not self.is_dead and not self.is_attacking:  # Prevent movement if dead or attacking
            self.position[0] += dx  # Ensure position is a list
            self.position[1] += dy

            # Ensure character doesn't go beyond the left or right screen bounds
            if self.position[0] < 0:
                self.position[0] = 0
            elif self.position[0] + self.width > self.screen_width:
                self.position[0] = self.screen_width - self.width

            # Ensure character doesn't go below the ground level
            if self.position[1] > self.ground_level:
                self.position[1] = self.ground_level
                self.velocity_y = 0  # Reset velocity if they land

            # Horizontal movement animation
            if dx != 0:
                self.set_animation('Run')
                self.direction = 'right' if dx > 0 else 'left'

    def attack(self, attack_type, damage_multiplier=1.0):
        if attack_type in self.animations and not self.is_dead and not self.is_attacking:
            self.set_animation(attack_type)
            self.is_attacking = True
            # Set attack frames and damage based on the attack type
            attack_params = {
                'Attack_One': (10, [2, 3, 4]),
                'Attack_Two': (15, [3, 4, 5]),
                'Attack_Three': (20, [1, 2, 3]),
            }
            if attack_type in attack_params:
                self.damage, self.attack_frame_indices = attack_params[attack_type]

    def is_attack_frame(self):
        return self.is_attacking and self.current_frame in self.attack_frame_indices

    def take_damage(self, damage):
        if not self.is_dead:  # No damage if already dead
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.die()  # Trigger death animation
            else:
                self.hurt()  # Trigger hurt animation

    def hurt(self):
        self.is_hurt = True
        self.set_animation('Hurt')

    def die(self):
        self.is_dead = True
        self.set_animation('Dead')

    def apply_gravity(self):
        if self.is_jumping or self.velocity_y != 0:
            self.velocity_y += self.GRAVITY  # Apply gravity to the vertical velocity
            self.position[1] += self.velocity_y  # Update character's Y position based on velocity

            # Ensure the character doesn't fall through the floor
            if self.position[1] >= self.ground_level:
                self.position[1] = self.ground_level
                self.velocity_y = 0
                self.is_jumping = False  # Stop jumping when character hits the ground

    def jump(self):
        if not self.is_jumping and not self.is_dead:  # Only jump if the character is not already in the air and not dead
            self.is_jumping = True
            self.velocity_y = self.JUMP_STRENGTH

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0
                if self.is_attacking:
                    self.is_attacking = False  # Attack sequence finished
                    self.set_animation('Idle')
                if self.is_hurt:
                    self.is_hurt = False
                    self.set_animation('Idle')

        self.apply_gravity()  # Apply gravity every frame

    def draw(self, surface):
        if self.direction == 'left':
            flipped_image = pygame.transform.flip(self.animations[self.current_animation][self.current_frame], True, False)
            surface.blit(flipped_image, self.position)
        else:
            surface.blit(self.animations[self.current_animation][self.current_frame], self.position)

    def reset(self):
        self.health = self.max_health
        self.is_dead = False
        self.is_hurt = False
        self.is_attacking = False
        self.is_jumping = False
        self.set_animation('Idle')

    def reset_position(self, default_x, default_y):
        """
        Reset the character's position to a default location.
        :param default_x: Default x position.
        :param default_y: Default y position.
        """
        self.position = [default_x, default_y]
