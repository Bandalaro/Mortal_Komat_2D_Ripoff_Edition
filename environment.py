import pygame
import os

class Environment:
    def __init__(self, base_folder, screen_width, screen_height):
        """
        Initialize the environment by loading and scaling all static background environments from the specified folders.

        :param base_folder: Path to the base folder containing subfolders with background layers.
        :param screen_width: The width of the Pygame window.
        :param screen_height: The height of the Pygame window.
        """
        self.background_sets = []  # Stores sets of layers for different environments
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.load_environments(base_folder)  # Load environments from the given base folder
        self.current_set = 0  # Default to the first background set

    def load_environments(self, base_folder):
        """
        Load environments from subfolders, where each subfolder contains layers of a single environment.

        :param base_folder: The path to the base folder containing all environment subfolders.
        """
        for subfolder in os.listdir(base_folder):
            subfolder_path = os.path.join(base_folder, subfolder)
            if os.path.isdir(subfolder_path):
                layers = []
                # Sort files to ensure correct layer order and load images
                for filename in sorted(os.listdir(subfolder_path)):
                    if filename.endswith('.png') or filename.endswith('.jpg'):
                        path = os.path.join(subfolder_path, filename)
                        image = pygame.image.load(path).convert_alpha()
                        # Scale the image to the screen size
                        scaled_image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
                        layers.append(scaled_image)
                # Append valid layers as a set
                if layers:
                    self.background_sets.append(layers)

    def set_background_set(self, set_index):
        """
        Change to a different set of environments based on the index provided.

        :param set_index: Index of the environment set to switch to.
        """
        if 0 <= set_index < len(self.background_sets):
            self.current_set = set_index  # Set to the specified index if valid
        else:
            raise IndexError("Environment set index out of range. Please provide a valid index.")

    def draw(self, screen):
        """
        Draw the current environment onto the screen.

        :param screen: Pygame surface to draw the environment on.
        """
        # Draw each layer in the current background set
        for layer in self.background_sets[self.current_set]:
            screen.blit(layer, (0, 0))

    def constrain_character_position(self, character):
        """
        Constrain the character's position within the environment bounds to prevent them from going off-screen.
        :param character: The character object whose position will be constrained.
        """
        lower_bound = self.screen_height - character.height

        # Constrain vertical position
        if character.position[1] < 0:  # Top boundary
            character.position[1] = 0
        elif character.position[1] > lower_bound:  # Bottom boundary
            character.position[1] = lower_bound

        # Constrain horizontal position
        if character.position[0] < 0:  # Left boundary
            character.position[0] = 0
        elif character.position[0] > self.screen_width - character.width:  # Right boundary
            character.position[0] = self.screen_width - character.width
    def next_background_set(self):
        """
        Switch to the next background set. If at the end of the list, loop back to the first set.
        """
        self.current_set = (self.current_set + 1) % len(self.background_sets)

    def previous_background_set(self):
        """
        Switch to the previous background set. If at the start of the list, loop back to the last set.
        """
        self.current_set = (self.current_set - 1) % len(self.background_sets)

    def reset_background(self):
        """
        Reset to the default background set (first one).
        """
        self.current_set = 0
