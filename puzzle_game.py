import pygame
from constants import WINDOW_SIZE, MOVE_SOUND
from utils import choose_image, load_image, shuffle_board
from solver import a_star
from ui import draw_board, draw_buttons, draw_stats_popup

class PuzzleGame:
    def __init__(self, grid_size=3, music_on=True):
        self.grid_size_options = [3, 4, 5, 6]
        self.grid_size = grid_size
        self.mode = "number"
        self.music_on = music_on
        self.initialize_board()
        self.image_tiles = None
        self.selected_image = None
        self.running = True
        self.solving = False
        self.paused = False
        self.won = False
        self.move_count = 0
        self.show_stats = False
        self.stats = {}
        self.hovered_button = None
        self.initial_a_star_steps = 0
        self.error_message = None
        self.error_timer = 0
        self.solution_path = []
        if self.music_on and pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(-1)  # Tiếp tục phát nhạc nền nếu bật

    def initialize_board(self):
        if self.grid_size > 7:
            self.error_message = "Grid size too large! Maximum supported size is 7x7."
            self.error_timer = 3000
            self.grid_size = 3
        self.board = [[i * self.grid_size + j for j in range(self.grid_size)] for i in range(self.grid_size)]
        self.board[-1][-1] = self.grid_size * self.grid_size - 1
        self.empty_pos = [self.grid_size - 1, self.grid_size - 1]
        self.goal = [[i * self.grid_size + j for j in range(self.grid_size)] for i in range(self.grid_size)]
        self.goal[-1][-1] = self.grid_size * self.grid_size - 1
        self.move_count = 0
        self.won = False
        self.show_stats = False
        self.paused = False
        self.solving = False
        self.solution_path = []  # Sửa lỗi dòng 46
        self.tile_size = 450 // self.grid_size
        self.grid_offset_x = (WINDOW_SIZE[0] - self.grid_size * self.tile_size) // 2
        self.grid_offset_y = 50
        self.initial_a_star_steps = 0

    def shuffle_board(self):
        self.board, self.empty_pos = shuffle_board(self.board, self.grid_size, self.empty_pos)
        self.move_count = 0
        self.won = False
        self.show_stats = False
        self.paused = False
        self.solving = False
        self.solution_path = []
        solution, stats = a_star(self.board, self.empty_pos, self.grid_size, self.goal, single_step=False)
        self.initial_a_star_steps = len(solution) if solution else 0
        if stats.get("error"):
            self.error_message = stats["error"]
            self.error_timer = 3000

    def move_tile(self, pos):
        x, y = pos
        if self.grid_offset_x <= x < self.grid_offset_x + self.grid_size * self.tile_size and self.grid_offset_y <= y < self.grid_offset_y + self.grid_size * self.tile_size:
            j = (x - self.grid_offset_x) // self.tile_size
            i = (y - self.grid_offset_y) // self.tile_size
            if abs(i - self.empty_pos[0]) + abs(j - self.empty_pos[1]) == 1:
                self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[i][j]
                self.board[i][j] = self.grid_size * self.grid_size - 1
                self.empty_pos = [i, j]
                self.move_count += 1
                self.solution_path = []
                self.solving = False
                self.paused = False
                if self.board == self.goal:
                    self.won = True
                    self.show_stats = True
                    self.stats = {
                        "nodes_expanded": 0,
                        "total_nodes": 0,
                        "steps": self.move_count,
                        "time": 0
                    }

    def run(self, screen):
        main_buttons = draw_buttons(screen, (0, 0), self)
        popup_buttons = []
        clock = pygame.time.Clock()
        last_auto_move = 0
        auto_move_delay = 300 

        while self.running:
            current_time = pygame.time.get_ticks()
            mouse_pos = pygame.mouse.get_pos()
            draw_board(screen, self)
            main_buttons = draw_buttons(screen, mouse_pos, self)
            if self.show_stats:
                popup_buttons = draw_stats_popup(screen, mouse_pos, self)

            if self.error_timer > 0:
                self.error_timer -= clock.get_time()
                if self.error_timer <= 0:
                    self.error_message = None

            if self.solving and not self.paused and not self.won and current_time - last_auto_move >= auto_move_delay:
                if not self.solution_path:
                    self.solution_path, self.stats = a_star(self.board, self.empty_pos, self.grid_size, self.goal, single_step=False)
                    if not self.solution_path:
                        self.solving = False
                        self.paused = False
                        self.error_message = self.stats.get("error", "No solution found")
                        self.error_timer = 3000
                if self.solution_path:
                    step_board, step_empty = self.solution_path.pop(0)
                    self.board = [row[:] for row in step_board]
                    self.empty_pos = step_empty[:]
                    self.move_count += 1
                    last_auto_move = current_time
                    if self.board == self.goal:
                        self.won = True
                        self.show_stats = True
                        self.solving = False
                        self.paused = False

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.show_stats:
                        for text, _, _, rect in popup_buttons:
                            if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:
                                if text == "Continue":
                                    self.shuffle_board()
                                elif text == "Exit":
                                    self.running = False
                                    return True  
                        continue

                    for text, _, _, rect in main_buttons:
                        if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:
                            if text == "Choose Image":
                                image_path = choose_image()
                                if image_path:
                                    self.mode = "image"
                                    self.image_tiles, error = load_image(image_path, self.grid_size, self.tile_size)
                                    if error:
                                        self.error_message = error
                                        self.error_timer = 3000
                                        self.mode = "number"
                                    else:
                                        self.shuffle_board()
                            elif text == "Number Mode":
                                self.mode = "number"
                                self.image_tiles = None
                                self.shuffle_board()
                            elif text == "Shuffle":
                                self.shuffle_board()
                            elif text == "Auto Solve":
                                if not self.won and not self.solving:
                                    self.solving = True
                                    self.paused = False
                                    self.solution_path = []
                            elif text == "Pause":
                                self.paused = True
                            elif text == "Exit":
                                self.running = False
                                return True  
                    if not self.solving and not self.won:
                        self.move_tile(event.pos)
                    elif self.solving and self.paused:
                        self.move_tile(event.pos)
        return False 
# COPYRIGHT by Perfect Dragon King (PDK)
