import pygame
import sys
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 110
STATUSBAR_HEIGHT = 35

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
BLUE = (50, 100, 220)
YELLOW = (255, 210, 0)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (90, 90, 90)
SELECTED = (180, 220, 255)

FONT = pygame.font.SysFont("Arial", 18)
SMALL_FONT = pygame.font.SysFont("Arial", 15)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

tool = "brush"
color = BLACK
radius = 8
drawing = False
start_pos = None
current_pos = None

tool_buttons = {
    "brush": pygame.Rect(20, 35, 80, 42),
    "rectangle": pygame.Rect(110, 35, 90, 42),
    "circle": pygame.Rect(210, 35, 80, 42),
    "eraser": pygame.Rect(300, 35, 90, 42),
    "square": pygame.Rect(400, 35, 80, 42),
    "r_triangle": pygame.Rect(490, 35, 110, 42),
    "e_triangle": pygame.Rect(610, 35, 120, 42),
    "rhombus": pygame.Rect(740, 35, 100, 42),
    "clear": pygame.Rect(850, 35, 80, 42),
}

color_buttons = {
    BLACK: pygame.Rect(120, 80, 30, 20),
    RED: pygame.Rect(160, 80, 30, 20),
    GREEN: pygame.Rect(200, 80, 30, 20),
    BLUE: pygame.Rect(240, 80, 30, 20),
    YELLOW: pygame.Rect(280, 80, 30, 20),
}


def get_color_name(c):
    if c == BLACK:
        return "Black"
    if c == RED:
        return "Red"
    if c == GREEN:
        return "Green"
    if c == BLUE:
        return "Blue"
    if c == YELLOW:
        return "Yellow"
    if c == WHITE:
        return "White"
    return str(c)


def draw_button(rect, text, active=False):
    fill = SELECTED if active else WHITE
    pygame.draw.rect(SCREEN, fill, rect, border_radius=8)
    pygame.draw.rect(SCREEN, BLACK, rect, 2, border_radius=8)

    label = SMALL_FONT.render(text, True, BLACK)
    SCREEN.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))


def draw_toolbar():
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(SCREEN, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    SCREEN.blit(SMALL_FONT.render("Tools", True, BLACK), (20, 10))
    SCREEN.blit(SMALL_FONT.render("Colors (1-5)", True, BLACK), (20, 82))
    SCREEN.blit(SMALL_FONT.render("UP / DOWN = Size", True, BLACK), (360, 82))

    for name, rect in tool_buttons.items():
        draw_button(rect, name, tool == name)

    for col, rect in color_buttons.items():
        pygame.draw.rect(SCREEN, col, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 2)
        if color == col:
            border = pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6)
            pygame.draw.rect(SCREEN, DARK_GRAY, border, 2)

    size_text = FONT.render(f"Size: {radius}", True, BLACK)
    SCREEN.blit(size_text, (500, 80))


def draw_statusbar():
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (0, HEIGHT - STATUSBAR_HEIGHT, WIDTH, STATUSBAR_HEIGHT))
    pygame.draw.line(SCREEN, DARK_GRAY, (0, HEIGHT - STATUSBAR_HEIGHT), (WIDTH, HEIGHT - STATUSBAR_HEIGHT), 2)

    status = f"Tool: {tool} | Color: {get_color_name(color)} | Size: {radius}"
    txt = SMALL_FONT.render(status, True, BLACK)
    SCREEN.blit(txt, (10, HEIGHT - STATUSBAR_HEIGHT + 8))


def inside_drawing_area(pos):
    x, y = pos
    return TOOLBAR_HEIGHT <= y <= HEIGHT - STATUSBAR_HEIGHT


