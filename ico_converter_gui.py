import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import os

class IcoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICO 轉檔小工具")
        self.root.geometry("1000x750")

        self.file_list = []
        self.current_index = 0
        self.original_image = None
        self.display_image = None
        self.scale_factor = 1.0
        self.crop_rect = None
        self.canvas_rect_id = None
        self.output_dir = ""
        
        self.setup_ui()

    def setup_ui(self):
        # 左側控制欄
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(control_frame, text="1. 選擇圖片 (可多選)", command=self.load_images).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="2. 選擇輸出資料夾", command=self.select_output_dir).pack(fill=tk.X, pady=5)
        
        self.output_label = ttk.Label(control_frame, text="尚未選擇輸出資料夾", foreground="red", wraplength=150)
        self.output_label.pack(anchor=tk.W, pady=5)

        # 尺寸選擇
        ttk.Label(control_frame, text="3. 選擇包含的尺寸:").pack(anchor=tk.W, pady=(10, 0))
        self.sizes_vars = {}
        standard_sizes = [16, 32, 48, 64, 128, 256]
        for size in standard_sizes:
            var = tk.BooleanVar(value=True if size in [32, 64, 128] else False)
            ttk.Checkbutton(control_frame, text=f"{size}x{size}", variable=var).pack(anchor=tk.W)
            self.sizes_vars[size] = var

        # 自定義尺寸勾選框與輸入框
        custom_frame = ttk.Frame(control_frame)
        custom_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.custom_size_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="自定義:", variable=self.custom_size_var).pack(side=tk.LEFT)
        
        self.custom_size_entry = ttk.Entry(custom_frame, width=5)
        self.custom_size_entry.insert(0, "256")
        self.custom_size_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(custom_frame, text="px").pack(side=tk.LEFT)

        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # 批次選項
        self.auto_crop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="自動中心裁切 (跳過手動)", variable=self.auto_crop_var).pack(anchor=tk.W)

        self.info_label = ttk.Label(control_frame, text="待機中...", foreground="gray")
        self.info_label.pack(anchor=tk.W, pady=10)

        self.progress_label = ttk.Label(control_frame, text="")
        self.progress_label.pack(anchor=tk.W)

        ttk.Button(control_frame, text="執行轉換", command=self.start_conversion, style="Accent.TButton").pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # 右側畫布欄
        canvas_frame = ttk.Frame(self.root, padding="10")
        canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.instructions = ttk.Label(canvas_frame, text="請先載入圖片。載入後，請在圖片上拖曳滑鼠進行正方形裁切。")
        self.instructions.pack(anchor=tk.W)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#e0e0e0", cursor="cross")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        
        # 綁定視窗大小縮放事件，以利更新圖片顯示
        self.canvas.bind("<Configure>", lambda e: self.update_canvas())

    def load_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if not files:
            return
        self.file_list = list(files)
        self.current_index = 0
        self.load_current_file()

    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"輸出至: {os.path.basename(directory)}", foreground="green")

    def load_current_file(self):
        if 0 <= self.current_index < len(self.file_list):
            file_path = self.file_list[self.current_index]
            self.original_image = Image.open(file_path)
            self.update_canvas()
            self.info_label.config(text=f"目前檔案 ({self.current_index + 1}/{len(self.file_list)}): \n{os.path.basename(file_path)}", foreground="black")
            if self.canvas_rect_id:
                self.canvas.delete(self.canvas_rect_id)
            self.crop_rect = None
            
            if self.auto_crop_var.get():
                # 如果是自動裁切模式且還有下一個檔案，可能需要邏輯調整
                # 這裡暫時只負責載入，轉換時才決定裁切方式
                pass
        else:
            self.info_label.config(text="所有檔案已處理完畢或未載入檔案")

    def update_canvas(self):
        if not self.original_image:
            return

        self.root.update_idletasks() # 確保 winfo 數值準確
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 50: canvas_w = 600
        if canvas_h < 50: canvas_h = 500

        img_w, img_h = self.original_image.size
        self.scale_factor = min(canvas_w / img_w, canvas_h / img_h, 1.0)
        
        new_w = int(img_w * self.scale_factor)
        new_h = int(img_h * self.scale_factor)
        
        resized = self.original_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        # 如果之前有裁切框，重繪（簡單處理：縮放時清掉，讓使用者重拉，比較精確）
        self.crop_rect = None
        self.canvas_rect_id = None

    def on_button_press(self, event):
        if not self.original_image: return
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.canvas_rect_id:
            self.canvas.delete(self.canvas_rect_id)
        self.canvas_rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_move_press(self, event):
        if not self.original_image: return
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        
        dx = cur_x - self.start_x
        dy = cur_y - self.start_y
        side = max(abs(dx), abs(dy))
        
        end_x = self.start_x + (side if dx > 0 else -side)
        end_y = self.start_y + (side if dy > 0 else -side)
        
        self.canvas.coords(self.canvas_rect_id, self.start_x, self.start_y, end_x, end_y)
        self.crop_rect = [self.start_x, self.start_y, end_x, end_y]

    def start_conversion(self):
        if not self.file_list:
            messagebox.showwarning("警告", "請先選擇來源圖片！")
            return
        if not self.output_dir:
            messagebox.showwarning("警告", "請選擇輸出資料夾！")
            return

        # 取得尺寸
        target_sizes = [s for s, var in self.sizes_vars.items() if var.get()]
        
        if self.custom_size_var.get():
            custom_s = self.custom_size_entry.get().strip()
            if custom_s:
                try:
                    target_sizes.append(int(custom_s))
                except ValueError:
                    messagebox.showerror("錯誤", "自定義尺寸錯誤，請輸入整數數字")
                    return
        
        if not target_sizes:
            messagebox.showwarning("警告", "請選擇尺寸")
            return

        # 如果是單個檔案且有裁切，直接處理
        if len(self.file_list) == 1 or not self.auto_crop_var.get():
            self.process_one_file(target_sizes)
        else:
            # 批次自動模式
            count = 0
            for i, f_path in enumerate(self.file_list):
                try:
                    img = Image.open(f_path)
                    # 自動中心裁切
                    w, h = img.size
                    side = min(w, h)
                    left = (w - side) // 2
                    top = (h - side) // 2
                    cropped = img.crop((left, top, left + side, top + side))
                    
                    base_name = os.path.splitext(os.path.basename(f_path))[0]
                    save_name = os.path.join(self.output_dir, f"{base_name}.ico")
                    
                    icon_sizes = [(s, s) for s in target_sizes if s <= 256]
                    cropped.save(save_name, format='ICO', sizes=icon_sizes)
                    count += 1
                except Exception as e:
                    print(f"Error processing {f_path}: {e}")
            
            messagebox.showinfo("完成", f"已成功批次轉換 {count} 個檔案。")

    def process_one_file(self, target_sizes):
        # 針對目前顯示的檔案進行轉換
        if not self.original_image: return

        if not self.crop_rect:
            # 自動中心裁切
            w, h = self.original_image.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            working_img = self.original_image.crop((left, top, left + side, top + side))
        else:
            x1, y1, x2, y2 = self.crop_rect
            left, right = sorted([x1, x2])
            top, bottom = sorted([y1, y2])
            working_img = self.original_image.crop((
                left / self.scale_factor, 
                top / self.scale_factor, 
                right / self.scale_factor, 
                bottom / self.scale_factor
            ))

        base_name = os.path.splitext(os.path.basename(self.file_list[self.current_index]))[0]
        save_name = os.path.join(self.output_dir, f"{base_name}.ico")
        
        try:
            icon_sizes = [(s, s) for s in target_sizes if s <= 256]
            working_img.save(save_name, format='ICO', sizes=icon_sizes)
            
            # 處理下一個？
            if self.current_index < len(self.file_list) - 1:
                if messagebox.askyesno("成功", f"檔案已儲存。是否繼續裁切下一個檔案？"):
                    self.current_index += 1
                    self.load_current_file()
            else:
                messagebox.showinfo("成功", "所有檔案處理完畢！")
        except Exception as e:
            messagebox.showerror("失敗", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = IcoConverterApp(root)
    root.mainloop()
