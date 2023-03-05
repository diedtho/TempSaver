import os
import logging
import threading
import time
from pathlib import Path

import pyscreenshot
from pynput import mouse
from screeninfo import get_monitors


logging.basicConfig(filename='app.log', level=logging.DEBUG)

def take_screenshot(x, y, common_utils):
    m = get_monitors()
    screen_width, screen_height = m[0].width, m[0].height
    # Größe des Bereichs, der aufgenommen werden soll
    width, height = 1200, 1200
    # Berechnung der Koordinaten des Bereichs
    x1 = max(0, x - width // 2)
    y1 = max(0, y - height // 2)
    x2 = min(screen_width, x + width // 2)
    y2 = min(screen_height, y + height // 2)
    im = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    print(f'path to save: {common_utils.path_to_save}')
    filename = f"screenshot_{common_utils.count}.png"
    filepath = os.path.join(common_utils.path_to_save, filename)
    im.save(filepath)
    print('Screenshot was taken.')
    common_utils.count += 1

def check_command_change(common_utils):
    cmd_timestamp = os.path.getmtime(common_utils.cmd_path)
    if cmd_timestamp != common_utils.cmd_timestamp_last:
        common_utils.cmd_timestamp_last = cmd_timestamp
        save_all_files(common_utils)


def save_all_files(common_utils):
    Path(common_utils.path_to_save).mkdir(parents=True, exist_ok=True)
    # do file saving operations


def on_click(x, y, button, pressed, common_utils):
    if button == mouse.Button.left and pressed:
        take_screenshot(x, y, common_utils)
        save_files_thread = threading.Thread(target=save_all_files, args=(common_utils,))
        save_files_thread.start()
        check_command_change(common_utils)


def start_mouse_listener(common_utils):
    with mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, common_utils)) as listener:
        listener.join()


def main():
    common_utils = CommonUtilities()

    while True:
        start_mouse_listener(common_utils)
        time.sleep(1)


class CommonUtilities:

    def __init__(self):
        self.count = 0
        self.source_root = r'D:\Temp'
        self.dest_root = r'D:\Backup'
        self.cmd_path = os.path.join(self.source_root, 'INSCommand.ini')
        self.path_to_save = os.path.join(self.dest_root, 'tmp')

        self.cmd_timestamp_last = os.path.getmtime(self.cmd_path)

        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    main()
