import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
import signal
import requests
import pystray
from PIL import Image

# 定义图标路径
BLUE_ICON_PATH = "github_96px_blue.ico"
BLACK_ICON_PATH = "github_96px_black.ico"

# 获取资源文件路径的函数
# https://blog.csdn.net/Yibans/article/details/111305438
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 检查网络连接的函数
def check_network_connection():
    try:
        response = requests.get("https://github.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# 更新托盘图标的函数
def update_tray_icon():
    while True:
        if check_network_connection():
            icon.icon = Image.open(get_resource_path(BLUE_ICON_PATH))
        else:
            icon.icon = Image.open(get_resource_path(BLACK_ICON_PATH))
        time.sleep(10) # every 10 secs

# 退出程序的函数
def on_exit(icon, item):
    icon.stop()

# 创建系统托盘图标
icon = pystray.Icon("Github Network Checker")
icon.menu = pystray.Menu(
    pystray.MenuItem("Exit", on_exit)
)

# 设置初始图标
icon.icon = Image.open(get_resource_path(BLACK_ICON_PATH))

# 创建一个事件来控制线程的停止
stop_event = threading.Event()

# 启动更新图标的线程
threading.Thread(target=update_tray_icon, daemon=True).start()

icon.run()

signal.signal(signal.SIGINT, on_exit)
