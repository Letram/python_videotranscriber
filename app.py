import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, Label, Button, Entry, Frame
import cronista
import threading

bg_light = "#95afc0"
bg_dark = "#535c68"
text_color = "#130f40"

transc_thread = None

def select_video(label_string):
    reset_text_box()
    video_filename = filedialog.askopenfilename(
        initialdir = "./videos",
        title = "Select video",
        filetypes = (
            ("Video", "*.webm *.mp4 *.mkv *.avi *.wmv *.flv"),
            ("All files", "*.*")
        )
    )
    label_string.set(video_filename)

def reset_text_box():
    text_box.delete("1.0", tk.END)

def add_to_text_box(text: str):
    text_box.insert(tk.END, "\n" + text)

def transc(audio_path, language, num_seconds, on_transcription_progress):
    cronista.cronista_transcribe_GUI(audio_path, language, num_seconds, on_transcription_progress)

def transc_btn_click(audio_path, language, num_seconds):
    reset_text_box()
    global transc_thread
    transc_thread = threading.Thread(target = lambda: transc(audio_path.get(), language.get(), int(num_seconds.get()), add_to_text_box))
    transc_thread.daemon = True
    transc_thread.start()
    #cronista.cronista_transcribe_GUI(audio_path.get(), language.get(), int(num_seconds.get()), add_to_text_box)

# Creamos la raíz de la aplicación. En este caso la ventana base se llamará root.
root = tk.Tk(className = "Cronista V0_2")


# Creamos los frames en los que dividiremos la aplicación (son como los divs) y les decimos que su padre es la ventana principal (root)
video_frame = tk.Frame(master = root)

label_string = tk.StringVar()
video_button = tk.Button(
    video_frame,
    text = "Añadir vídeo",
    bg = bg_light,
    fg = text_color,
    command = lambda: select_video(label_string)
)
video_label = tk.Label(
    video_frame,
    textvariable = label_string,
    fg = text_color
)

video_button.pack(side = tk.LEFT)
video_label.pack(side = tk.LEFT,  padx = 10)

video_frame.pack(fill = tk.X, padx = 20, pady = 10)

lang_sec_frame = tk.Frame(master=root)

lang_subframe = Frame(
    lang_sec_frame
)
label_lang = Label(
    lang_subframe,
    text = "Lenguaje del vídeo ('es' o 'en')",
    fg = text_color
)
lang_entry = Entry(
    lang_subframe,
    fg = text_color
)
lang_entry.insert(0, "es")

label_lang.pack(side = tk.LEFT)
lang_entry.pack(side = tk.RIGHT)
lang_subframe.pack()

sec_subframe = Frame(
    lang_sec_frame
)
label_sec = Label(
    sec_subframe,
    text = "Duración de los bloques de audio en segundos",
    fg = text_color
)
sec_entry = Entry(
    sec_subframe,
    fg = text_color
)
sec_entry.insert(0, "20")

label_sec.pack(side = tk.LEFT)
sec_entry.pack(side = tk.RIGHT)
sec_subframe.pack()

lang_sec_frame.pack(fill = tk.X)

text_frame = tk.Frame(master=root)

text_box = Text(
    text_frame,
    fg = text_color,
    wrap = tk.WORD
)
text_box_scroll = Scrollbar(text_frame, orient = tk.VERTICAL, command = text_box.yview)
text_box_scroll.pack( padx = 10, pady = 10, side = tk.RIGHT, fill = tk.Y)

text_box["yscrollcommand"] = text_box_scroll.set

text_box.pack(padx = 10, pady = 10, side = tk.LEFT, fill = tk.X, expand = tk.YES)
text_frame.pack(fill = tk.X)

transcribe_button = Button(
    root,
    text = "Transcribir vídeo",
    bg = bg_light,
    fg = text_color,
    command = lambda: transc_btn_click(label_string, lang_entry, sec_entry)
)

transcribe_button.pack(pady = 10)

root.mainloop()
