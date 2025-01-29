import tkinter as tk
from tkinter import ttk

def enable_controls():
    text_area.config(bg='turquoise')
    for widget in (entry_x, entry_y, entry_z, btn_send_x, btn_send_y, btn_send_z, slider):
        widget.config(state="normal")

def update_brightness(value):
    brightness = int(float(value))
    if text_area.cget("bg") == "turquoise":
        text_area.config(fg=f"#{brightness:02x}{brightness:02x}{brightness:02x}")

def send_value(entry):
    try:
        value = int(entry.get())
        text_area.insert(tk.END, f"Отправлено: {value}\n")
    except ValueError:
        text_area.insert(tk.END, "Ошибка: Введите целое число!\n")

root = tk.Tk()
root.title("Форма управления")
root.geometry("400x400")
root.configure(bg="gray20")

text_area = tk.Text(root, height=5, width=40, bg="gray30", fg="white", state="normal")
text_area.pack(pady=5)

btn_enable = tk.Button(root, text="Включить", command=enable_controls)
btn_enable.pack(pady=5)

frame_inputs = tk.Frame(root, bg="gray20")
frame_inputs.pack(pady=5)

entry_x = ttk.Entry(frame_inputs, state="disabled")
entry_y = ttk.Entry(frame_inputs, state="disabled")
entry_z = ttk.Entry(frame_inputs, state="disabled")

btn_send_x = tk.Button(frame_inputs, text="Отправить", command=lambda: send_value(entry_x), state="disabled")
btn_send_y = tk.Button(frame_inputs, text="Отправить", command=lambda: send_value(entry_y), state="disabled")
btn_send_z = tk.Button(frame_inputs, text="Отправить", command=lambda: send_value(entry_z), state="disabled")

labels = ["X", "Y", "Z"]
entries = [entry_x, entry_y, entry_z]
buttons = [btn_send_x, btn_send_y, btn_send_z]

for i in range(3):
    tk.Label(frame_inputs, text=labels[i], bg="gray20", fg="white").grid(row=i, column=0, padx=5, pady=2)
    entries[i].grid(row=i, column=1, padx=5, pady=2)
    buttons[i].grid(row=i, column=2, padx=5, pady=2)

slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", command=update_brightness, state="disabled")
slider.pack(pady=10)

root.mainloop()
