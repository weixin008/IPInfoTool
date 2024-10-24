import requests
import tkinter as tk
from tkinter import Label, messagebox
import logging
import os
import random

# 设置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 随机选择请求头
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
]

class IPInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP和归属地")
        self.root.wm_attributes('-alpha', 0.6)
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.window_width = 220
        self.window_height = 150

        x_position = int(screen_width * 0.95) - self.window_width
        y_position = int(screen_height * 0.05)

        if x_position is None:
            x_position = 0
        if y_position is None:
            y_position = 0

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")

        self.message_label = Label(self.root, text="欢迎使用IP属地显示", font=("Helvetica", 10), justify="center")
        self.message_label.pack(fill='both')

        self.label = Label(self.root, text="", font=("Helvetica", 10), justify="left")
        self.label.pack(expand=True, fill='both', pady=(0, 5))  # 确保没有上部填充

        self.update_label()

        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<ButtonRelease-1>', self.stop_move)
        self.root.bind('<B1-Motion>', self.do_move)

        self.label.bind('<Button-1>', self.on_click)

    def check_permissions(self):
        return os.access('/', os.R_OK)

    def prompt_network_permission(self):
        response = messagebox.askyesno("权限检查", "当前没有网络访问权限，是否检查网络连接？")
        if response:
            try:
                requests.get('https://www.google.com', timeout=5)
                return True
            except requests.ConnectionError:
                messagebox.showerror("错误", "网络连接失败，请检查您的网络设置。")
                return False
        return False

    def get_public_ip_info(self):
        if not self.check_permissions():
            if not self.prompt_network_permission():
                return {'ip': 'N/A', 'country': 'N/A', 'region': 'N/A', 'city': 'N/A', 'error': '权限不足'}

        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS)
            }
            response = requests.get('http://ip-api.com/json/?lang=zh-CN', headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()

            ip = data.get('query', 'N/A')
            country = data.get('country', 'N/A')
            region = data.get('regionName', 'N/A')
            city = data.get('city', 'N/A')

            return {'ip': ip, 'country': country, 'region': region, 'city': city}
        except requests.exceptions.RequestException as e:
            logging.error(f"网络请求错误: {e}")
            return {'ip': 'N/A', 'country': 'N/A', 'region': 'N/A', 'city': 'N/A', 'error': f"网络错误: {str(e)}"}

    def show_message(self, text, color):
        self.message_label.config(text=text, bg=color)
        self.root.after(0, self.fade_in)
        
    def fade_in(self, step=0):
        if step <= 20:
            alpha = step / 20
            self.message_label.config(bg=self.message_label.cget("bg"), fg='black')
            self.message_label.master.wm_attributes('-alpha', 0.6 + 0.4 * alpha)
            self.root.after(50, self.fade_in, step + 1)
        else:
            self.root.after(2000, self.fade_out)

    def fade_out(self, step=20):
        if step >= 0:
            alpha = step / 20
            self.message_label.master.wm_attributes('-alpha', 0.6 + 0.4 * alpha)
            self.root.after(50, self.fade_out, step - 1)
        else:
            self.message_label.config(text="欢迎使用IP属地显示", bg='SystemButtonFace')

    def update_label(self):
        public_info = self.get_public_ip_info()

        if 'error' in public_info:
            info = f"错误: {public_info['error']}"
            self.show_message("更新失败", "#FFCCCC")
        else:
            info = (f"外网IP: {public_info['ip']}\n"
                    f"国家: {public_info['country']}\n"
                    f"地区: {public_info['region']}\n"
                    f"城市: {public_info['city']}")
            self.show_message("更新成功", "#CCFFCC")

        self.label.config(text=info, wraplength=0)
        self.root.geometry(f"{self.window_width}x{self.window_height}")

    def on_click(self, event):
        self.update_label()

    def start_move(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def stop_move(self, event):
        self.root.x = None
        self.root.y = None

    def do_move(self, event):
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPInfoApp(root)
    root.mainloop()
