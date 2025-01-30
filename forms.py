import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from drv_command import DrvCommand
from serial_settings_dialog import SerialSettingsDialog
from transport import SerialSettings


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        # Инициализируем менеджер настроек
        self.settings_manager = SerialSettings('configs_com.ini')
        self.drv = None
        self.title("Устройство ЯК-001")
        self.geometry("450x450")  # Увеличил высоту для слайдера
        self.resizable(False, False)

        # состояние экрана начальное - потушен
        self.is_turquoise = False

        # Установка фиксированного серого фона окна
        self.configure(bg='#808080')

        # Создание главного меню
        self.menu_bar = tk.Menu(self)

        # Создание подменю "Настройки"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="COM port", command=self.open_settings)
        file_menu.add_command(label="Вид", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)

        # Создание подменю "Справка"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Добавление подменю в главное меню
        self.menu_bar.add_cascade(label="Настройки", menu=file_menu)
        self.menu_bar.add_cascade(label="Справка", menu=help_menu)

        # Установка меню в root
        self.config(menu=self.menu_bar)

        # Создание текстового поля без прокрутки
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            width=40,
            height=5,
            bg='#696969',
            fg='white'
        )
        self.text_area.pack(pady=20, padx=20)

        # Добавление примерного сообщения
        self.text_area.insert(tk.END, "ВЫКЛЮЧЕНО.\n")
        # self.text_area.configure(state='disabled')

        # Создание слайдера
        self.brightness_slider = ttk.Scale(
            self,
            from_=0,
            to=255,
            orient='horizontal',
            command=self.update_brightness,
            state="disabled"

        )
        self.frame_inputs = tk.Frame(self, bg="#808080")
        self.frame_inputs.pack(pady=5)

        self.entry_x = ttk.Entry(self.frame_inputs, state="disabled")
        self.entry_y = ttk.Entry(self.frame_inputs, state="disabled")
        self.entry_z = ttk.Entry(self.frame_inputs, state="disabled")

        self.btn_send_x = tk.Button(self.frame_inputs, text="Отправить",
                                    command=lambda: self.send_value(self.entry_x, "x"),
                                    state="disabled")
        self.btn_send_y = tk.Button(self.frame_inputs, text="Отправить",
                                    command=lambda: self.send_value(self.entry_y, "y"),
                                    state="disabled")
        self.btn_send_z = tk.Button(self.frame_inputs, text="Отправить",
                                    command=lambda: self.send_value(self.entry_z, "z"),
                                    state="disabled")

        labels = ["X", "Y", "Z"]
        entries = [self.entry_x, self.entry_y, self.entry_z]
        buttons = [self.btn_send_x, self.btn_send_y, self.btn_send_z]

        for i in range(3):
            tk.Label(self.frame_inputs, text=labels[i], bg="#808080", fg="white").grid(row=i, column=0, padx=5, pady=2)
            entries[i].grid(row=i, column=1, padx=5, pady=2)
            buttons[i].grid(row=i, column=2, padx=5, pady=2)


        tk.Label(self, text="Яркость", bg="#808080", fg="white").pack(pady=0)

        self.brightness_slider.set(50)  # Установка начального значения
        self.brightness_slider.pack(pady=10, padx=20, fill='x')

        self.button_frame = tk.Frame(self, bg="#808080")
        self.button_frame.pack(pady=10)  # Используем pack() для размещения фрейма

        # Создание кнопки test
        self.btn_test = tk.Button(
            self.button_frame,
            text="Тест соединения ...  ",
            command=self.test_connect,
            bg='#A9A9A9',
            fg='white',
            pady=7,
            padx=5,
            state="disabled"
        )

        # Создание кнопки reset
        self.btn_reset = tk.Button(
            self.button_frame,
            text="Сброс устройства",
            command=self.reset,
            bg='red',
            fg='white',
            pady=7,
            padx=20,
            state="disabled"
        )

        # Создание кнопки
        self.change_color_button = tk.Button(
            self.button_frame,
            text="Включить/Выключить ",
            command=self.on_off_device,
            bg='#A9A9A9',
            fg='black',
            pady=7,
            padx=20
        )

        self.btn_test.grid(row=0, column=0, padx=5, pady=5)
        self.btn_reset.grid(row=0, column=1, padx=5, pady=5)
        self.change_color_button.grid(row=1, column=0, columnspan=2, padx=5, pady=20)

    @staticmethod
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def send_value(self, entry, name: str):
        try:
            value = int(entry.get())
            setattr(self.drv, name, value)
            self.text_area.insert(tk.END, f"Отправлено в {name}: {value}\n")
        except ValueError:
            self.text_area.insert(tk.END, "Ошибка: Введите целое число!\n")
        self.text_area.yview(tk.END)

    def update_brightness(self, value):
        if self.is_turquoise:
            # Преобразуем значение слайдера (0-255) в компоненты цвета
            brightness = int(float(value))
            self.drv.br = brightness
            # Регулируем яркость бирюзового цвета
            r = int(64 * (brightness / 255))  # Базовый компонент R для бирюзового: 64
            g = int(224 * (brightness / 255))  # Базовый компонент G для бирюзового: 224
            b = int(208 * (brightness / 255))  # Базовый компонент B для бирюзового: 208

            new_color = self.rgb_to_hex(r, g, b)
            self.text_area.configure(bg=new_color)

    def on_off_device(self):
        list_el = (self.btn_reset, self.btn_test, self.entry_x, self.entry_y, self.entry_z, self.btn_send_x, self.btn_send_y, self.btn_send_z,
                   self.brightness_slider)
        if not self.is_turquoise:
            _conn = self.settings_manager.get_serial_connection()
            if _conn:
                self.drv = DrvCommand(_conn)
                if self.drv.is_connection():
                    # Изменение на бирюзовый и применение текущей яркости
                    self.is_turquoise = True
                    self.update_brightness(self.brightness_slider.get())
                    for widget in list_el:
                        widget.config(state="normal")
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, "Включено:\n")
                else:
                    self.text_area.insert(tk.END, "Устройство не готово...\n")
            else:
                self.text_area.insert(tk.END, "COM порт не готов\n")
        else:
            # Возврат к серому
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "ВЫКЛЮЧЕНО.\n")
            self.text_area.configure(bg='#696969')
            self.is_turquoise = False
            for widget in list_el:
                widget.config(state="disabled")
            self.drv.close()

    def test_connect(self):
        if self.drv.is_connection():
            self.text_area.insert(tk.END,"Устройство готово к работе!\n")
        else:
            self.text_area.insert(tk.END,"Устройство не 'отвечает'!\n")


    def reset(self):
        if messagebox.askyesno("Сброс устройства!","Вы уверенны?"):
            self.drv.reset()
            self.text_area.insert(tk.END,"Устройство сброшено к заводским настройкам!\n")

    def show_about(self):
        pass

    def open_settings(self):
        """Открытие диалога настроек"""
        SerialSettingsDialog(
            self,
            self.settings_manager,
            on_save=self.on_settings_saved
        )

    def on_settings_saved(self):
        """Callback при сохранении настроек"""
        self.text_area.insert(tk.END,"Настройки сохранены\n")
        print("Настройки сохранены")






