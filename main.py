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
PLAYER_COLORS = [(0, 0, 255)]
CELL_SIZE = 60
CELL_GAP = 4
BOARD_SIZE = 63
MAX_ROLL_HISTORY = 3

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

# Define a dictionary to map cell positions to phrases
cell_phrases = {
    1: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    2: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    3: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    4: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    5: "La sua comicità di fornire il modello Universo in poche pagine nella sua espressione",
    6: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    7: "La sua comicità di fornire il modello universo in poche pagine nella sua espressione",
    8: "Le città sono divise in categorie, sono 55. Scopri di quali città stiamo parlando continuando a giocare!",
    9: "La sua comicità di fornire il modello universo in poche pagine nella sua espressione",
    10: "Ogni città ha un messaggio che puo' essere implicito o esplicito",
    11: "Ogni città ha un messaggio che puo' essere implicito o esplicito",
    12: "Ogni città ha un messaggio che puo' essere implicito o esplicito",
    13: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili (quelle che sogna) sono un sogno, poiché invivibili.",
    14: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili (quelle che sogna) sono un sogno, poiché invivibili.",
    15: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili (quelle che sogna) sono un sogno, poiché invivibili.",
    16: "",
    17: "",
    18: "",
    19: "",
    20: "",
    21: "",
    22: "",
    23: "",
    24: "",
    25: "",
    26: "",
    27: "",
    28: "",
    29: "",
    30: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… \nRaggiungi le caselle da 40 a 44 per leggere il continuo!",
    31: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… \nRaggiungi le caselle da 40 a 44 per leggere il continuo!",
    32: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… \nRaggiungi le caselle da 40 a 44 per leggere il continuo!",
    33: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… \nRaggiungi le caselle da 40 a 44 per leggere il continuo!",
    34: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… \nRaggiungi le caselle da 40 a 44 per leggere il continuo!",
    35: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… \nRaggiungi le caselle da 45 a 49 per sapere il continuo!",
    36: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… \nRaggiungi le caselle da 45 a 49 per sapere il continuo!",
    37: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… \nRaggiungi le caselle da 45 a 49 per sapere il continuo!",
    38: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… \nRaggiungi le caselle da 45 a 49 per sapere il continuo!",
    39: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… \nRaggiungi le caselle da 45 a 49 per sapere il continuo!",
    40: "Queste città mantengono i motivi da cui sono originate, mantenendo intatto il loro fascino misterioso e atermporale.",
    41: "Queste città mantengono i motivi da cui sono originate, mantenendo intatto il loro fascino misterioso e atermporale.",
    42: "Queste città mantengono i motivi da cui sono originate, mantenendo intatto il loro fascino misterioso e atermporale.",
    43: "Queste città mantengono i motivi da cui sono originate, mantenendo intatto il loro fascino misterioso e atermporale.",
    44: "Queste città mantengono i motivi da cui sono originate, mantenendo intatto il loro fascino misterioso e atermporale.",
    45: "…un'atmosfera di dualità costante. Questa tecnica narrativa mette in evidenza la complessità delle percezioni umane e si riflette nelle diverse città immaginarie descritte nel libro.",
    46: "…un'atmosfera di dualità costante. Questa tecnica narrativa mette in evidenza la complessità delle percezioni umane e si riflette nelle diverse città immaginarie descritte nel libro.",
    47: "…un'atmosfera di dualità costante. Questa tecnica narrativa mette in evidenza la complessità delle percezioni umane e si riflette nelle diverse città immaginarie descritte nel libro.",
    48: "…un'atmosfera di dualità costante. Questa tecnica narrativa mette in evidenza la complessità delle percezioni umane e si riflette nelle diverse città immaginarie descritte nel libro.",
    49: "…un'atmosfera di dualità costante. Questa tecnica narrativa mette in evidenza la complessità delle percezioni umane e si riflette nelle diverse città immaginarie descritte nel libro.",
    # Add more cell positions and phrases as needed
}


def show_special_popup(text):
    # Store original game window size
    original_size = screen.get_size()

    popup_size = (400, 200)
    popup_screen = pygame.display.set_mode(popup_size)
    pygame.display.set_caption("Special Popup")

    popup_screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(popup_size[0] // 2, popup_size[1] // 2))
    popup_screen.blit(text_surface, text_rect)
    pygame.display.flip()

    waiting_for_close = True
    while waiting_for_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to close the popup
                    waiting_for_close = False


# Main game loop
def main():
    global popup_screen
    special_popup = None  # Initialize special popup
    player = Player("Player 1", PLAYER_COLORS[0])  # Create a single player for a one-player game

    target_position = player.position  # Initialize target_position to current position
    move_speed = 5  # Adjust the speed of movement

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    roll_result = random.randint(1, 6)

                    print(f"{player.name} rolled a {roll_result}")

                    if player.position + roll_result >= BOARD_SIZE:
                        player.position = BOARD_SIZE  # Set the player's position to the winning position
                        winner_name = player.name
                        show_special_popup(f"{winner_name} wins!")
                    else:
                        # Update target_position for progressive movement
                        target_position = player.position + roll_result

                        # Check if the player has landed on a special cell
                        if player.position in cell_phrases:
                            special_popup = cell_phrases[player.position]

        if player.position < len(board_positions):
            screen.fill(WHITE)

            # Draw cells and cell numbers
            for i, (x, y) in enumerate(board_positions):
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)
                font = pygame.font.Font(None, 24)
                text = font.render(str(i + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

            # Implement progressive movement
            if player.position != target_position:
                dx = (board_positions[target_position][0] - board_positions[player.position][0]) / move_speed
                dy = (board_positions[target_position][1] - board_positions[player.position][1]) / move_speed
                player.position += 1
                pygame.time.delay(50)  # Delay to control the movement speed
            else:
                player.position = target_position

            player.draw()  # Use player's current position

            # Display rolls with player-specific colors
            roll_display_x = 30
            roll_display_y = 400
            font = pygame.font.Font(None, 24)

            rolls_text = f"{player.name} Rolls:\n"
            for roll in player.roll_history:
                text_color = player.color
                rolls_text += f"{player.name} rolled a {roll}\n"
            rolls_text += "\n"

            lines = rolls_text.splitlines()
            y_offset = 0
            for line in lines:
                text_color = player.color
                text = font.render(line, True, text_color)
                screen.blit(text, (roll_display_x, roll_display_y + y_offset))
                y_offset += font.get_height()

            # Display special pop-up
            if special_popup:
                show_special_popup(special_popup)
                special_popup = None

            pygame.display.flip()

        # Remove the special pop-up after a delay
        if special_popup:
            pygame.time.delay(2000)  # Display the pop-up for 2 seconds
            special_popup = None

if __name__ == "__main__":
    main()