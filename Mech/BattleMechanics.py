import pygame

class BattleMechanics:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.ground_level = screen_height - 150  # Define a ground level for characters

    def update(self, player, ai):
        """
        Update battle mechanics for both player and AI.
        Reduces health on successful attacks and ensures characters stay within screen boundaries.
        """
        # Ensure player and AI remain within the game boundaries
        self.ensure_within_boundaries(player)
        self.ensure_within_boundaries(ai)

        # Check for attack collisions and adjust health if necessary
        if player.is_attack_frame() and self.check_attack_collision(player, ai):
            ai.take_damage(1)  # AI loses health when player attack lands
        if ai.is_attack_frame() and self.check_attack_collision(ai, player):
            player.take_damage(1)  # Player loses health when AI attack lands

    def ensure_within_boundaries(self, character):
        """Ensure character does not move off screen or below the ground level."""
        character.position[0] = max(0, min(self.screen_width - character.width, character.position[0]))
        character.position[1] = min(self.ground_level, character.position[1])

    def check_attack_collision(self, attacker, target):
        """Check if the attacker's current attack range hits the target."""
        attack_range = pygame.Rect(attacker.position[0], attacker.position[1], attacker.attack_range_width, attacker.height)
        target_rect = pygame.Rect(target.position[0], target.position[1], target.width, target.height)
        return attack_range.colliderect(target_rect)

    def draw_health_bar(self, screen, player_character, ai_character, y):
        """Draw health bars for the player and AI."""
        player_health_x = 50  # X coordinate for player health bar
        ai_health_x = screen.get_width() - 200  # X coordinate for AI health bar

        # Calculate health bar sizes
        player_health_percentage = player_character.health / player_character.max_health
        ai_health_percentage = ai_character.health / ai_character.max_health

        # Draw player health bar
        pygame.draw.rect(screen, (255, 0, 0), (player_health_x, y, self.health_bar_width * player_health_percentage, self.health_bar_height))
        # Draw AI health bar
        pygame.draw.rect(screen, (0, 0, 255), (ai_health_x, y, self.health_bar_width * ai_health_percentage, self.health_bar_height))

    def draw_timer(self, screen, seconds_left):
        """Draw the countdown timer."""
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f'Time: {seconds_left}', True, (255, 255, 255))
        screen.blit(timer_text, (self.screen_width // 2 - 50, 20))

    def display_game_over(self, screen, player, ai):
        """Display a 'Game Over' message."""
        font = pygame.font.Font(None, 74)
        if player.health <= 0:
            game_over_text = font.render('Game Over! You Lose!', True, (255, 0, 0))
        elif ai.health <= 0:
            game_over_text = font.render('Game Over! You Win!', True, (255, 0, 0))
        else:
            game_over_text = font.render('Time Up!', True, (255, 255, 0))
        screen.blit(game_over_text, (self.screen_width // 2 - 200, self.screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)

    def calculate_reward(self, player, ai):
        """Calculate the reward based on player and AI actions."""
        reward = 0

        # Reward for dealing damage to the AI
        if ai.health < ai.max_health:
            reward += ai.max_health - ai.health  # Damage dealt

        # Penalty for taking damage
        if player.health < player.max_health:
            reward -= player.max_health - player.health  # Damage taken

        # Small bonus for performing attacks
        if player.is_attacking and player.is_attack_frame():
            reward += 5

        # Major reward/penalty for game end states
        if ai.is_dead:
            reward += 100
        if player.is_dead:
            reward -= 100

        return reward
