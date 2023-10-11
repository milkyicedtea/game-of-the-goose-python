import pygame
import random
import sys
from collections import deque
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 0, 255)
CELL_SIZE = 60
CELL_GAP = 4
BOARD_SIZE = 63
MAX_ROLL_HISTORY = 3
MOVE_SPEED = 200

# Initialize the main screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of the Goose")


# Player class
class Player:
    def __init__(self, name, color):
        self.position = 0
        self.name = name
        self.color = color
        self.roll_history = deque(maxlen=MAX_ROLL_HISTORY)
        self.animation_start_time = 0
        self.target_position = None

    def move(self, steps):
        if self.target_position is None:
            self.target_position = self.position + steps
            self.animation_start_time = time.time()

    def update(self):
        if self.target_position is not None:
            elapsed_time = min(time.time() - self.animation_start_time, 1.0)
            progress = elapsed_time
            x1, y1 = board_positions[self.position]

            if self.target_position < BOARD_SIZE:
                x2, y2 = board_positions[self.target_position]
                x = int(x1 + (x2 - x1) * progress * 1)  # Adjust the factor (0.75) to control speed
                y = int(y1 + (y2 - y1) * progress * 1)  # Adjust the factor (0.75) to control speed

                # Update player's position directly
                self.position = self.position + int(progress * 1 * (self.target_position - self.position))
                self.draw()

                if elapsed_time >= 1.0:
                    self.position = self.target_position
                    self.target_position = None

    def draw(self):
        position = min(self.position, BOARD_SIZE)
        if position < len(board_positions):
            x, y = board_positions[position]
            x += CELL_SIZE // 2
            y += CELL_SIZE // 2
            pygame.draw.circle(screen, self.color, (x, y), 10)


# Initialize the player
player = Player("Player", PLAYER_COLOR)

# Board positions (x, y)
board_positions = []
x, y = WIDTH // 2, HEIGHT // 2
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
direction_index = 0
steps_until_direction_change = 1
current_step = 0

for i in range(1, BOARD_SIZE + 1):
    board_positions.append((x, y))

    if current_step == steps_until_direction_change:
        direction_index = (direction_index + 1) % 4
        if direction_index % 2 == 0:
            steps_until_direction_change += 1
        current_step = 0

    dx, dy = directions[direction_index]
    x += (dx * CELL_SIZE) + (dx * CELL_GAP)
    y += (dy * CELL_SIZE) + (dy * CELL_GAP)

    current_step += 1

board_positions.reverse()

for i, (x, y) in enumerate(board_positions):
    x -= CELL_SIZE // 2
    y -= CELL_SIZE // 2
    board_positions[i] = (x, y)

# Load the winner image (replace "winner_image.png" with your image file path)
winner_image = pygame.image.load("resources/calvino2.jpg")

# Calculate image_rect
image_rect = winner_image.get_rect()

# Popup screen
popup_screen = None


# Main game loop
def main():
    global popup_screen

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    roll_result = random.randint(1, 6)
                    print(f"{player.name} rolled a {roll_result}")

                    # Check for winning condition before moving the player
                    if player.position + roll_result >= BOARD_SIZE:
                        player.position = BOARD_SIZE  # Set the player's position to the winning position
                        winner_name = player.name
                        popup_size = (640, 384)
                        popup_screen = pygame.display.set_mode(popup_size)
                        pygame.display.set_caption("Winner")

                        popup_screen.fill(WHITE)
                        popup_screen.blit(winner_image, ((popup_size[0] - image_rect.width) // 2, (popup_size[1] - image_rect.height) // 2))

                        font = pygame.font.Font(None, 36)
                        text = font.render(f"{winner_name} wins!", True, PLAYER_COLOR)
                        text_rect = text.get_rect(center=(popup_size[0] // 2, popup_size[1] - 30))
                        popup_screen.blit(text, text_rect)
                        pygame.display.flip()
                    else:
                        player.move(roll_result)

        if player.position < len(board_positions):
            screen.fill(WHITE)

            for i, (x, y) in enumerate(board_positions):
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)
                font = pygame.font.Font(None, 24)
                text = font.render(str(i + 1), True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

            player.update()
            player.draw()

            if player.position < len(board_positions):
                # ... (previous code)

                # Display rolls in blue
                roll_display_x = 30
                roll_display_y = 400  # Adjust the vertical position
                font = pygame.font.Font(None, 24)
                rolls_text = f"{player.name} Rolls:\n"
                for roll in player.roll_history:
                    rolls_text += f"{player.name} rolled a {roll}\n"
                rolls_text += "\n"

                # Split the rolls text into lines and render them separately
                lines = rolls_text.splitlines()
                y_offset = 0
                for line in lines:
                    text_color = (0, 0, 255)  # Blue text color
                    text = font.render(line, True, text_color)  # Use blue text color for roll messages
                    screen.blit(text, (roll_display_x, roll_display_y + y_offset))
                    y_offset += font.get_height()

                pygame.display.flip()


if __name__ == "__main__":
    main()
