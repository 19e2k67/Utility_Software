import tkinter as tk


def chinese_to_unicode(text):
    unicode_str = ", ".join([f"0x{ord(char):x}" for char in text])
    return unicode_str


class ChineseToUnicodeConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.input_entry = None
        self.convert_button = None
        self.output_text = None
        self.credits_label = None
        self.converted_texts = None
        self.output_history_text = None
        self.title("中文转Unicode编码")
        self.geometry("800x800")

        self.create_widgets()

    def create_widgets(self):
        self.credits_label = tk.Label(self, text="输入要转换的文字")
        self.credits_label.pack(pady=10)

        self.input_entry = tk.Entry(self, width=100)
        self.input_entry.pack(pady=10)

        self.convert_button = tk.Button(self, text="中文转换Unicode", command=self.convert_and_display)
        self.convert_button.pack()

        self.credits_label = tk.Label(self, text="转换结果")
        self.credits_label.pack(pady=10)

        self.output_text = tk.Text(self, wrap=tk.WORD, width=100, height=10, state=tk.DISABLED)
        self.output_text.pack(pady=10)

        self.credits_label = tk.Label(self, text="转换记录（最多10笔）")
        self.credits_label.pack(pady=10)

        self.converted_texts = []
        self.output_history_text = tk.Text(self, wrap=tk.WORD, width=100, height=20, state=tk.DISABLED)
        self.output_history_text.pack(pady=5)

    def convert_and_display(self):
        input_text = self.input_entry.get()
        if input_text:
            unicode_text = chinese_to_unicode(input_text)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, unicode_text)
            self.output_text.config(state=tk.DISABLED)
            self.add_to_history(input_text, unicode_text)

    def add_to_history(self, input_text, unicode_text):
        self.converted_texts.append((input_text, unicode_text))
        if len(self.converted_texts) > 10:
            self.converted_texts.pop(0)

        history_text = "\n".join(
            [f"{input_text} -> {unicode_text}" for input_text, unicode_text in self.converted_texts])
        self.output_history_text.config(state=tk.NORMAL)
        self.output_history_text.delete(1.0, tk.END)
        self.output_history_text.insert(tk.END, history_text)
        self.output_history_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = ChineseToUnicodeConverter()
    app.mainloop()