def draw_equilateral_triangle(surface, color, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    if side < 1:
        return

    if x2 >= x1:
        base_left = (x1, y2)
        base_right = (x1 + side, y2)
        top = (x1 + side // 2, int(y2 - (side * math.sqrt(3) / 2)))
    else:
        base_left = (x1 - side, y2)
        base_right = (x1, y2)
        top = (x1 - side // 2, int(y2 - (side * math.sqrt(3) / 2)))

    pygame.draw.polygon(surface, color, [base_left, base_right, top], width)


def draw_shape_preview(surface):
    if not (drawing and start_pos and current_pos):
        return

    if tool == "rectangle":
        x = min(start_pos[0], current_pos[0])
        y = min(start_pos[1], current_pos[1])
        w = abs(current_pos[0] - start_pos[0])
        h = abs(current_pos[1] - start_pos[1])
        pygame.draw.rect(surface, color, (x, y, w, h), 2)

    elif tool == "circle":
        center_x = (start_pos[0] + current_pos[0]) // 2
        center_y = (start_pos[1] + current_pos[1]) // 2
        rx = abs(current_pos[0] - start_pos[0]) // 2
        ry = abs(current_pos[1] - start_pos[1]) // 2
        circle_radius = min(rx, ry)
        pygame.draw.circle(surface, color, (center_x, center_y), circle_radius, 2)

    elif tool == "square":
        size = min(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
        x = start_pos[0]
        y = start_pos[1]

        if current_pos[0] < start_pos[0]:
            x = start_pos[0] - size
        if current_pos[1] < start_pos[1]:
            y = start_pos[1] - size

        pygame.draw.rect(surface, color, (x, y, size, size), 2)

    elif tool == "r_triangle":
        points = [start_pos, (start_pos[0], current_pos[1]), current_pos]
        pygame.draw.polygon(surface, color, points, 2)

    elif tool == "e_triangle":
        draw_equilateral_triangle(surface, color, start_pos, current_pos, 2)

    elif tool == "rhombus":
        x1, y1 = start_pos
        x2, y2 = current_pos
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, color, points, 2)


def draw_preview():
    preview_surface = canvas.copy()
    draw_shape_preview(preview_surface)
    SCREEN.blit(preview_surface, (0, 0))


def handle_toolbar_click(pos):
    global tool, color

    for name, rect in tool_buttons.items():
        if rect.collidepoint(pos):
            if name == "clear":
                canvas.fill(WHITE)
            else:
                tool = name
            return

    for col, rect in color_buttons.items():
        if rect.collidepoint(pos):
            color = col
            return


def finalize_shape():
    if not (start_pos and current_pos):
        return

    if tool == "rectangle":
        x = min(start_pos[0], current_pos[0])
        y = min(start_pos[1], current_pos[1])
        w = abs(current_pos[0] - start_pos[0])
        h = abs(current_pos[1] - start_pos[1])
        pygame.draw.rect(canvas, color, (x, y, w, h), 2)

    elif tool == "circle":
        center_x = (start_pos[0] + current_pos[0]) // 2
        center_y = (start_pos[1] + current_pos[1]) // 2
        rx = abs(current_pos[0] - start_pos[0]) // 2
        ry = abs(current_pos[1] - start_pos[1]) // 2
        circle_radius = min(rx, ry)
        pygame.draw.circle(canvas, color, (center_x, center_y), circle_radius, 2)

    elif tool == "square":
        size = min(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
        x = start_pos[0]
        y = start_pos[1]

        if current_pos[0] < start_pos[0]:
            x = start_pos[0] - size
        if current_pos[1] < start_pos[1]:
            y = start_pos[1] - size

        pygame.draw.rect(canvas, color, (x, y, size, size), 2)

    elif tool == "r_triangle":
        points = [start_pos, (start_pos[0], current_pos[1]), current_pos]
        pygame.draw.polygon(canvas, color, points, 2)

    elif tool == "e_triangle":
        draw_equilateral_triangle(canvas, color, start_pos, current_pos, 2)

    elif tool == "rhombus":
        x1, y1 = start_pos
        x2, y2 = current_pos
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(canvas, color, points, 2)


def main():
    global tool, color, radius, drawing, start_pos, current_pos

    clock = pygame.time.Clock()
    last_pos = None

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    tool = "brush"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "r_triangle"
                elif event.key == pygame.K_q:
                    tool = "e_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_1:
                    color = BLACK
                elif event.key == pygame.K_2:
                    color = RED
                elif event.key == pygame.K_3:
                    color = GREEN
                elif event.key == pygame.K_4:
                    color = BLUE
                elif event.key == pygame.K_5:
                    color = YELLOW
                elif event.key == pygame.K_UP:
                    radius += 1
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 1)
                elif event.key == pygame.K_SPACE:
                    canvas.fill(WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] < TOOLBAR_HEIGHT:
                        handle_toolbar_click(event.pos)
                    elif inside_drawing_area(event.pos):
                        drawing = True
                        start_pos = event.pos
                        current_pos = event.pos
                        last_pos = event.pos

                        if tool == "brush":
                            pygame.draw.circle(canvas, color, event.pos, radius)
                        elif tool == "eraser":
                            pygame.draw.circle(canvas, WHITE, event.pos, radius)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    current_pos = event.pos

                    if tool in ["rectangle", "circle", "square", "r_triangle", "e_triangle", "rhombus"]:
                        finalize_shape()

                    start_pos = None
                    current_pos = None
                    last_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                if inside_drawing_area(event.pos):
                    current_pos = event.pos

                    if tool == "brush":
                        pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                        last_pos = event.pos
                    elif tool == "eraser":
                        pygame.draw.line(canvas, WHITE, last_pos, event.pos, radius * 2)
                        last_pos = event.pos

        SCREEN.fill(WHITE)
        draw_preview()
        draw_toolbar()
        draw_statusbar()
        pygame.display.update()


if __name__ == "__main__":
    main()
