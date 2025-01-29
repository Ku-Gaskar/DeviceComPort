import tkinter as tk
from tkinter import ttk, scrolledtext


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Устройство ЯК-001")
        self.root.geometry("400x450")  # Увеличил высоту для слайдера
        self.root.resizable(False, False)

        # состояние экрана начальное - потушен
        self.is_turquoise = False

        # Установка фиксированного серого фона окна
        self.root.configure(bg='#808080')

        # Создание текстового поля без прокрутки
        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=40,
            height=5,
            bg='#696969',
            fg='white'
        )
        self.text_area.pack(pady=20, padx=20)

        # Добавление примерного сообщения
        self.text_area.insert(tk.END, "ВЫКЛЮЧЕНО.\n")
        self.text_area.configure(state='disabled')

        # Создание слайдера
        self.brightness_slider = ttk.Scale(
            root,
            from_=0,
            to=255,
            orient='horizontal',
            command=self.update_brightness
        )
        self.frame_inputs = tk.Frame(root, bg="gray20")
        self.frame_inputs.pack(pady=5)

        self.entry_x = ttk.Entry(self.frame_inputs, state="disabled")
        self.entry_y = ttk.Entry(self.frame_inputs, state="disabled")
        self.entry_z = ttk.Entry(self.frame_inputs, state="disabled")

        self.btn_send_x = tk.Button(self.frame_inputs, text="Отправить", command=lambda: self.send_value(self.entry_x),
                                    state="disabled")
        self.btn_send_y = tk.Button(self.frame_inputs, text="Отправить", command=lambda: self.send_value(self.entry_y),
                                    state="disabled")
        self.btn_send_z = tk.Button(self.frame_inputs, text="Отправить", command=lambda: self.send_value(self.entry_z),
                                    state="disabled")

        labels = ["X", "Y", "Z"]
        entries = [self.entry_x, self.entry_y, self.entry_z]
        buttons = [self.btn_send_x, self.btn_send_y, self.btn_send_z]

        for i in range(3):
            tk.Label(self.frame_inputs, text=labels[i], bg="gray20", fg="white").grid(row=i, column=0, padx=5, pady=2)
            entries[i].grid(row=i, column=1, padx=5, pady=2)
            buttons[i].grid(row=i, column=2, padx=5, pady=2)

        self.brightness_slider.set(50)  # Установка начального значения
        self.brightness_slider.pack(pady=10, padx=20, fill='x')

        # Создание кнопки test
        self.form = tk.Button(
            root,
            text="Тест соединения ...  ",
            command=self.test_connect,
            bg='#A9A9A9',
            fg='white',
            pady=10,
            padx=20
        )

        # Создание кнопки
        self.change_color_button = tk.Button(
            root,
            text="Включить/Выключить ",
            command=self.on_off_device,
            bg='#A9A9A9',
            fg='white',
            pady=10,
            padx=20
        )
        self.form.pack(pady=20)
        self.change_color_button.pack(pady=20)

    @staticmethod
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def send_value(self, entry):
        try:
            value = int(entry.get())
            self.text_area.insert(tk.END, f"Отправлено: {value}\n")
        except ValueError:
            self.text_area.insert(tk.END, "Ошибка: Введите целое число!\n")
        self.text_area.yview(tk.END)

    def update_brightness(self, value):
        if self.is_turquoise:
            # Преобразуем значение слайдера (0-255) в компоненты цвета
            brightness = int(float(value))
            # Регулируем яркость бирюзового цвета
            r = int(64 * (brightness / 255))  # Базовый компонент R для бирюзового: 64
            g = int(224 * (brightness / 255))  # Базовый компонент G для бирюзового: 224
            b = int(208 * (brightness / 255))  # Базовый компонент B для бирюзового: 208

            new_color = self.rgb_to_hex(r, g, b)
            self.text_area.configure(bg=new_color)

    def on_off_device(self):
        list_el = (self.entry_x, self.entry_y, self.entry_z, self.btn_send_x, self.btn_send_y, self.btn_send_z,
                       self.brightness_slider, self.text_area)
        if not self.is_turquoise:
            # Изменение на бирюзовый и применение текущей яркости
            self.is_turquoise = True
            self.update_brightness(self.brightness_slider.get())
            for widget in list_el:
                widget.config(state="normal")
            self.text_area.delete("1.0",tk.END)
            self.text_area.insert(tk.END,"Включено:\n")
        else:
            # Возврат к серому
            self.text_area.delete("1.0",tk.END)
            self.text_area.insert(tk.END,"ВЫКЛЮЧЕНО.")
            self.text_area.configure(bg='#696969')
            self.is_turquoise = False
            for widget in list_el:
                widget.config(state="disabled")

    def test_connect(self):
        pass


if __name__ == "__main__":
    base_root = tk.Tk()
    app = MainApplication(base_root)
    base_root.mainloop()
