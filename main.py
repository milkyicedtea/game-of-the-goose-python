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
    13: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili sono un sogno, poiché invivibili.",
    14: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili sono un sogno, poiché invivibili.",
    15: "Diceva che dal momento che è sempre più difficile vivere come in città forse ci si sta avvicinando a un momento di crisi di vita urbana. E le città Invisibili sono un sogno, poiché invivibili.",
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
    30: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… Raggiungi le caselle da 40 a 44 per leggere il continuo!",
    31: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… Raggiungi le caselle da 40 a 44 per leggere il continuo!",
    32: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… Raggiungi le caselle da 40 a 44 per leggere il continuo!",
    33: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… Raggiungi le caselle da 40 a 44 per leggere il continuo!",
    34: "Riflette sulle ragioni segrete che guidano l’ uomo verso le città, esplorando le radici delle città antiche e nella modernità. Queste città… Raggiungi le caselle da 40 a 44 per leggere il continuo!",
    35: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… Raggiungi le caselle da 45 a 49 per sapere il continuo!",
    36: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… Raggiungi le caselle da 45 a 49 per sapere il continuo!",
    37: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… Raggiungi le caselle da 45 a 49 per sapere il continuo!",
    38: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… Raggiungi le caselle da 45 a 49 per sapere il continuo!",
    39: "Nel racconto 'Le città invisibili' di Italo Calvino, la struttura bipolare emerge attraverso le descrizioni delle città. Marco Polo, nel suo dialogo con Kublai Khan, rivela città che sono visibili e invisibili, creando un'atmosfera di… Raggiungi le caselle da 45 a 49 per sapere il continuo!",
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

cell_images = {
    1: "./resources/CALVINO/1/Italo_Calvino.png",
    2: "./resources/CALVINO/1/Italo_Calvino.png",
    3: "./resources/CALVINO/1/Italo_Calvino.png",
    4: "./resources/CALVINO/1/Italo_Calvino.png",
    5: "./resources/CALVINO/2/Calvino_crater_mercurio.jpg",
    6: "./resources/CALVINO/1/Italo_Calvino.png",
    7: "./resources/CALVINO/2/Calvino_crater_mercurio.jpg",
    8: "./resources/CALVINO/1/Italo_Calvino.png",
    9: "./resources/CALVINO/2/Calvino_crater_mercurio.jpg",
    10: "./resources/CALVINO/3/anastasia-400-per-sito_7bxh.jpg",
    11: "./resources/CALVINO/3/anastasia-400-per-sito_7bxh.jpg",
    12: "./resources/CALVINO/3/anastasia-400-per-sito_7bxh.jpg",
    13: "./resources/CALVINO/4/Him_sitDown.jpg",
    14: "./resources/CALVINO/4/Him_sitDown.jpg",
    15: "./resources/CALVINO/4/Him_sitDown.jpg",
    16: "./resources/CALVINO/categorie_11_citta/1_diomira_Memoria.png",
    17: "./resources/CALVINO/categorie_11_citta/1_diomira_Memoria.png",
    18: "./resources/CALVINO/categorie_11_citta/1_diomira_Memoria.png",
    19: "./resources/CALVINO/categorie_11_citta/2_despina_Desiderio.png",
    20: "./resources/CALVINO/categorie_11_citta/2_despina_Desiderio.png",
    21: "./resources/CALVINO/categorie_11_citta/2_despina_Desiderio.png",
    22: "./resources/CALVINO/categorie_11_citta/3_tamara_Segni.png",
    23: "./resources/CALVINO/categorie_11_citta/3_tamara_Segni.png",
    24: "./resources/CALVINO/categorie_11_citta/3_tamara_Segni.png",
    25: "./resources/CALVINO/categorie_11_citta/4_ottavia_Sottili.png",
    26: "./resources/CALVINO/categorie_11_citta/4_ottavia_Sottili.png",
    27: "./resources/CALVINO/categorie_11_citta/4_ottavia_Sottili.png",
    28: "./resources/CALVINO/categorie_11_citta/5_ersilia_Scambi.png",
    29: "./resources/CALVINO/categorie_11_citta/5_ersilia_Scambi.png",
    30: "./resources/CALVINO/4/Him_Think.PNG",
    31: "./resources/CALVINO/4/Him_Think.PNG",
    32: "./resources/CALVINO/4/Him_Think.PNG",
    33: "./resources/CALVINO/4/Him_Think.PNG",
    34: "./resources/CALVINO/4/Him_Think.PNG",
    35: "./resources/CALVINO/marco-polo.png",
    36: "./resources/CALVINO/marco-polo.png",
    37: "./resources/CALVINO/marco-polo.png",
    38: "./resources/CALVINO/marco-polo.png",
    39: "./resources/CALVINO/marco-polo.png",
    40: "./resources/CALVINO/4/Him_Think.PNG",
    41: "./resources/CALVINO/4/Him_Think.PNG",
    42: "./resources/CALVINO/4/Him_Think.PNG",
    43: "./resources/CALVINO/4/Him_Think.PNG",
    44: "./resources/CALVINO/4/Him_Think.PNG",
    45: "./resources/CALVINO/marco-polo.png",
    46: "./resources/CALVINO/marco-polo.png",
    47: "./resources/CALVINO/marco-polo.png",
    48: "./resources/CALVINO/marco-polo.png",
    49: "./resources/CALVINO/marco-polo.png",
    50: "./resources/CALVINO/categorie_11_citta/6_bauci_Occhi.png",
    51: "./resources/CALVINO/categorie_11_citta/6_bauci_Occhi.png",
    52: "./resources/CALVINO/categorie_11_citta/7_aglaura_Nomi.png",
    53: "./resources/CALVINO/categorie_11_citta/7_aglaura_Nomi.png",
    54: "./resources/CALVINO/categorie_11_citta/8_eusapia_Morti.png",
    55: "./resources/CALVINO/categorie_11_citta/8_eusapia_Morti.png",
    56: "./resources/CALVINO/categorie_11_citta/9_eudossia_Cielo.png",
    57: "./resources/CALVINO/categorie_11_citta/9_eudossia_Cielo.png",
    58: "./resources/CALVINO/categorie_11_citta/10_procopia_Continue.png",
    59: "./resources/CALVINO/categorie_11_citta/10_procopia_Continue.png",
    60: "./resources/CALVINO/categorie_11_citta/11_oldindia_Nascoste.png",
    61: "./resources/CALVINO/categorie_11_citta/11_oldindia_Nascoste.png",
    62: "./resources/CALVINO/2/him_happy.jpg",
}


