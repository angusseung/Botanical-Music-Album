import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import os

# 初始化 CustomTkinter
ctk.set_appearance_mode("light")  # 设置主题为浅色

class PlantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.selected_artist_button = None  # 记录选中的按钮

        self.title("Plant Importer")
        self.geometry("290x600")
        self.imported_image = None
        self.photo_ref = None

        # 第一部分：图片和导入按钮
        first_label = ctk.CTkLabel(self, text="First Step: Import a Plant Picture!", font=("Century Gothic", 15, "bold"), text_color="black")
        first_label.grid(row=0, column=0, pady=(10, 0), padx=20, sticky="w")

        self.image_label = ctk.CTkLabel(self, text="", width=250, height=150)
        self.image_label.grid(row=1, column=0, pady=(0, 0), padx=20)

        import_button = ctk.CTkButton(self, text="Import", font=("Century Gothic", 15, "bold"),command=self.import_image,fg_color="black", hover_color="#4e4e4e", width=180,height=30)
        import_button.grid(row=2, column=0, pady=10, padx=20)

        # 第二部分：画家按钮
        second_label = ctk.CTkLabel(self, text="Second Step: Choose a Pic Style!", font=("Century Gothic", 15, "bold"), text_color="black")
        second_label.grid(row=3, column=0, pady=(10, 0), padx=20, sticky="w")

        self.artist_list_frame = ctk.CTkFrame(self, width=250, height=100)
        self.artist_list_frame.grid(row=4, column=0, pady=10, padx=20)

        self.add_artist_info()

        # 第三部分：生成按钮
        third_label = ctk.CTkLabel(self, text="Third Step: Generate a Plant Music!", font=("Century Gothic", 15, "bold"), text_color="black")
        third_label.grid(row=5, column=0, pady=(20, 10), padx=20, sticky="w")

        generate_button = ctk.CTkButton(self, text="Generate", font=("Century Gothic", 15, "bold"),command=self.open_music_player, width=180,height=30,fg_color="black", hover_color="#4e4e4e")

        generate_button.grid(row=6, column=0, pady=(20, 10), padx=20)

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            image = Image.open(file_path)  # 这里保存的是 PIL 图像对象
            image = image.resize((230, 230), Image.LANCZOS)

            mask = Image.new('L', (230, 230), 0)
            draw = ImageDraw.Draw(mask)
            radius = 20
            draw.rounded_rectangle([0, 0, 230, 230], radius=radius, fill=255)
            image.putalpha(mask)
            
            # 保存 PIL 图像对象而不是 ImageTk.PhotoImage
            self.imported_image = image

            # 转换为 ImageTk.PhotoImage 并更新显示
            self.photo_ref = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.photo_ref, text="")  # 更新显
    

    def add_artist_info(self):
        artists = [("Keith Haring", "Keith Haring.jpg"),
                ("Pablo Picasso", "Pablo Picasso.jpg"),
                ("Wassily Kandinsky", "Wassily Kandinsky.jpg")]

        for artist_name, artist_image_filename in artists:
            artist_image_path = os.path.join("pic", artist_image_filename)
            try:
                artist_image = Image.open(artist_image_path).resize((100, 60), Image.LANCZOS)
                artist_image = ImageTk.PhotoImage(artist_image)
            except Exception as e:
                print(f"Error loading image {artist_image_filename}: {e}")
                continue

            # 创建按钮
            artist_button = ctk.CTkButton(
                self.artist_list_frame,
                text=artist_name,
                image=artist_image,
                compound="left",
                width=240,  # 使按钮宽度占满
                height=50,
                fg_color="transparent",  # 默认背景透明
                hover_color="white",  # 鼠标悬停时显示白色
                anchor="w",
                text_color="black",
                font=("Century Gothic", 15, "bold"),
                border_width=0, # 移除边框
                corner_radius=0
            )
            artist_button.grid(row=len(self.artist_list_frame.winfo_children()), column=0, pady=0, padx=0, sticky="ew")  # 填充整个框

            # 为按钮绑定点击事件
            artist_button.configure(command=lambda b=artist_button, name=artist_name: self.on_artist_selected(b, name))


    def on_mouse_enter(self, event, button):
        """鼠标进入时触发的事件，进行高亮显示"""
        button.configure(fg_color="white")  # 高亮显示背景为白色

    def on_mouse_leave(self, event, button):
        """鼠标离开时恢复原状"""
        if button != self.selected_artist_button:
            button.configure(fg_color="transparent")  # 恢复原始背景

    def on_artist_selected(self, artist_button, artist_name):
        """处理画家按钮的选中状态"""
        print(f"Artist selected: {artist_name}")

        # 如果有已选中的按钮，将其恢复为默认颜色
        if self.selected_artist_button:
            self.selected_artist_button.configure(fg_color="transparent")  # 恢复之前按钮的背景色

        # 更新当前按钮为选中状态，并设置颜色
        self.selected_artist_button = artist_button
        artist_button.configure(fg_color="white")  # 设置选中背景色
        
    def open_music_player(self):
        if self.imported_image:
            music_player = MusicPlayer(self, self.imported_image)
            music_player.grab_set()
        else:
            print("Please import an image first.")


