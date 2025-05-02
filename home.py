import pygame
from constants import WINDOW_SIZE, SMALL_FONT, PASTEL_BLUE, PASTEL_BLUE_HOVER, PASTEL_GREEN, PASTEL_GREEN_HOVER, PASTEL_ORANGE, PASTEL_ORANGE_HOVER, PASTEL_YELLOW, PASTEL_YELLOW_HOVER, BLACK, WHITE

class HomeScreen:
    def __init__(self):
        self.running = True
        self.show_combobox = False
        self.show_instructions = False
        self.selected_grid_size = "3x3"
        self.grid_sizes = ["3x3", "4x4", "5x5", "6x6"]
        self.music_on = True
        self.music_button_color = BLACK
        self.music_button_text_color = WHITE
        pygame.mixer.music.play(-1)  # Play background music on start

    def draw_buttons(self, screen, mouse_pos):
        buttons = [
            ("Start", PASTEL_GREEN, PASTEL_GREEN_HOVER, (WINDOW_SIZE[0] // 2 - 60, 300, 120, 50)),
            ("Size", PASTEL_BLUE, PASTEL_BLUE_HOVER, (WINDOW_SIZE[0] // 2 - 60, 360, 120, 50)),
            ("How to play", PASTEL_YELLOW, PASTEL_YELLOW_HOVER, (WINDOW_SIZE[0] // 2 - 60, 420, 120, 50)),
            ("Music", self.music_button_color, self.music_button_color, (WINDOW_SIZE[0] // 2 - 60, 480, 120, 50)),
            ("Exit", PASTEL_ORANGE, PASTEL_ORANGE_HOVER, (WINDOW_SIZE[0] // 2 - 60, 540, 120, 50))
        ]
        hovered_button = None
        for text, color, hover_color, rect in buttons:
            if text == "Music":
                hover_color = color  # Music button doesn't change color on hover
            if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
                pygame.draw.rect(screen, hover_color, rect, border_radius=15)
                hovered_button = text
            else:
                pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)
            text_color = self.music_button_text_color if text == "Music" else BLACK
            label = SMALL_FONT.render(text, True, text_color)
            label_rect = label.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
            screen.blit(label, label_rect)
        return buttons, hovered_button

    def draw_combobox(self, screen, mouse_pos):
        combobox_width, combobox_height = 120, 160
        combobox_x = WINDOW_SIZE[0] // 2 - 60
        combobox_y = 410  # Below Size button

        pygame.draw.rect(screen, WHITE, (combobox_x, combobox_y, combobox_width, combobox_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (combobox_x, combobox_y, combobox_width, combobox_height), 2, border_radius=10)

        options = []
        for i, size in enumerate(self.grid_sizes):
            if int(size[0]) > 7:
                continue
            rect = (combobox_x, combobox_y + i * 30, combobox_width, 30)
            if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
                pygame.draw.rect(screen, PASTEL_BLUE_HOVER, rect)
            else:
                pygame.draw.rect(screen, PASTEL_BLUE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            label = SMALL_FONT.render(size, True, BLACK)
            label_rect = label.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
            screen.blit(label, label_rect)
            options.append((size, rect))

        ok_rect = (combobox_x + 20, combobox_y + combobox_height - 40, 80, 30)
        if ok_rect[0] <= mouse_pos[0] <= ok_rect[0] + ok_rect[2] and ok_rect[1] <= mouse_pos[1] <= ok_rect[1] + ok_rect[3]:
            pygame.draw.rect(screen, PASTEL_GREEN_HOVER, ok_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, PASTEL_GREEN, ok_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, ok_rect, 2, border_radius=10)
        label = SMALL_FONT.render("OK", True, BLACK)
        label_rect = label.get_rect(center=(ok_rect[0] + ok_rect[2] // 2, ok_rect[1] + ok_rect[3] // 2))
        screen.blit(label, label_rect)

        return options, ok_rect

    def draw_instructions(self, screen, mouse_pos):
        popup_width, popup_height = 600, 600
        popup_x = (WINDOW_SIZE[0] - popup_width) // 2
        popup_y = (WINDOW_SIZE[1] - popup_height) // 2

        pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 2, border_radius=10)

        title_text = SMALL_FONT.render("                               How to Play", True, BLACK)
        screen.blit(title_text, (popup_x + 20, popup_y + 20))

        instructions = [
            "           Welcome to the Sliding Puzzle Game!",
            "",
            "- Choose a grid size (3x3 to 6x6) from the 'Size' button.",
            "- Select 'Number Mode' to play with numbered tiles or",
            "- Select 'Choose Image' to use a custom image.",
            "- Click tiles next to the empty space to move them.",
            "- Goal: Arrange tiles in order (1 to N) or restore the image.",
            "- Use 'Shuffle' to randomize the board.",
            "- Click 'Auto Solve' to let the A* algorithm solve the puzzle.",
            "",
            "About the A* Algorithm:",
            "- A* is a pathfinding algorithm that finds the shortest path",
            "  from the current board to the goal state.",
            "- It uses a heuristic (Manhattan Distance) to estimate the",
            "  distance to the goal, ensuring an optimal solution.",
            "- The algorithm explores possible moves, prioritizing those",
            "  that are likely to lead to the solution faster.",
            "",
            "Tips:",
            "- Use 'Pause' during auto-solving to take control.",
            "- Have fun and challenge yourself with larger grids!"
        ]

        for i, line in enumerate(instructions):
            line_text = SMALL_FONT.render(line, True, BLACK)
            screen.blit(line_text, (popup_x + 20, popup_y + 50 + i * 25))

        back_button = (popup_x + popup_width - 120, popup_y + popup_height - 60, 100, 40)
        if back_button[0] <= mouse_pos[0] <= back_button[0] + back_button[2] and back_button[1] <= mouse_pos[1] <= back_button[1] + back_button[3]:
            pygame.draw.rect(screen, PASTEL_ORANGE_HOVER, back_button, border_radius=10)
        else:
            pygame.draw.rect(screen, PASTEL_ORANGE, back_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, back_button, 2, border_radius=10)
        label = SMALL_FONT.render("Back", True, BLACK)
        label_rect = label.get_rect(center=(back_button[0] + back_button[2] // 2, back_button[1] + back_button[3] // 2))
        screen.blit(label, label_rect)

        return back_button

    def run(self, screen):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill(WHITE)
            title = SMALL_FONT.render("Puzzle Game", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_SIZE[0] // 2, 200))
            screen.blit(title, title_rect)

            buttons, hovered_button = self.draw_buttons(screen, mouse_pos)
            if self.show_combobox:
                combobox_options, ok_button = self.draw_combobox(screen, mouse_pos)
            if self.show_instructions:
                back_button = self.draw_instructions(screen, mouse_pos)

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.show_instructions:
                        if back_button and back_button[0] <= x <= back_button[0] + back_button[2] and back_button[1] <= y <= back_button[1] + back_button[3]:
                            self.show_instructions = False
                        continue
                    if self.show_combobox:
                        for size, rect in combobox_options:
                            if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:
                                self.selected_grid_size = size
                        if ok_button and ok_button[0] <= x <= ok_button[0] + ok_button[2] and ok_button[1] <= y <= ok_button[1] + ok_button[3]:
                            self.show_combobox = False
                        continue

                    for text, _, _, rect in buttons:
                        if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:
                            if text == "Start":
                                grid_size = int(self.selected_grid_size[0])
                                self.running = False
                                return grid_size
                            elif text == "Size":
                                self.show_combobox = not self.show_combobox
                            elif text == "How to play":
                                self.show_instructions = True
                            elif text == "Music":
                                self.music_on = not self.music_on
                                if self.music_on:
                                    self.music_button_color = BLACK
                                    self.music_button_text_color = WHITE
                                    pygame.mixer.music.play(-1)
                                else:
                                    self.music_button_color = WHITE
                                    self.music_button_text_color = BLACK
                                    pygame.mixer.music.stop()
                            elif text == "Exit":
                                self.running = False
                                return None
# COPYRIGHT by Perfect Dragon King (PDK)