import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

img_original = None
img_preview = None
img_width, img_height = 0, 0
img_tk = None


def rgb_to_rgb565(r, g, b):
    # 将RGB值转换为RGB565格式
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
        print("Error:", e)
        return None


def open_image():
    global img_original, img_preview, img_width, img_height, img_tk

    file_path = filedialog.askopenfilename(filetypes=[("JPG/PNG Files", "*.jpg;*.png"), ("All Files", "*.*")])

    if file_path:
        img_original = Image.open(file_path)
        img_width, img_height = img_original.size

        new_width_preview = int(img_width * 0.3)
        new_height_preview = int(img_height * 0.3)
        img_preview = img_original.resize((new_width_preview, new_height_preview), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_preview)

        image_label.config(image=img_tk)
        export_button.config(state=tk.NORMAL)


def export_image():
    if img_original:
        export_path = filedialog.asksaveasfilename(defaultextension=".h", filetypes=[("Header Files", "*.h")])
        if export_path:
            name = name_var.get()
            rgb565_data, width, height = image_to_rgb565(img_original)
            if rgb565_data:
                try:
                    with open(export_path, 'w') as f:
                        f.write("#define IMAGE_DATA_H\n\n")
                        f.write(f"const uint16_t {name}[{width * height}] PROGMEM = {{\n")

                        for i, value in enumerate(rgb565_data):
                            f.write("0x{:04X}".format(value))
                            if i < len(rgb565_data) - 1:
                                f.write(", ")
                            if (i + 1) % width == 0:
                                f.write("\n")

                        f.write("};\n\n")

                    export_label_var.set("Image exported to " + export_path)
                except Exception as e:
                    export_label_var.set("Error: " + str(e))
            else:
                export_label_var.set("Error converting image to RGB565!")


# 创建GUI窗口
window = tk.Tk()
window.title("单张图片转565转换器")
window.geometry("800x600")

# 创建LabelFrame用于显示图像
image_frame = ttk.LabelFrame(window, text="预览图像")
image_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

image_label = tk.Label(image_frame)
image_label.pack()

# 创建LabelFrame用于用户输入
input_frame = ttk.LabelFrame(window, text="输入信息")
input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

name_label = tk.Label(input_frame, text="数组名称:")
name_label.pack()
name_var = tk.StringVar()
name_entry = tk.Entry(input_frame, textvariable=name_var)
name_entry.pack()

# 创建按钮
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

open_button = tk.Button(button_frame, text="打开单张图片", command=open_image)
open_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(button_frame, text="导出h文件", command=export_image, state=tk.DISABLED)
export_button.pack(side=tk.LEFT, padx=5)

# 创建用于显示导出状态的标签
export_label_var = tk.StringVar()
export_label = tk.Label(window, textvariable=export_label_var)
export_label.pack()

window.mainloop()