class MusicPlayer(ctk.CTkToplevel):
    def __init__(self, parent, imported_image):
        super().__init__(parent)  # 创建Toplevel窗口

        self.title("Music Player")

        # 设置窗口大小
        self.geometry("325x530")

        # imported_image 是 PIL 图像对象
        pil_image = imported_image  # 使用传递过来的 PIL 图像对象

        # 调整图片大小
        pil_image = pil_image.resize((370, 370), Image.LANCZOS)

        # 转换为 ImageTk.PhotoImage 对象
        self.imported_image = ImageTk.PhotoImage(pil_image)
        # 设置歌曲时长
        self.song_duration = 4 * 60 + 36  # 4:36转为秒

        # 使用CustomTkinter的CTkFont类加载自定义字体，指定字号等属性
        custom_font = ctk.CTkFont(family="Century Gothic", size=25, weight="bold")
        custom_font_smaller = ctk.CTkFont(family="Century Gothic", size=20, weight="bold")

        # 在窗口顶部添加文字，调整与左侧和图片的距离，应用自定义字体
        album_label = ctk.CTkLabel(self, text="Botanical Music Album", font=custom_font, text_color="black")
        album_label.grid(row=0, column=0, pady=(30, 0), padx=20, sticky="w")  # 设置左侧边距和顶部间距

        # 在第一行文字下方添加第二行文字，减小与图片的间距，应用自定义字体
        now_playing_label = ctk.CTkLabel(self, text="Now Playing", font=custom_font_smaller, text_color="#8d8d8d")
        now_playing_label.grid(row=1, column=0, pady=(5, 0), padx=20, sticky="w")

        # 显示传递过来的植物图片
        image_label = ctk.CTkLabel(self, image=self.imported_image, width=260, height=260, text="")  # 清空text
        image_label.grid(row=2, column=0, pady=(15, 0))

        # 进度条上方的时间显示
        self.left_time_label = ctk.CTkLabel(self, text="0:00", font=("Century Gothic", 12), text_color="gray")
        self.left_time_label.grid(row=3, column=0, padx=20, sticky="w")

        self.right_time_label = ctk.CTkLabel(self, text=self.format_time(self.song_duration), font=("Century Gothic", 12), text_color="gray")
        self.right_time_label.grid(row=3, column=0, padx=20, sticky="e")

        # 播放进度条放到按钮区域的上一行，并加长进度条
        self.progress_bar = ctk.CTkSlider(self, from_=0, to=self.song_duration, width=250, command=self.update_time)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, pady=10)

        # 控制按钮区域
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=5, column=0, pady=10)

        icon_size = (50, 50)  # 控制按钮图标大小

        # 更新按钮的路径
        prev_icon_path = os.path.join("pic", "prev.png")
        prev_icon = Image.open(prev_icon_path).resize(icon_size)
        prev_icon = ImageTk.PhotoImage(prev_icon)

        play_icon_path = os.path.join("pic", "play.png")
        play_icon = Image.open(play_icon_path).resize(icon_size)
        play_icon = ImageTk.PhotoImage(play_icon)

        next_icon_path = os.path.join("pic", "next.png")
        next_icon = Image.open(next_icon_path).resize(icon_size)
        next_icon = ImageTk.PhotoImage(next_icon)

        prev_button = ctk.CTkButton(control_frame, image=prev_icon, width=50, height=50, text="", border_width=0, fg_color="transparent", hover_color="white",
                                   command=self.previous_track)
        prev_button.grid(row=0, column=0, padx=5)

        self.play_pause_button = ctk.CTkButton(control_frame, image=play_icon, width=50, height=50, text="", border_width=0,
                                               fg_color="transparent",  hover_color="white", command=self.toggle_play_pause)
        self.play_pause_button.grid(row=0, column=1, padx=5)

        next_button = ctk.CTkButton(control_frame, image=next_icon, width=50, height=50, text="", border_width=0, fg_color="transparent", hover_color="white",
                                   command=self.next_track)
        next_button.grid(row=0, column=2, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_playing = False

    def format_time(self, total_seconds):
        """格式化时间，将秒转换为mm:ss格式"""
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_time(self, current_position):
        """更新左侧时间显示"""
        current_position = int(current_position)  # 确保是整数
        formatted_time = self.format_time(current_position)
        self.left_time_label.configure(text=formatted_time)

    def toggle_play_pause(self):
        if self.is_playing:
            self.play_pause_button.configure(image=ImageTk.PhotoImage(Image.open(os.path.join("pic", "play.png")).resize((50, 50))))
            print("Music paused!")
        else:
            self.play_pause_button.configure(image=ImageTk.PhotoImage(Image.open(os.path.join("pic", "pause.png")).resize((50, 50))))
            print("Playing music!")
        self.is_playing = not self.is_playing

    def previous_track(self):
        print("Playing previous track!")

    def next_track(self):
        print("Playing next track!")

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    plant_app = PlantApp()
    plant_app.mainloop()
