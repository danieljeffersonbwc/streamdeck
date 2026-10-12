import os
import json
import subprocess
import webbrowser
import serial
import time
import ctypes

ARDUINO_PORT = "COM3"
BAUD_RATE = 9600

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

# Selected button state
selected_button = None

# Internal volume state
last_volume_value = 0
is_muted = False


def load_config():
    print(f"[DEBUG] Loading config from: {CONFIG_FILE}")

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            print("[DEBUG] Config loaded:", json.dumps(config, indent=2))
            return config

    else:
        print("[DEBUG] Config file not found. Creating default config.")

        config = {}

        for i in range(1, 10):
            config[f"BUTTON_{i}"] = {
                "type": "none",
                "value": ""
            }

        config["BUTTON_1"] = {
            "type": "link",
            "value": "https://www.youtube.com"
        }

        return config


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=2)


def execute_action(action):
    if action["type"] == "link" and action["value"]:
        webbrowser.open(action["value"])

    elif action["type"] == "exe" and action["value"]:
        try:
            subprocess.Popen(action["value"])
        except Exception as error:
            print("Error opening executable:", error)

    else:
        print("No action configured.")


def listen_to_serial(config):
    try:
        with serial.Serial(
            ARDUINO_PORT,
            BAUD_RATE,
            timeout=1
        ) as serial_connection:

            print(f"Connected to {ARDUINO_PORT}")

            while True:
                line = serial_connection.readline().decode(
                    "utf-8"
                ).strip()

                if line:
                    print("Received:", line)

                    if line.startswith("VOLUME_"):
                        value = line.replace("VOLUME_", "")
                        handle_volume(value)

                    elif line == "MUTE":
                        handle_mute()

                    elif line == "MEDIA":
                        handle_media()

                    elif line in config:
                        execute_action(config[line])

    except Exception as error:
        print(f"[ERROR] Serial port: {error}")
        time.sleep(5)
        listen_to_serial(config)


def simulate_keypress(virtual_key_code):
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002

    ctypes.windll.user32.keybd_event(
        virtual_key_code, 0, KEYEVENTF_EXTENDEDKEY, 0
    )

    ctypes.windll.user32.keybd_event(
        virtual_key_code,
        0,
        KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,
        0
    )


def handle_volume(value):
    global last_volume_value

    try:
        volume_value = int(value)
        delta = volume_value - last_volume_value

        if delta != 0:
            virtual_key = 0xAF if delta > 0 else 0xAE
            # VK_VOLUME_UP / VK_VOLUME_DOWN

            for _ in range(abs(delta)):
                simulate_keypress(virtual_key)

            print(f"[DEBUG] Volume adjusted by {delta}")

        last_volume_value = volume_value

    except ValueError:
        print("[ERROR] Invalid volume value:", value)


def handle_mute():
    global is_muted

    simulate_keypress(0xAD)  # VK_VOLUME_MUTE

    is_muted = not is_muted

    print(
        f"[DEBUG] Mute toggled -> "
        f"{'ON' if is_muted else 'OFF'}"
    )


def handle_media():
    simulate_keypress(0xB3)  # VK_MEDIA_PLAY_PAUSE
    print("[DEBUG] Media play/pause triggered")


def select_button(button):
    global selected_button

    selected_button = button

    print(f"[DEBUG] Selected button: {button}")


def deselect_button():
    global selected_button

    selected_button = None


def get_selected_button():
    return selected_button