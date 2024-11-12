import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk

# 初始化 CustomTkinter
ctk.set_appearance_mode("light")  # 设置主题为浅色
ctk.set_default_color_theme("blue")  # 主题色

class PlantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Plant Importer")
        self.geometry("300x500")  # 设置窗口大小
        self.imported_image = None  # 保存导入的图片
        self.photo_ref = None       # 保持图片引用
        
        # 昰显示植物图片的标签
        self.image_label = ctk.CTkLabel(self, text="", width=300, height=300)  # 清空 text 属性
        self.image_label.pack(pady=20)
        
        # 导入按钮
        import_button = ctk.CTkButton(self, text="Import", command=self.import_image)
        import_button.pack(pady=10)
        
        # 生成按钮
        generate_button = ctk.CTkButton(self, text="Generate", command=self.open_music_player)
        generate_button.pack(pady=10)

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300), Image.LANCZOS)  # 使用 LANCZOS 替代 ANTIALIAS
            
            # 创建圆形掩模
            mask = Image.new('L', (300, 300), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 300, 300), fill=255)

            # 使用掩模将图片裁剪成圆形
            image.putalpha(mask)
            self.photo_ref = ImageTk.PhotoImage(image)  # 保存引用
            self.image_label.configure(image=self.photo_ref, text="")  # 清空 text
            self.imported_image = self.photo_ref  # 保存导入的图片以便传递到音乐播放器界面

    def open_music_player(self):
        if self.imported_image:
            # 获取当前窗口的大小
            music_player = MusicPlayer(self, self.imported_image)
            music_player.grab_set()  # 抓取焦点到新窗口
        else:
            print("Please import an image first.")

class MusicPlayer(ctk.CTkToplevel):
    def __init__(self, parent, imported_image):
        super().__init__(parent)  # 创建 Toplevel 窗口
        
        self.title("Music Player")
        
        # 设置窗口大小
        self.geometry("300x500")
        self.imported_image = imported_image  # 保持图片引用
        
        # 显示传递过来的植物图片
        image_label = ctk.CTkLabel(self, image=self.imported_image, width=300, height=300, text="")  # 清空 text
        image_label.pack(pady=20)
        
        # 创建控制按钮（上一首、播放/暂停、下一首）
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10)
        
        # 加载按钮图标并统一调整大小为 50x50
        icon_size = (50, 50)  # 统一图标大小
        
        prev_icon = Image.open("prev.png").resize(icon_size)
        prev_icon = ImageTk.PhotoImage(prev_icon)
        
        play_icon = Image.open("play.png").resize(icon_size)
        play_icon = ImageTk.PhotoImage(play_icon)
        
        next_icon = Image.open("next.png").resize(icon_size)
        next_icon = ImageTk.PhotoImage(next_icon)

        # 创建按钮并使用图标，同时去掉背景和文本
        prev_button = ctk.CTkButton(control_frame, image=prev_icon, width=50, height=50, text="", border_width=0, fg_color="transparent", command=self.previous_track)
        prev_button.grid(row=0, column=0, padx=5)
        
        self.play_pause_button = ctk.CTkButton(control_frame, image=play_icon, width=50, height=50, text="", border_width=0, fg_color="transparent", command=self.toggle_play_pause)
        self.play_pause_button.grid(row=0, column=1, padx=5)
        
        next_button = ctk.CTkButton(control_frame, image=next_icon, width=50, height=50, text="", border_width=0, fg_color="transparent", command=self.next_track)
        next_button.grid(row=0, column=2, padx=5)
        
        # 播放进度条
        self.progress_bar = ctk.CTkSlider(self, from_=0, to=100)
        self.progress_bar.pack(pady=20)
        
        # 重写关闭窗口事件
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.is_playing = False  # 播放状态标记

    def toggle_play_pause(self):
        if self.is_playing:
            self.play_pause_button.configure(image=ImageTk.PhotoImage(Image.open("play.png").resize((50, 50))))  # 替换为播放图标
            print("Music paused!")
            # 暂停音乐逻辑可在此处实现
        else:
            self.play_pause_button.configure(image=ImageTk.PhotoImage(Image.open("pause.png").resize((50, 50))))  # 替换为暂停图标
            print("Playing music!")
            # 播放音乐逻辑可在此处实现
        self.is_playing = not self.is_playing  # 切换播放状态

    def previous_track(self):
        print("Playing previous track!")
        # 上一首歌曲逻辑可在此处实现

    def next_track(self):
        print("Playing next track!")
        # 下一首歌曲逻辑可在此处实现

    def on_close(self):
        # 关闭音乐播放器窗口
        self.destroy()

if __name__ == "__main__":
    # 创建并启动应用程序窗口
    plant_app = PlantApp()
    plant_app.mainloop()
