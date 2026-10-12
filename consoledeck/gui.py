import pygame
import os
import tkinter as tk
from tkinter import filedialog
import webbrowser

from logic import execute_action


# Global constants
FONT = None
SMALL_FONT = None
SCREEN = None

BUTTON_SIZE = 100
SPACING_X = 140
SPACING_Y = 120
MARGIN_Y = 20

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 650


# GUI button rectangles
cancel_button_rect = None
browse_button_rect = None
save_button_rect = None
type_button_rects = {}

# Temporary configuration values
temp_config_type = None
temp_config_value = None

save_enabled = False
save_clicked = False

input_active = False
input_rect = None


def init_pygame():
    global FONT, SMALL_FONT, SCREEN

    pygame.init()

    FONT = pygame.font.SysFont(None, 24)
    SMALL_FONT = pygame.font.SysFont(None, 16)

    SCREEN = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("ConsoleDeck V2")


def draw_buttons(config, selected=None):
    SCREEN.fill((30, 30, 30))

    button_size = BUTTON_SIZE
    spacing_x = SPACING_X
    spacing_y = SPACING_Y

    total_width = (
        3 * button_size
        + 2 * (spacing_x - button_size)
    )

    start_x = (SCREEN_WIDTH - total_width) // 2
    margin_y = MARGIN_Y

    for i in range(9):
        key = f"BUTTON_{i + 1}"

        x = start_x + (i % 3) * spacing_x
        y = margin_y + (i // 3) * spacing_y

        # Button background
        pygame.draw.rect(
            SCREEN,
            (50, 50, 50),
            (x, y, button_size, button_size),
            border_radius=8
        )

        # Button border
        if selected == key:
            border_color = (200, 120, 40)
        else:
            border_color = (200, 200, 200)

        pygame.draw.rect(
            SCREEN,
            border_color,
            (x, y, button_size, button_size),
            width=3,
            border_radius=8
        )

        # Centered button number
        number_text = FONT.render(
            str(i + 1), True, (255, 255, 255)
        )

        number_x = x + (
            button_size - number_text.get_width()
        ) // 2

        number_y = y + (
            button_size - number_text.get_height()
        ) // 2

        SCREEN.blit(number_text, (number_x, number_y))

    # Divider line
    line_y = margin_y + 3 * spacing_y + 5

    pygame.draw.line(
        SCREEN,
        (180, 180, 180),
        (start_x, line_y),
        (start_x + total_width, line_y),
        2
    )

    font_18 = pygame.font.SysFont(None, 18)

    if selected:
        message = f"Program button {selected[-1]}"
    else:
        message = "Click on a button to program it"

    message_render = font_18.render(
        message, True, (255, 255, 255)
    )

    message_area_y = line_y + 10
    message_area_height = button_size

    message_x = (
        SCREEN_WIDTH - message_render.get_width()
    ) // 2

    message_y = message_area_y + (
        message_area_height - message_render.get_height()
    ) // 2

    SCREEN.blit(message_render, (message_x, message_y))

    if selected:
        draw_advanced_configurator(selected, config)

    pygame.display.flip()


def draw_advanced_configurator(selected, config):
    global type_button_rects
    global cancel_button_rect
    global input_rect
    global browse_button_rect
    global temp_config_type
    global temp_config_value
    global save_button_rect

    small_font = pygame.font.SysFont(None, 16)

    data = config.get(
        selected,
        {"type": "none", "value": ""}
    )

    action_type = (
        temp_config_type
        if temp_config_type is not None
        else data.get("type", "none")
    )

    action_value = (
        temp_config_value
        if temp_config_value is not None
        else data.get("value", "")
    )

    options = ["LINK", "EXE", "NONE"]

    base_y = 460
    button_width = 120
    button_height = 40
    spacing = 20

    total_width = (
        len(options) * button_width
        + (len(options) - 1) * spacing
    )

    start_x = (SCREEN_WIDTH - total_width) // 2

    type_button_rects = {}
    input_rect = None
    browse_button_rect = None

    # Action type buttons
    for i, button_name in enumerate(options):
        x = start_x + i * (button_width + spacing)
        y = base_y

        is_active = button_name.lower() == action_type

        color = (
            (200, 120, 40)
            if is_active
            else (80, 80, 80)
        )

        rect = pygame.Rect(
            x, y, button_width, button_height
        )

        type_button_rects[button_name] = rect

        pygame.draw.rect(
            SCREEN, color, rect, border_radius=6
        )

        button_text = small_font.render(
            button_name, True, (255, 255, 255)
        )

        SCREEN.blit(
            button_text,
            button_text.get_rect(center=rect.center)
        )

    base_y += button_height + 15

    # URL input field
    if action_type == "link":
        label = small_font.render(
            "ENTER URL:", True, (200, 200, 200)
        )

        SCREEN.blit(label, (50, base_y))

        base_y += label.get_height() + 5

        input_rect = pygame.Rect(
            50, base_y, 540, 30
        )

        pygame.draw.rect(
            SCREEN,
            (255, 255, 255),
            input_rect,
            border_radius=4
        )

        text_color = (0, 0, 0)
        url_text = action_value if action_value else ""

        rendered_text = small_font.render(
            url_text, True, text_color
        )

        SCREEN.blit(
            rendered_text,
            (input_rect.x + 5, input_rect.y + 7)
        )

        base_y += 40

    # Executable file selection
    elif action_type == "exe":
        label = small_font.render(
            "SELECT EXECUTABLE FILE:",
            True,
            (200, 200, 200)
        )

        SCREEN.blit(label, (50, base_y))

        base_y += label.get_height() + 5

        browse_rect = pygame.Rect(
            50, base_y, 100, 30
        )

        pygame.draw.rect(
            SCREEN,
            (200, 120, 40),
            browse_rect,
            border_radius=5
        )

        button_text = small_font.render(
            "BROWSE", True, (255, 255, 255)
        )

        SCREEN.blit(
            button_text,
            button_text.get_rect(center=browse_rect.center)
        )

        browse_button_rect = browse_rect

        base_y += 40

    # Cancel and Save buttons
    button_y = base_y + 20

    total_button_width = 80 + 20 + 80
    start_x = (SCREEN_WIDTH - total_button_width) // 2

    cancel_text = small_font.render(
        "Cancel", True, (200, 120, 40)
    )

    cancel_text_rect = cancel_text.get_rect()

    SCREEN.blit(
        cancel_text,
        (
            start_x,
            button_y
            + (30 - cancel_text_rect.height) // 2
        )
    )

    cancel_button_rect = pygame.Rect(
        start_x, button_y, 60, 30
    )

    save_rect = pygame.Rect(
        start_x + 100, button_y, 80, 30
    )

    if save_clicked:
        save_color = (200, 120, 40)
    elif save_enabled:
        save_color = (200, 120, 40)
    else:
        save_color = (100, 100, 100)

    pygame.draw.rect(
        SCREEN,
        save_color,
        save_rect,
        border_radius=5
    )

    save_text = small_font.render(
        "Save", True, (255, 255, 255)
    )

    SCREEN.blit(
        save_text,
        save_text.get_rect(center=save_rect.center)
    )

    # Store the clickable Save button rectangle
    save_button_rect = save_rect


def is_dirty(selected, config):
    global temp_config_type, temp_config_value

    if not selected:
        return False

    current = config.get(
        selected,
        {"type": "none", "value": ""}
    )

    action_type = (
        temp_config_type
        if temp_config_type is not None
        else current["type"]
    )

    action_value = (
        temp_config_value
        if temp_config_value is not None
        else current["value"]
    )

    return (
        action_type != current["type"]
        or action_value != current["value"]
    )


def find_button_click(mouse_x, mouse_y):
    total_width = (
        3 * BUTTON_SIZE
        + 2 * (SPACING_X - BUTTON_SIZE)
    )

    start_x = (SCREEN_WIDTH - total_width) // 2

    for i in range(9):
        x = start_x + (i % 3) * SPACING_X
        y = MARGIN_Y + (i // 3) * SPACING_Y

        if (
            x <= mouse_x <= x + BUTTON_SIZE
            and y <= mouse_y <= y + BUTTON_SIZE
        ):
            return f"BUTTON_{i + 1}"

    return None


def configure_button(button_key, config):
    root = tk.Tk()
    root.title(f"Configure {button_key}")

    action_type_var = tk.StringVar(root)
    action_type_var.set(config[button_key]["type"])

    action_value_var = tk.StringVar(root)
    action_value_var.set(
        config[button_key].get("value", "")
    )

    def update_value_widgets(action_type):
        for widget in root.pack_slaves():
            if getattr(widget, "is_value_widget", False):
                widget.destroy()

        if action_type == "link":
            tk.Label(
                root, text="Enter URL:"
            ).pack()

            entry = tk.Entry(
                root,
                width=50,
                textvariable=action_value_var
            )

            entry.pack()
            entry.is_value_widget = True

            tk.Button(
                root,
                text="Test Action",
                command=lambda: webbrowser.open(
                    action_value_var.get()
                )
            ).pack()

            tk.Button(
                root,
                text="Save",
                command=save
            ).pack()

        elif action_type == "exe":

            def browse_for_executable():
                file_path = filedialog.askopenfilename(
                    title="Select Executable",
                    filetypes=[
                        ("Executable files", "*.exe")
                    ]
                )

                if file_path:
                    action_value_var.set(file_path)

            tk.Button(
                root,
                text="Choose .exe File",
                command=browse_for_executable
            ).pack()

            file_label = tk.Label(
                root,
                textvariable=action_value_var
            )

            file_label.pack()
            file_label.is_value_widget = True

            tk.Button(
                root,
                text="Test Action",
                command=lambda: execute_action({
                    "type": "exe",
                    "value": action_value_var.get()
                })
            ).pack()

            tk.Button(
                root,
                text="Save",
                command=save
            ).pack()

    def save():
        action_type = action_type_var.get()
        action_value = action_value_var.get()

        if action_type != "none":
            config[button_key] = {
                "type": action_type,
                "value": action_value
            }
        else:
            config[button_key] = {
                "type": "none",
                "value": ""
            }

        root.destroy()

    tk.Label(
        root,
        text="Select Action Type:"
    ).pack()

    tk.OptionMenu(
        root,
        action_type_var,
        "link",
        "exe",
        "none",
        command=update_value_widgets
    ).pack()

    update_value_widgets(action_type_var.get())

    root.mainloop()