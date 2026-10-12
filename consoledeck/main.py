import argparse
import pygame
import pyperclip
import gui

from logic import (
    load_config,
    save_config,
    listen_to_serial,
    select_button,
    get_selected_button,
    deselect_button,
)

from gui import (
    init_pygame,
    draw_buttons,
    find_button_click,
)


def main(gui_mode):
    config = load_config()

    if gui_mode:
        init_pygame()
        pygame.key.set_repeat(300, 30)

        running = True

        while running:
            selected = get_selected_button()
            draw_buttons(config, selected)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected = get_selected_button()
                    click_consumed = False

                    # Click inside the URL input field
                    if (
                        selected
                        and gui.input_rect
                        and gui.input_rect.collidepoint(
                            mouse_x, mouse_y
                        )
                    ):
                        gui.input_active = True
                        click_consumed = True
                    else:
                        gui.input_active = False

                    # Click Cancel
                    if (
                        selected
                        and gui.cancel_button_rect
                        and gui.cancel_button_rect.collidepoint(
                            mouse_x, mouse_y
                        )
                    ):
                        gui.temp_config_type = None
                        gui.temp_config_value = None
                        gui.save_enabled = False
                        gui.save_clicked = False
                        gui.input_active = False

                        deselect_button()
                        click_consumed = True

                    # Click Save
                    if (
                        not click_consumed
                        and selected
                        and hasattr(gui, "save_button_rect")
                        and gui.save_button_rect
                        and gui.save_button_rect.collidepoint(
                            mouse_x, mouse_y
                        )
                    ):
                        current = config.get(
                            selected,
                            {"type": "none", "value": ""}
                        )

                        new_type = (
                            gui.temp_config_type
                            if gui.temp_config_type is not None
                            else current.get("type", "none")
                        )

                        new_value = (
                            gui.temp_config_value
                            if gui.temp_config_value is not None
                            else current.get("value", "")
                        )

                        if new_type == "none":
                            new_value = ""

                        config[selected] = {
                            "type": new_type,
                            "value": new_value
                        }

                        gui.temp_config_type = None
                        gui.temp_config_value = None
                        gui.save_enabled = False
                        gui.save_clicked = True

                        save_config(config)

                        gui.save_clicked = False

                    # Click LINK, EXE, or NONE
                    if (
                        not click_consumed
                        and selected
                        and hasattr(gui, "type_button_rects")
                    ):
                        for button_name, rect in (
                            gui.type_button_rects.items()
                        ):
                            if rect.collidepoint(
                                mouse_x, mouse_y
                            ):
                                action_type = button_name.lower()

                                gui.temp_config_type = action_type

                                if action_type == "none":
                                    gui.temp_config_value = ""
                                else:
                                    if gui.temp_config_value is None:
                                        gui.temp_config_value = (
                                            config.get(
                                                selected,
                                                {
                                                    "type": "none",
                                                    "value": ""
                                                }
                                            ).get("value", "")
                                        )

                                gui.save_enabled = gui.is_dirty(
                                    selected, config
                                )

                                click_consumed = True
                                break

                    # Click Browse
                    current_type = gui.temp_config_type or (
                        config.get(selected, {}).get("type")
                        if selected
                        else None
                    )

                    if (
                        not click_consumed
                        and selected
                        and current_type == "exe"
                        and hasattr(gui, "browse_button_rect")
                        and gui.browse_button_rect
                        and gui.browse_button_rect.collidepoint(
                            mouse_x, mouse_y
                        )
                    ):
                        from tkinter import filedialog
                        import tkinter as tk
                        import os

                        root = tk.Tk()
                        root.withdraw()

                        file_path = filedialog.askopenfilename(
                            title="Select Executable",
                            filetypes=[
                                ("Executable files", "*.exe")
                            ],
                            initialdir=os.path.expanduser("~")
                        )

                        if file_path:
                            gui.temp_config_value = file_path

                            gui.save_enabled = gui.is_dirty(
                                selected, config
                            )

                        root.destroy()
                        click_consumed = True

                    if click_consumed:
                        continue

                    # Click one of buttons 1–9
                    button = find_button_click(
                        mouse_x, mouse_y
                    )

                    if button:
                        select_button(button)

                        gui.temp_config_type = None
                        gui.temp_config_value = None
                        gui.save_enabled = False
                        gui.save_clicked = False
                        gui.input_active = False

                # Handle keyboard input in the URL field
                elif (
                    event.type == pygame.KEYDOWN
                    and gui.input_active
                ):
                    selected = get_selected_button()

                    if not selected:
                        gui.input_active = False
                        continue

                    active_type = (
                        gui.temp_config_type
                        if gui.temp_config_type is not None
                        else config.get(
                            selected, {"type": "none"}
                        ).get("type", "none")
                    )

                    if active_type != "link":
                        gui.input_active = False
                        continue

                    # Backspace
                    if event.key == pygame.K_BACKSPACE:
                        gui.temp_config_value = (
                            gui.temp_config_value or ""
                        )[:-1]

                    # Ctrl+V: Paste
                    elif (
                        event.key == pygame.K_v
                        and pygame.key.get_mods()
                        & pygame.KMOD_CTRL
                    ):
                        clipboard_text = pyperclip.paste()

                        if clipboard_text:
                            gui.temp_config_value = (
                                gui.temp_config_value or ""
                            ) + clipboard_text

                    # Ctrl+A: Select all
                    elif (
                        event.key == pygame.K_a
                        and pygame.key.get_mods()
                        & pygame.KMOD_CTRL
                    ):
                        # Text selection is not implemented.
                        pass

                    # Ctrl+C: Copy the entire field
                    elif (
                        event.key == pygame.K_c
                        and pygame.key.get_mods()
                        & pygame.KMOD_CTRL
                    ):
                        if gui.temp_config_value:
                            pyperclip.copy(
                                gui.temp_config_value
                            )

                    # Ctrl+X: Cut the entire field
                    elif (
                        event.key == pygame.K_x
                        and pygame.key.get_mods()
                        & pygame.KMOD_CTRL
                    ):
                        if gui.temp_config_value:
                            pyperclip.copy(
                                gui.temp_config_value
                            )

                            gui.temp_config_value = ""

                            gui.save_enabled = gui.is_dirty(
                                selected, config
                            )

                    # Type a character
                    else:
                        character = event.unicode

                        if character.isprintable():
                            gui.temp_config_value = (
                                gui.temp_config_value or ""
                            ) + character

                    gui.save_enabled = gui.is_dirty(
                        selected, config
                    )

        pygame.quit()

    else:
        listen_to_serial(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Start the configuration GUI"
    )

    args = parser.parse_args()

    main(args.gui)