import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

def rgb_to_rgb565(r, g, b):
    r = (r >> 3) & 0x1F
    g = (g >> 2) & 0x3F
    b = (b >> 3) & 0x1F
    return (r << 11) | (g << 5) | b

def image_to_rgb565(image):
    try:
        img = image.convert("RGB")
        width, height = img.size
        rgb565_data = []

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                rgb565_value = rgb_to_rgb565(r, g, b)
                rgb565_data.append(rgb565_value)

        return rgb565_data, width, height

    except Exception as e:
        print("Error in image_to_rgb565:", e)
        return None

def open_images():
    global frames, img_list, img_preview_list, img_width_list, img_height_list, img_tk_list

    file_paths = filedialog.askopenfilenames(
        filetypes=[("JPG/PNG Files", "*.jpg"), ("JPG/PNG Files", "*.png"), ("ALL Files", "*")])

    if file_paths:
        frames = len(file_paths)
        img_list, img_preview_list, img_width_list, img_height_list, img_tk_list = [], [], [], [], []

        for file_path in file_paths:
            img = Image.open(file_path)
            img_width, img_height = img.size
            img_preview = img.resize((int(img_width * 0.3), int(img_height * 0.3)), Image.LANCZOS)

            img_list.append(img)
            img_preview_list.append(img_preview)
            img_width_list.append(img_width)
            img_height_list.append(img_height)

        show_images(img_preview_list, img_tk_list)

def show_images(img_preview_list, img_tk_list):
    # Clear previous image labels
    for widget in image_labels_frame.winfo_children():
        widget.destroy()

    # Create new image labels
    for i, img_preview in enumerate(img_preview_list):
        img_tk = ImageTk.PhotoImage(img_preview)
        img_tk_list.append(img_tk)
        img_label = tk.Label(image_labels_frame, image=img_tk)
        img_label.img_tk = img_tk  # 保持引用
        img_label.pack(side=tk.LEFT)

    # Update preview count label
    preview_count_label.config(text=f"预览图数量: {len(img_preview_list)}")
    export_button.config(state=tk.NORMAL)

def export_images():
    global frames, img_list, img_width_list, img_height_list

    if img_list:
        name = name_var.get()
        export_path = filedialog.asksaveasfilename(defaultextension=".h", filetypes=[("Header Files", "*.h")])

        if export_path:
            try:
                with open(export_path, 'w') as f:
                    f.write(f"#define {name}_FRAMES {frames}\n")
                    f.write(f"const uint16_t PROGMEM {name}[{frames}][{img_width_list[0] * img_height_list[0]}] = {{\n")

                    for i, img in enumerate(img_list):
                        rgb565_data, width, height = image_to_rgb565(img)
                        if rgb565_data:
                            f.write("{")
                            for j, value in enumerate(rgb565_data):
                                f.write("0x{:04X}".format(value))
                                if j < len(rgb565_data) - 1:
                                    f.write(", ")
                                if (j + 1) % width == 0:
                                    f.write("\n")
                            f.write("},\n")
                        else:
                            f.write("// Error converting image to RGB565!\n")

                    f.write("};\n\n")

                    export_label_var.set("Images exported to " + export_path)
            except Exception as e:
                export_label_var.set("Error: " + str(e))

# 创建GUI窗口
window = tk.Tk()
window.title("单张图片转565转换器")
window.geometry("800x600")

# 创建LabelFrame用于显示图像
image_frame = ttk.LabelFrame(window, text="预览图像", padding=(10, 10))
image_frame.pack(fill=tk.BOTH, expand=True)

image_labels_frame = tk.Frame(image_frame)
image_labels_frame.pack()

# 创建LabelFrame用于用户输入
input_frame = ttk.LabelFrame(window, text="输入信息", padding=(10, 10))
input_frame.pack(fill=tk.BOTH, expand=True)

name_label = tk.Label(input_frame, text="数组名称:")
name_label.pack()
name_var = tk.StringVar()
name_entry = tk.Entry(input_frame, textvariable=name_var)
name_entry.pack()

# 创建按钮
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

open_button = tk.Button(button_frame, text="打开多张图片", command=open_images)
open_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(button_frame, text="导出h文件", command=export_images, state=tk.DISABLED)
export_button.pack(side=tk.LEFT, padx=5)

# 创建用于显示导出状态的标签
export_label_var = tk.StringVar()
export_label = tk.Label(window, textvariable=export_label_var)
export_label.pack()

# Update global variables
frames = 0
img_list, img_preview_list, img_width_list, img_height_list, img_tk_list = [], [], [], [], []

# Create preview count label
preview_count_label = tk.Label(window, text="预览图数量: 0")
preview_count_label.pack()

window.mainloop()