def show_special_popup(text, position, image_path=None):
    print('show_special_popup')
    # Store the original game window size
    original_size = screen.get_size()
    if position != 63:
        popup_width, popup_height = 800, 400
        popup_screen = pygame.display.set_mode((popup_width, popup_height))
        pygame.display.set_caption("Special Popup")

        popup_screen.fill(WHITE)
        font = pygame.font.Font(None, 24)  # Adjust the font size

        # Wrap the text to fit within the popup window width
        max_line_width = popup_width - 40  # Adjust the padding
        wrapped_text = []
        words = text.split()
        line = []
        line_width = 0

        for word in words:
            word_surface = font.render(word, True, (0, 0, 0))
            word_width, word_height = word_surface.get_size()

            if line_width + word_width <= max_line_width:
                line.append(word)
                line_width += word_width
            else:
                wrapped_text.append(" ".join(line))
                line = [word]
                line_width = word_width

        if line:
            wrapped_text.append(" ".join(line))

        text_rect = pygame.Rect(10, 10, max_line_width, popup_height - 40)  # Adjust the position and size
        for line in wrapped_text:
            text_surface = font.render(line, True, (0, 0, 0))
            popup_screen.blit(text_surface, text_rect.topleft)
            text_rect.top += word_height  # Adjust the line spacing

        # Load and display an image if provided
        print(position)
        if position in cell_images:
            image_path = cell_images[position]
            try:
                image = pygame.image.load(image_path)

                # Calculate the maximum available width and height
                max_width = max_line_width  # To fit the text width
                max_height = popup_height - 40  # Adjust for padding

                # Get the image dimensions
                image_width, image_height = image.get_size()

                # Calculate the scaling factor for width and height
                width_factor = max_width / image_width
                height_factor = max_height / image_height

                # Choose the smallest scaling factor to maintain aspect ratio
                scale_factor = min(width_factor, height_factor)

                # Resize the image while maintaining aspect ratio
                image = pygame.transform.scale(image, (int(image_width * scale_factor), int(image_height * scale_factor)))

                # Calculate the position to center the image
                image_x = (max_width - image.get_width()) // 2
                image_y = (max_height - image.get_height()) // 2 + 40

                popup_screen.blit(image, (10 + image_x, 10 + image_y))
            except pygame.error as e:
                print(f"Error loading image: {e}")

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

        # Restore the original game window size
        pygame.display.set_mode(original_size)


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
                        player.position = BOARD_SIZE
                        winner_name = player.name
                        popup_size = (640, 384)
                        popup_screen = pygame.display.set_mode(popup_size)
                        pygame.display.set_caption("Winner")

                        popup_screen.fill(WHITE)
                        winning_image = pygame.image.load("./resources/calvino2.jpg")
                        popup_screen.blit(winning_image, ((popup_size[0] - winning_image.get_width()) // 2,
                                                          (popup_size[1] - winning_image.get_height()) // 2))
                        font = pygame.font.Font(None, 36)
                        text = font.render(f"{winner_name} wins!", True, player.color)
                        text_rect = text.get_rect(center = (popup_size[0] // 2, popup_size[1] - 30))
                        popup_screen.blit(text, text_rect)
                        pygame.display.flip()
                    else:
                        target_position = player.position + roll_result
                        if player.position in cell_phrases:
                            special_popup = cell_phrases[player.position] or cell_images[player.position]
                            print(special_popup)

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
                print(player.position)
                print('calling special popup')
                show_special_popup(special_popup, player.position, cell_images)
                special_popup = None

            pygame.display.flip()

        # Remove the special pop-up after a delay
        if special_popup:
            pygame.time.delay(2000)  # Display the pop-up for 2 seconds
            special_popup = None


if __name__ == "__main__":
    main()
