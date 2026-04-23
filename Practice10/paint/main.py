import pygame
import sys

pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 100
STATUSBAR_HEIGHT = 35

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
BLUE = (50, 100, 220)
YELLOW = (255, 210, 0)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (90, 90, 90)
SELECTED = (180, 220, 255)

# Fonts
FONT = pygame.font.SysFont("Arial", 20)
SMALL_FONT = pygame.font.SysFont("Arial", 16)

# Canvas surface
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Current state
tool = "brush"
color = BLACK
radius = 8
drawing = False
start_pos = None
current_pos = None

# Toolbar buttons
tool_buttons = {
    "brush": pygame.Rect(20, 35, 80, 42),
    "rectangle": pygame.Rect(115, 35, 95, 42),
    "circle": pygame.Rect(225, 35, 85, 42),
    "eraser": pygame.Rect(325, 35, 90, 42),
    "clear": pygame.Rect(430, 35, 80, 42),
}

color_buttons = {
    BLACK: pygame.Rect(560, 35, 35, 35),
    RED: pygame.Rect(610, 35, 35, 35),
    GREEN: pygame.Rect(660, 35, 35, 35),
    BLUE: pygame.Rect(710, 35, 35, 35),
    YELLOW: pygame.Rect(760, 35, 35, 35),
}

size_box = pygame.Rect(850, 35, 90, 42)


def get_color_name(c):
    """Return readable color name."""
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
    """Draw one toolbar button."""
    fill = SELECTED if active else WHITE
    pygame.draw.rect(SCREEN, fill, rect, border_radius=8)
    pygame.draw.rect(SCREEN, BLACK, rect, 2, border_radius=8)

    label = FONT.render(text, True, BLACK)
    SCREEN.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))


def draw_toolbar():
    """Draw toolbar."""
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(SCREEN, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    SCREEN.blit(SMALL_FONT.render("Tools", True, BLACK), (20, 10))
    SCREEN.blit(SMALL_FONT.render("Colors", True, BLACK), (560, 10))
    SCREEN.blit(SMALL_FONT.render("Size", True, BLACK), (850, 10))

    draw_button(tool_buttons["brush"], "Brush", tool == "brush")
    draw_button(tool_buttons["rectangle"], "Rect", tool == "rectangle")
    draw_button(tool_buttons["circle"], "Circle", tool == "circle")
    draw_button(tool_buttons["eraser"], "Eraser", tool == "eraser")
    draw_button(tool_buttons["clear"], "Clear", False)

    for col, rect in color_buttons.items():
        pygame.draw.rect(SCREEN, col, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 2)
        if color == col:
            border = pygame.Rect(rect.x - 4, rect.y - 4, rect.width + 8, rect.height + 8)
            pygame.draw.rect(SCREEN, DARK_GRAY, border, 2)

    pygame.draw.rect(SCREEN, WHITE, size_box, border_radius=8)
    pygame.draw.rect(SCREEN, BLACK, size_box, 2, border_radius=8)

    txt = FONT.render(str(radius), True, BLACK)
    SCREEN.blit(txt, (size_box.centerx - txt.get_width() // 2, size_box.centery - txt.get_height() // 2))

    SCREEN.blit(SMALL_FONT.render("UP / DOWN", True, BLACK), (850, 82))


def draw_statusbar():
    """Draw bottom status bar."""
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (0, HEIGHT - STATUSBAR_HEIGHT, WIDTH, STATUSBAR_HEIGHT))
    pygame.draw.line(SCREEN, DARK_GRAY, (0, HEIGHT - STATUSBAR_HEIGHT), (WIDTH, HEIGHT - STATUSBAR_HEIGHT), 2)

    status = f"Tool: {tool}  |  Color: {get_color_name(color)}  |  Size: {radius}"
    txt = SMALL_FONT.render(status, True, BLACK)
    SCREEN.blit(txt, (10, HEIGHT - STATUSBAR_HEIGHT + 8))


def inside_drawing_area(pos):
    """Allow drawing only in the canvas area."""
    return TOOLBAR_HEIGHT <= pos[1] <= HEIGHT - STATUSBAR_HEIGHT


def draw_preview():
    """Preview rectangle or circle while dragging."""
    temp = canvas.copy()

    if drawing and start_pos and current_pos:
        if tool == "rectangle":
            x = min(start_pos[0], current_pos[0])
            y = min(start_pos[1], current_pos[1])
            w = abs(current_pos[0] - start_pos[0])
            h = abs(current_pos[1] - start_pos[1])
            pygame.draw.rect(temp, color, (x, y, w, h), 2)

        elif tool == "circle":
            center_x = (start_pos[0] + current_pos[0]) // 2
            center_y = (start_pos[1] + current_pos[1]) // 2
            rx = abs(current_pos[0] - start_pos[0]) // 2
            ry = abs(current_pos[1] - start_pos[1]) // 2
            circle_radius = min(rx, ry)
            pygame.draw.circle(temp, color, (center_x, center_y), circle_radius, 2)

    SCREEN.blit(temp, (0, 0))


def handle_toolbar_click(pos):
    """Handle toolbar clicks for tools and colors."""
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

            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    tool = "brush"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
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

            # Mouse button pressed
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

            # Mouse button released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = event.pos

                    if tool == "rectangle":
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        w = abs(end_pos[0] - start_pos[0])
                        h = abs(end_pos[1] - start_pos[1])
                        pygame.draw.rect(canvas, color, (x, y, w, h), 2)

                    elif tool == "circle":
                        center_x = (start_pos[0] + end_pos[0]) // 2
                        center_y = (start_pos[1] + end_pos[1]) // 2
                        rx = abs(end_pos[0] - start_pos[0]) // 2
                        ry = abs(end_pos[1] - start_pos[1]) // 2
                        circle_radius = min(rx, ry)
                        pygame.draw.circle(canvas, color, (center_x, center_y), circle_radius, 2)

                    start_pos = None
                    current_pos = None
                    last_pos = None

            # Mouse motion
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