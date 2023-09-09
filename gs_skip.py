import time

import keyboard
import yaml
from loguru import logger

from ui import UI, ImageButton, wait_secs, show


PASS = "PASS"

interact_button = ImageButton(
    "images/interact.jpg",
    crop_posi=[1079, 320, 1162, 930],
    threshold=0.99,  # mask=True
)
dialogue_button = ImageButton(
    "images/dialogue.jpg",
    crop_posi=[1140, 320, 1223, 930],
    threshold=0.99,
)


def pick_up_task(ui: UI):
    actions = ui.actions
    if ui.match_button(interact_button):
        x0, y0 = interact_button.crop_posi[:2]
        x, y = interact_button.max_loc
        dialogue_button.crop_posi = [
            x0 + x + 50,
            y0 + y - 20,
            x0 + x + 360,
            y0 + y + 60,
        ]
        if ui.match_button(dialogue_button):
            return
        posi = [x0 + x + 110, y0 + y + 5, x0 + x + 210, y0 + y + 30]
        if ui.is_crop_zero(posi):
            return
        logger.info("pick up")
        actions.pick_up()
    return PASS


play0_button = ImageButton(
    "images/play0.jpg", crop_posi=[45, 26, 99, 77], threshold=0.99
)
play1_button = ImageButton(
    "images/play1.jpg", crop_posi=[45, 26, 99, 77], threshold=0.99
)
paim_button = ImageButton(
    "images/paim.jpg", crop_posi=[11, 11, 106, 103], threshold=0.99
)
task_button = ImageButton(
    "images/task.jpg", crop_posi=[24, 170, 95, 248], threshold=0.99, mask=True
)
skip_dialogue_button = ImageButton(
    "images/dialogue.jpg",
    crop_posi=[1266, 763, 1326, 855],
    threshold=0.99,
)


def skip_dialogue_task(ui: UI):
    actions = ui.actions
    if ui.match_button(play1_button) or ui.match_button(play0_button):
        logger.info("skip dialogue start")
        while not PAUSED:
            ui.new_capture(0.2)
            if ui.match_button(paim_button) or ui.match_button(task_button):
                wait_secs("skip dialogue end", 0.3)
                break
            if ui.match_button(skip_dialogue_button):
                actions.move_and_click(skip_dialogue_button.click_position)
                continue
            actions.skip_dialogue()


def run_task():
    ui = UI()
    if not ui.handle:
        wait_secs("window not found", 3)
        return
    if ui.capture is None:
        wait_secs("window resolution ", 3.0)
        return
    tasklist = [
        pick_up_task,
        skip_dialogue_task,
    ]
    for task in tasklist:
        ret = task(ui)
        if ret is None:
            return
        if ret == PASS:
            pass


PAUSED = False


def tasks_pause(e=None):
    global PAUSED
    PAUSED = not PAUSED
    if PAUSED:
        logger.info("tasks paused")
    else:
        logger.info("tasks resumed")


def pause_key():
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    return data["tasks_pause"]


def main():
    delta = 1 / 50
    keyboard.on_press_key("pause", tasks_pause)
    keyboard.add_hotkey(pause_key(), tasks_pause)
    while True:
        start_time = time.time()
        if not PAUSED:
            run_task()
        else:
            wait_secs("program paused.", 3)
        run_time = time.time() - start_time
        sleep_time = delta - run_time
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()
