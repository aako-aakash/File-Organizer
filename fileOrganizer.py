import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

#  Backend 
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Programs": [".exe", ".msi", ".apk"],
    "Python Files": [".py"],
    "Others": []
}

# 🚨 Blocked folders (critical system dirs)
BLOCKED_FOLDERS = [
    "C:\\", "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users"
]

def is_safe_path(path):
    """Check if path is safe to organise"""
    norm_path = os.path.normpath(path).lower()
    for blocked in BLOCKED_FOLDERS:
        if norm_path == os.path.normpath(blocked).lower():
            return False
    return True

def organise_files(folder_path):
    if not os.path.exists(folder_path):
        return "Folder does not exist!"

    if not is_safe_path(folder_path):
        return "⚠ This folder is protected. Please choose another folder."

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):  # Only handle files
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if any(filename.lower().endswith(ext) for ext in extensions):
                    category_path = os.path.join(folder_path, category)
                    os.makedirs(category_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_path, filename))
                    moved = True
                    break
            if not moved:  # If no category matched
                other_path = os.path.join(folder_path, "Others")
                os.makedirs(other_path, exist_ok=True)
                shutil.move(file_path, os.path.join(other_path, filename))

    return "✅ Files organised successfully!"

#  Frontend 
def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def start_organising():
    path = folder_path.get()
    if path:
        result = organise_files(path)
        if "⚠" in result:
            messagebox.showerror("Error", result)
        else:
            messagebox.showinfo("Result", result)
    else:
        messagebox.showwarning("Warning", "Please select a folder!")

# Theme Colors
LIGHT_THEME = {
    "bg": "#F5F5F5",
    "fg": "#000000",
    "button_bg": "#E0E0E0",
    "button_fg": "#000000",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#000000"
}

DARK_THEME = {
    "bg": "#2E2E2E",
    "fg": "#FFFFFF",
    "button_bg": "#444444",
    "button_fg": "#FFFFFF",
    "entry_bg": "#3E3E3E",
    "entry_fg": "#FFFFFF"
}

current_theme = DARK_THEME  
def apply_theme(theme):
    root.config(bg=theme["bg"])
    label.config(bg=theme["bg"], fg=theme["fg"])
    entry.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
    browse_btn.config(bg=theme["button_bg"], fg=theme["button_fg"])
    organise_btn.config(bg="green", fg="white")
    toggle_btn.config(bg=theme["button_bg"], fg=theme["button_fg"])

def toggle_theme():
    global current_theme
    if current_theme == DARK_THEME:
        current_theme = LIGHT_THEME
    else:
        current_theme = DARK_THEME
    apply_theme(current_theme)

# Tkinter Window
root = tk.Tk()
root.title("File Organiser - Light/Dark Mode (Safe)")
root.geometry("500x260")
root.resizable(False, False)

folder_path = tk.StringVar()

# GUI Widgets
label = tk.Label(root, text="Select a folder to organise:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, textvariable=folder_path, width=50)
entry.pack(pady=5)

browse_btn = tk.Button(root, text="Browse", command=browse_folder, relief="flat")
browse_btn.pack(pady=5)

organise_btn = tk.Button(root, text="Organise Files", command=start_organising, bg="green", fg="white", relief="flat")
organise_btn.pack(pady=10)

toggle_btn = tk.Button(root, text="Toggle Light/Dark Mode", command=toggle_theme, relief="flat")
toggle_btn.pack(pady=5)

apply_theme(current_theme)


root.mainloop()