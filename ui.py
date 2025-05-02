import pygame
from constants import *

def draw_board(screen, game):
    screen.fill(WHITE)
    for i in range(game.grid_size):
        for j in range(game.grid_size):
            x = game.grid_offset_x + j * game.tile_size
            y = game.grid_offset_y + i * game.tile_size
            pygame.draw.rect(screen, GRAY, (x, y, game.tile_size, game.tile_size), 1)
            if game.board[i][j] == game.grid_size * game.grid_size - 1:
                pygame.draw.rect(screen, BLACK, (x, y, game.tile_size, game.tile_size))
            elif game.mode == "image" and game.image_tiles:
                tile_idx = game.board[i][j]
                if tile_idx != game.grid_size * game.grid_size - 1 and game.image_tiles[tile_idx]:
                    screen.blit(game.image_tiles[tile_idx], (x, y))
            else:
                text = SMALL_FONT.render(str(game.board[i][j] + 1), True, BLACK)
                text_rect = text.get_rect(center=(x + game.tile_size // 2, y + game.tile_size // 2))
                screen.blit(text, text_rect)

    for i in range(game.grid_size + 1):
        pygame.draw.line(screen, BLACK, (game.grid_offset_x, game.grid_offset_y + i * game.tile_size),
                         (game.grid_offset_x + game.grid_size * game.tile_size, game.grid_offset_y + i * game.tile_size), 2)
        pygame.draw.line(screen, BLACK, (game.grid_offset_x + i * game.tile_size, game.grid_offset_y),
                         (game.grid_offset_x + i * game.tile_size, game.grid_offset_y + game.grid_size * game.tile_size), 2)

    move_text = MOVE_FONT.render(f"Moves: {game.move_count}", True, BLACK)
    screen.blit(move_text, (game.grid_offset_x + game.grid_size * game.tile_size + 20, game.grid_offset_y))

    if game.error_message and game.error_timer > 0:
        error_text = SMALL_FONT.render(game.error_message, True, (255, 0, 0))
        error_rect = error_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - 50))
        screen.blit(error_text, error_rect)

    if game.paused:
        pause_text = SMALL_FONT.render("Paused", True, BLACK)
        pause_rect = pause_text.get_rect(center=(WINDOW_SIZE[0] // 2, game.grid_offset_y + game.grid_size * game.tile_size + 50))
        screen.blit(pause_text, pause_rect)

def draw_buttons(screen, mouse_pos, game):
    buttons = [
        ("Number Mode", PASTEL_GREEN, PASTEL_GREEN_HOVER, (game.grid_offset_x, game.grid_offset_y + game.grid_size * game.tile_size + 80, 120, 50)),
        ("Choose Image", PASTEL_BLUE, PASTEL_BLUE_HOVER, (game.grid_offset_x + 280, game.grid_offset_y + game.grid_size * game.tile_size + 80, 120, 50)),
        ("Shuffle", PASTEL_PINK, PASTEL_PINK_HOVER, (game.grid_offset_x, game.grid_offset_y + game.grid_size * game.tile_size + 140, 120, 50)),
        ("Auto Solve" if not game.solving or game.paused else "Pause", PASTEL_PURPLE, PASTEL_PURPLE_HOVER, (game.grid_offset_x + 140, game.grid_offset_y + game.grid_size * game.tile_size + 140, 120, 50)),
        ("Exit", PASTEL_ORANGE, PASTEL_ORANGE_HOVER, (game.grid_offset_x + 280, game.grid_offset_y + game.grid_size * game.tile_size + 140, 120, 50))
    ]
    game.hovered_button = None
    for text, color, hover_color, rect in buttons:
        if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
            pygame.draw.rect(screen, hover_color, rect, border_radius=15)
            game.hovered_button = text
        else:
            pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)
        if text in ["Choose Image", "Number Mode", "Auto Solve", "Pause"]:
            words = text.split()
            label1 = SMALL_FONT.render(words[0], True, BLACK)
            label2 = SMALL_FONT.render(words[1] if len(words) > 1 else "", True, BLACK)
            label1_rect = label1.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2 - 10))
            label2_rect = label2.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2 + 10))
            screen.blit(label1, label1_rect)
            if len(words) > 1:
                screen.blit(label2, label2_rect)
        else:
            label = SMALL_FONT.render(text, True, BLACK)
            label_rect = label.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
            screen.blit(label, label_rect)
    return buttons

def draw_stats_popup(screen, mouse_pos, game):
    popup_width, popup_height = 500, 330
    popup_x = (WINDOW_SIZE[0] - popup_width) // 2
    popup_y = (WINDOW_SIZE[1] - popup_height) // 2

    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 2, border_radius=10)

    title_text = SMALL_FONT.render("Solution", True, BLACK)
    screen.blit(title_text, (popup_x + 20, popup_y + 20))

    stats_lines = [
        f"Algorithm used: A* with Heuristic",
        f"A* solution steps: {game.initial_a_star_steps}",
        f"Total moves: {game.stats.get('steps', 0)}",
        f"Nodes expanded: {game.stats.get('nodes_expanded', 0)}",
        f"Total nodes in tree: {game.stats.get('total_nodes', 0)}",
        f"Search time: {game.stats.get('time', 0):.2f}s",
        f"Would you like to continue?"
    ]
    for i, line in enumerate(stats_lines):
        line_text = SMALL_FONT.render(line, True, BLACK)
        screen.blit(line_text, (popup_x + 20, popup_y + 50 + i * 30))

    buttons = [
        ("Continue", PASTEL_GREEN, PASTEL_GREEN_HOVER, (popup_x + 120, popup_y + popup_height - 60, 100, 40)),
        ("Exit", PASTEL_PINK, PASTEL_PINK_HOVER, (popup_x + popup_width - 220, popup_y + popup_height - 60, 100, 40))
    ]
    for text, color, hover_color, rect in buttons:
        if rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
            pygame.draw.rect(screen, hover_color, rect, border_radius=10)
        else:
            pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
        label = SMALL_FONT.render(text, True, BLACK)
        label_rect = label.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        screen.blit(label, label_rect)
    return buttons
# COPYRIGHT by Perfect Dragon King (PDK)