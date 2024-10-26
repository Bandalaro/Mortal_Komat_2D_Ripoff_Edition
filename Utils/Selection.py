import pygame
import random
from Character.character_selecty import CharacterSelect

class BackgroundSelect:
    def __init__(self, screen, backgrounds):
        """
        Initialize the background selection menu.
        :param screen: Pygame screen where the selection menu will be displayed.
        :param backgrounds: A list of available background names (indices or names).
        """
        self.screen = screen
        self.backgrounds = backgrounds
        self.selected_index = 0
        self.font = pygame.font.Font(None, 74)
        self.selection_color = (0, 255, 0)  # Green color for selected background
        self.normal_color = (255, 255, 255)  # White color for other backgrounds

    def draw(self):
        """
        Draw the background selection screen.
        """
        self.screen.fill((0, 0, 0))  # Black background

        for i, background_name in enumerate(self.backgrounds):
            color = self.selection_color if i == self.selected_index else self.normal_color
            text_surface = self.font.render(f"Background {i + 1}", True, color)

            # Center the text horizontally and space it vertically
            x = (self.screen.get_width() - text_surface.get_width()) // 2
            y = 100 + i * 100
            self.screen.blit(text_surface, (x, y))

        pygame.display.flip()

    def update(self):
        """
        Handle background selection using arrow keys and 'Enter'.
        :return: The selected background index when 'Enter' is pressed, else None.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.selected_index = (self.selected_index + 1) % len(self.backgrounds)
            pygame.time.wait(200)  # Add delay to avoid rapid input

        if keys[pygame.K_UP]:
            self.selected_index = (self.selected_index - 1) % len(self.backgrounds)
            pygame.time.wait(200)

        if keys[pygame.K_RETURN]:
            return self.selected_index

        return None

def clear_event_queue():
    """
    Clear the Pygame event queue to prevent key buffering issues.
    """
    pygame.event.clear()

def wait_for_key_release():
    """
    Wait for all keys to be released before proceeding.
    This ensures that there is no accidental carry-over of key inputs from the previous selection.
    """
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                waiting = False

def selection_flow(environment, characters_data, screen, screen_width, screen_height):
    """
    Handle the flow for selecting the background and character.
    :param environment: The Environment object managing background sets.
    :param characters_data: A dictionary mapping character names to their asset paths.
    :param screen: Pygame screen where the selection will be drawn.
    :param screen_width: Width of the game screen.
    :param screen_height: Height of the game screen.
    :return: Selected background index and selected character data.
    """
    # --- Background Selection ---
    background_selector = BackgroundSelect(screen, range(len(environment.background_sets)))
    selected_background = None

    while selected_background is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        selected_background = background_selector.update()
        background_selector.draw()

    # Set the selected background in the environment
    environment.set_background_set(selected_background)

    # Clear event queue and wait for key release before starting character selection
    clear_event_queue()
    wait_for_key_release()

    # --- Character Selection ---
    character_names = list(characters_data.keys())
    character_selector = CharacterSelect(screen, character_names)
    selected_character_name = None

    while selected_character_name is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        selected_character_name = character_selector.update()
        character_selector.draw()

    # Return the selected background index and character data
    selected_character_data = {'name': selected_character_name, 'base_folder': characters_data[selected_character_name]}

    return selected_background, selected_character_data
