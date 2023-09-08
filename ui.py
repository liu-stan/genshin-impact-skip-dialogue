import ctypes
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import time

import numpy as np
import pyautogui
import cv2
from loguru import logger


WINDOWTITLE = ['Genshin Impact', '原神']
WINDOWBORDER = [0, 35]

GetDC = ctypes.windll.user32.GetDC
CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
GetWindowRect  = ctypes.windll.user32.GetWindowRect 
GetClientRect = ctypes.windll.user32.GetClientRect
CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
SelectObject = ctypes.windll.gdi32.SelectObject
BitBlt = ctypes.windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = ctypes.windll.gdi32.GetBitmapBits
DeleteObject = ctypes.windll.gdi32.DeleteObject
ReleaseDC = ctypes.windll.user32.ReleaseDC
GetWindowTextW = ctypes.windll.user32.GetWindowTextW
GetWindowTextLengthW = ctypes.windll.user32.GetWindowTextLengthW

ctypes.windll.user32.SetProcessDPIAware()


def capture_window(handle: HWND):
    """
    return numpy.ndarray
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # return numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

def get_capture(handle: HWND):
    _ret = capture_window(handle)
    cap = _ret[:, :,:3]
    return cap


def enum_win(hwnd, handle2win_titles):
    if all((
        windll.user32.IsWindow(hwnd), 
        windll.user32.IsWindowEnabled(hwnd), 
        windll.user32.IsWindowVisible(hwnd)
    )):
        handle2win_titles.update({ hwnd: windll.user32.GetWindowText(hwnd) })

def get_window_title(handle: HWND):
    length = GetWindowTextLengthW(handle)
    buff = ctypes.create_unicode_buffer(length)
    GetWindowTextW(handle, buff, length + 1)
    window_title =  buff.value
    return window_title


def get_handle():
    handle = windll.user32.GetForegroundWindow()
    title = get_window_title(handle)
    if title in  WINDOWTITLE:
        return handle

def get_rect():
    rect = RECT()
    handle = get_handle()
    GetWindowRect(handle, ctypes.byref(rect))
    return rect

def wait_secs(msg, secs):
    logger.info(f'{msg} wait {secs} seconds.')
    time.sleep(secs)

def active(func):
    def wrapper(*args, **kwargs):
        handle = get_handle()
        if handle:
            result = func(*args, **kwargs)
            return result
        else:
            wait_secs('window window not found ', 3.0)
    return wrapper


def show(image, name=None):
    import random
    if isinstance(image, list):
        for i in image:
            name = f'image-{random.random()}'
            cv2.imshow(name, i)
    else:
        cv2.imshow(name, image)
    cv2.waitKey()

def crop(image, rect):
    """
    rect: left, top, right, bottom
    """
    left, top, right, bottom = rect
    return image[top:bottom, left:right]


class Actions:

    @active
    def pres_key(self, key):
        pyautogui.press(key)

    def pick_up(self, ):
        self.pres_key('f')

    def skip_dialogue(self, ):
        self.pres_key('space')

    def _mouse_position(self, position):
        rect = get_rect()
        border_left, border_top = WINDOWBORDER
        x, y = rect.left + position[0] + border_left, rect.top + position[1] + border_top
        return x, y
    
    @active
    def move_and_click(self, position, delay=0.3):
        x, y = self._mouse_position(position)
        time.sleep(delay)
        pyautogui.moveTo(x, y)
        pyautogui.leftClick()
    
    @active
    def move_to(self, position, delay=0.3):
        x, y = self._mouse_position(position)
        time.sleep(delay)
        pyautogui.moveTo(x, y)

class ImageButton:
    def __init__(self, filepath, crop_posi, threshold=0.9,  mask=None) -> None:
        self._filepath = filepath
        self.image = cv2.imread(filepath)
        if mask:
            self.mask = cv2.imread(filepath.replace('.jpg', '-mask.jpg'))
        else:
            self.mask = None
        self.threshold=threshold
        self.crop_posi = crop_posi
        self.max_val = None
        self.max_loc = None

    def show(self):
        show(self.image)

    @property
    def click_position(self):
        if self.max_loc is None:
            raise Exception('max_loc is None')
        left, top, _, _ = self.crop_posi
        return left + self.max_loc[0], top + self.max_loc[1]

    def __str__(self) -> str:
        return f'ImageButton(filepath="{self._filepath}")'

class UI:
    def __init__(self, ):
        self.handle  = get_handle()
        self.actions = Actions()
        self._capture = get_capture(self.handle)
        self._title = None
        self._chat_name = None
        self._crop = None
    
    @property
    def capture(self):
        return self._capture
    
    def new_capture(self, delay: float = 0 ):
        """
        sleep delay secs and return a new capture
        """
        time.sleep(delay)
        self._capture = get_capture(self.handle)
        return self._capture

    @property
    def chat_name(self):
        return self._chat_name
    
    @chat_name.setter
    def chat_name(self, name):
        self._chat_name = name

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title

    def show_capture(self):
        show(self.capture, 'ui capture')

    def show_capture(self):
        show(self._crop, 'ui crop')

    def crop(self, posi):
        self._crop = crop(self._capture, posi)
        return self._crop

    def match_button(self, image_button: ImageButton, method=cv2.TM_CCORR_NORMED):
        if image_button.crop_posi is not None:
            image = self.crop(image_button.crop_posi)
        else:
            image = self.capture
        template = image_button.image
        mask = image_button.mask
        result = cv2.matchTemplate(image, template, method, mask=mask)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        image_button.max_val = max_val
        image_button.max_loc = max_loc
        return max_val >= image_button.threshold
        

if __name__ == "__main__":
    ui = UI()
    ui.new_capture(3)
    ui.show_capture()
