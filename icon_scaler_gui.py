#!/usr/bin/env python3
"""
Android Icon Generator GUI
GUI-Anwendung mit Drag-and-Drop für die Erstellung von Android App Icons
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from tkinter import Tk, Label, Button, Frame, filedialog, messagebox, BooleanVar, Checkbutton
from tkinter import ttk
from tkinter.ttk import Progressbar
import threading

from PIL import Image, ImageTk

# rembg wird nur bei Bedarf importiert
rembg_available = False
try:
    from rembg import remove as remove_background
    rembg_available = True
except ImportError:
    pass


ICON_SIZES = {
    'ldpi': 36,
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192
}


class IconScalerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Android Icon Scaler")
        self.root.geometry("500x470")
        self.root.resizable(False, False)

        self.current_icon_dir = None
        self.remove_bg_var = BooleanVar(value=False)

        self.setup_ui()
        self.setup_drag_drop()
        
    def setup_ui(self):
        self.root.configure(bg='#2b2b2b')
        
        title_label = Label(
            self.root,
            text="Android Icon Generator",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=20)
        
        self.drop_frame = Frame(
            self.root,
            bg='#3c3c3c',
            relief='solid',
            borderwidth=2,
            width=400,
            height=200,
            highlightbackground='#555555',
            highlightthickness=1
        )
        self.drop_frame.pack(pady=20)
        self.drop_frame.pack_propagate(False)
        
        self.drop_label = Label(
            self.drop_frame,
            text="Bild hier hineinziehen\noder klicken zum Auswählen",
            font=("Arial", 14),
            bg='#3c3c3c',
            fg='#ffffff'
        )
        self.drop_label.pack(expand=True)
        
        self.drop_frame.bind("<Button-1>", lambda e: self.select_file())
        self.drop_label.bind("<Button-1>", lambda e: self.select_file())

        # Checkbox für Hintergrundentfernung
        self.remove_bg_checkbox = Checkbutton(
            self.root,
            text="Hintergrund entfernen (transparent)",
            variable=self.remove_bg_var,
            font=("Arial", 11),
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#3c3c3c',
            activebackground='#2b2b2b',
            activeforeground='#ffffff'
        )
        self.remove_bg_checkbox.pack(pady=(10, 5))

        # Style für Progressbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar", 
                       background='#4CAF50',
                       troughcolor='#555555',
                       borderwidth=0,
                       lightcolor='#4CAF50',
                       darkcolor='#4CAF50')
        
        self.progress = Progressbar(
            self.root,
            length=400,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10)
        
        self.status_label = Label(
            self.root,
            text="Bereit für Bilddateien (JPG/PNG)",
            font=("Arial", 11),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        self.status_label.pack(pady=(10, 5))
        
        self.open_folder_btn = Button(
            self.root,
            text="📁 Ordner öffnen",
            font=("Arial", 11, "bold"),
            command=self.open_icon_folder,
            state='disabled',
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            disabledforeground='#666666',
            activebackground='#45a049',
            activeforeground='white'
        )
        self.open_folder_btn.pack(pady=(5, 20))
        
    def setup_drag_drop(self):
        try:
            from tkinterdnd2 import DND_FILES
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<DropEnter>>', self.drag_enter)
            self.drop_frame.dnd_bind('<<DropLeave>>', self.drag_leave)
            self.drop_frame.dnd_bind('<<Drop>>', self.drop)
        except (ImportError, AttributeError):
            pass
        
    def drag_enter(self, event):
        self.drop_frame.configure(bg='#1976d2')
        self.drop_label.configure(bg='#1976d2', fg='#ffffff')
        return 'copy'
        
    def drag_leave(self, event):
        self.drop_frame.configure(bg='#3c3c3c')
        self.drop_label.configure(bg='#3c3c3c', fg='#ffffff')
        
    def drop(self, event):
        self.drop_frame.configure(bg='#3c3c3c')
        self.drop_label.configure(bg='#3c3c3c', fg='#ffffff')
        
        files = event.data.split()
        if files:
            file_path = files[0].strip('{}')
            self.process_file(file_path)
        return 'copy'
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Bilddatei auswählen",
            filetypes=[
                ("Bilddateien", "*.jpg *.jpeg *.png"),
                ("JPG Dateien", "*.jpg *.jpeg"),
                ("PNG Dateien", "*.png")
            ]
        )
        if file_path:
            self.process_file(file_path)
            
    def process_file(self, file_path):
        threading.Thread(
            target=self.process_file_thread,
            args=(file_path,),
            daemon=True
        ).start()
        
    def process_file_thread(self, file_path):
        remove_bg = self.remove_bg_var.get()

        self.root.after(0, self.update_status, "Verarbeite Bild...")
        self.root.after(0, self.progress.configure, {'value': 0})

        if not os.path.exists(file_path):
            self.root.after(0, self.show_error, f"Datei nicht gefunden: {file_path}")
            return

        valid_extensions = ['.jpg', '.jpeg', '.png']
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in valid_extensions:
            self.root.after(0, self.show_error, "Nur JPG und PNG Dateien werden unterstützt!")
            return

        # Prüfe ob rembg verfügbar ist, wenn Hintergrundentfernung gewünscht
        if remove_bg and not rembg_available:
            self.root.after(0, self.show_error, "rembg ist nicht installiert!\nInstalliere es mit: pip install rembg")
            return

        input_path = Path(file_path)
        input_dir = input_path.parent

        icon_dir = input_dir / "icon"
        icon_dir.mkdir(exist_ok=True)
        self.current_icon_dir = str(icon_dir)

        try:
            with Image.open(file_path) as img:
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGBA')

                # Hintergrund entfernen falls gewünscht
                if remove_bg:
                    self.root.after(0, self.update_status, "Entferne Hintergrund...")
                    img = remove_background(img)
                    self.root.after(0, self.update_status, "Erstelle Icons...")

                total_sizes = len(ICON_SIZES)

                for idx, (density, size) in enumerate(ICON_SIZES.items()):
                    density_dir = icon_dir / "res" / f"mipmap-{density}"
                    density_dir.mkdir(parents=True, exist_ok=True)
                    
                    resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
                    
                    output_file = density_dir / "ic_launcher.png"
                    resized_img.save(output_file, "PNG", optimize=True)
                    
                    progress_value = ((idx + 1) / total_sizes) * 100
                    self.root.after(0, self.progress.configure, {'value': progress_value})
                    
            self.root.after(0, self.update_status, "✅ Icons erfolgreich erstellt!")
            self.root.after(0, self.enable_open_folder_button)
            
            preview_text = f"✅ Icons erfolgreich erstellt!\n📁 {self.current_icon_dir}"
            self.root.after(0, self.drop_label.configure, {'text': preview_text, 'fg': '#4CAF50'})
            
        except Exception as e:
            self.root.after(0, self.show_error, f"Fehler beim Verarbeiten: {str(e)}")
            
    def open_icon_folder(self):
        if not self.current_icon_dir:
            return
            
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', self.current_icon_dir])
        elif platform.system() == 'Windows':
            subprocess.run(['explorer', self.current_icon_dir])
        else:  # Linux
            subprocess.run(['xdg-open', self.current_icon_dir])
            
    def update_status(self, message):
        self.status_label.configure(text=message)
        
    def show_error(self, message):
        messagebox.showerror("Fehler", message)
        self.update_status("Bereit für Bilddateien (JPG/PNG)")
        self.progress.configure(value=0)
        
    def enable_open_folder_button(self):
        self.open_folder_btn.configure(state='normal', fg='#000000')


def main():
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = Tk()
    
    app = IconScalerGUI(root)
    
    try:
        from tkinterdnd2 import TkinterDnD
    except ImportError:
        messagebox.showwarning(
            "Hinweis",
            "Drag-and-Drop ist nicht verfügbar.\nInstalliere tkinterdnd2 mit: pip install tkinterdnd2\n\nDu kannst trotzdem Dateien per Klick auswählen."
        )
    
    root.mainloop()


if __name__ == "__main__":
    main()