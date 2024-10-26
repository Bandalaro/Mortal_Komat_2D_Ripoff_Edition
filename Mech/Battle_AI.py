import numpy as np
from Mech.DQN import PPOAgent
from Character.character import Character

class BattleAI:
    GRAVITY = 2  # Gravity constant

    def __init__(self, character_names, state_size, action_size, screen_width, screen_height):
        self.character_names = character_names
        self.state_size = state_size
        self.action_size = action_size
        self.agent = PPOAgent(state_size, action_size)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.selected_character = None
        self.ai_character = None

    def select_character(self, player_position):
        character_name = np.random.choice(self.character_names)
        self.selected_character = character_name
        self.ai_character = self.load_character(character_name, player_position)
        return self.ai_character

    def load_character(self, character_name, player_position):
        base_folder = f'Assets/Characters/{character_name}'
        character = Character(
            name=character_name,
            base_folder=base_folder,
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )
        # Position the AI character on the opposite side of the player
        character.position = [self.screen_width - 100, player_position[1]]
        return character

    def update_state(self, player_character):
        if self.ai_character is None:
            return np.zeros((1, self.state_size))

        state = np.array([
            self.ai_character.position[0], self.ai_character.position[1],
            player_character.position[0], player_character.position[1],
            self.ai_character.health, player_character.health,
            int(self.ai_character.is_jumping), int(self.ai_character.is_attacking),
            int(self.ai_character.is_hurt), int(self.ai_character.is_dead)
        ]).reshape(1, -1)

        return state

    def take_action(self, state):
        if np.random.rand() < 0.3:
            return np.random.randint(0, self.action_size)
        action, _ = self.agent.get_action(state)
        return action

    def execute_action(self, action):
        if self.ai_character and not self.ai_character.is_dead:
            if not (self.ai_character.is_hurt or self.ai_character.is_attacking):
                action_map = {
                    0: (-3, 0),  # Move left
                    1: (3, 0),   # Move right
                    2: (0, -10),  # Jump
                    3: 'Attack_One',  # Attack1
                    4: 'Attack_Two',  # Attack2
                    5: 'Attack_Three'  # Attack3
                }

                if action in action_map:
                    if action in [0, 1, 2]:  # Movement actions
                        dx, dy = action_map[action]
                        self.ai_character.move(dx, dy)
                    else:  # Attack actions
                        attack_type = action_map[action]
                        self.ai_character.attack(attack_type)

    def train(self, states, actions, rewards, next_states, dones):
        self.agent.train(states, actions, rewards, next_states, dones)

    def rational_behavior(self, player_character):
        state = self.update_state(player_character)
        if player_character.health < 20:
            action = np.random.choice([3, 4, 5], p=[0.3, 0.3, 0.4])
        elif self.ai_character.health < 20:
            action = np.random.choice([0, 1], p=[0.8, 0.2])
        else:
            action = self.take_action(state)
        self.execute_action(action)

    def apply_gravity(self):
        """Applies gravity to the AI character and prevents it from exceeding Y-axis limits."""
        if self.ai_character and (self.ai_character.is_jumping or self.ai_character.velocity_y != 0):
            self.ai_character.velocity_y += self.GRAVITY  # Apply gravity to velocity
            self.ai_character.position[1] += self.ai_character.velocity_y  # Update Y position based on velocity

            # Ensure the character doesn't fall below the ground
            if self.ai_character.position[1] >= self.screen_height - self.ai_character.height:  # Set ground level
                self.ai_character.position[1] = self.screen_height - self.ai_character.height
                self.ai_character.velocity_y = 0
                self.ai_character.is_jumping = False  # Stop jumping when it hits the ground

            # Ensure the character doesn't jump too high
            elif self.ai_character.position[1] < 0:
                self.ai_character.position[1] = 0
                self.ai_character.velocity_y = 0  # Prevent it from going beyond the top of the screen

    def update(self, player_character):
        """Update the AI's behavior, including gravity and actions."""
        self.apply_gravity()
        self.rational_behavior(player_character)  # Take rational actions based on state
