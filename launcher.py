import json
import os
import pygame
from tkinter import Tk, Button, Label, filedialog, Entry, Listbox, Scrollbar, messagebox
import subprocess

def load_game_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def run_game(game_data):
    resolution = game_data.get('resolution', (1080, 720))
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption(game_data.get('title', 'The Running Zombie'))

    game_path = game_data.get('game_path', '')
    if game_path:
        try:
            subprocess.run(['python', game_path])
        except Exception as e:
            print(f"Błąd podczas uruchamiania gry: {e}")
    else:
        print("Brak ścieżki do pliku game_loop.py")

    pygame.quit()

def select_game_folder():
    default_folder = os.path.join("C:", "easyPyGame")  # Domyślny folder na dysku C
    folder_path = filedialog.askdirectory(title="Wybierz folder z grą", initialdir=default_folder)

    # Sprawdź i utwórz folder, jeśli nie istnieje
    target_folder = os.path.join(folder_path, "easyPyGame")
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    game_folder_entry.delete(0, 'end')
    game_folder_entry.insert(0, target_folder)

def install_required_libraries():
    try:
        subprocess.run(["pip", "install", "pygame"])
    except Exception as e:
        print(f"Błąd podczas instalacji bibliotek: {e}")

def start_game():
    game_folder = game_folder_entry.get()
    game_data_file = "game_data.pg"
    game_path = os.path.join(game_folder, game_data_file)

    if os.path.exists(game_path):
        data = load_game_data(game_path)
        run_game(data)
    else:
        result_label.config(text=f"Brak pliku danych gry: {game_data_file}")

def browse_games():
    game_folder = game_folder_entry.get()
    game_listbox.delete(0, 'end')  # Wyczyść listbox przed dodaniem nowych pozycji

    if os.path.exists(game_folder):
        games = [game for game in os.listdir(game_folder) if game.endswith(".pg")]
        for game in games:
            game_listbox.insert('end', game)
    else:
        messagebox.showinfo("Błąd", "Folder gier nie istnieje. Wybierz poprawny folder.")

def show_game_info():
    selected_game = game_listbox.get('active')
    if not selected_game:
        messagebox.showinfo("Informacja", "Wybierz grę, aby zobaczyć informacje.")
        return

    game_folder = game_folder_entry.get()
    game_path = os.path.join(game_folder, selected_game)

    if os.path.exists(game_path):
        data = load_game_data(game_path)
        info_str = f"Opis: {data.get('description', 'Brak opisu')}\nTwórca: {data.get('creator', 'Brak informacji')}\nData wydania: {data.get('release_date', 'Brak informacji')}"
        messagebox.showinfo("Informacje o grze", info_str)
    else:
        messagebox.showinfo("Błąd", "Nie można znaleźć informacji o grze. Sprawdź wybrany folder gier.")

def manage_library():
    # W tym miejscu można dodać funkcje zarządzania biblioteką gier
    pass

# Interfejs graficzny
root = Tk()
root.title("Pygame Launcher")

game_folder_label = Label(root, text="Folder z grą:")
game_folder_label.pack()

game_folder_entry = Entry(root, width=50)
game_folder_entry.pack()

select_folder_button = Button(root, text="Wybierz folder", command=select_game_folder)
select_folder_button.pack()

start_button = Button(root, text="Uruchom grę", command=start_game)
start_button.pack()

result_label = Label(root, text="")
result_label.pack()

install_required_libraries()

# Dodane funkcje:
game_listbox = Listbox(root, selectmode='single', width=50, height=10)
game_listbox.pack()

browse_button = Button(root, text="Przeglądaj gry", command=browse_games)
browse_button.pack()

info_button = Button(root, text="Informacje o grze", command=show_game_info)
info_button.pack()

manage_button = Button(root, text="Zarządzaj biblioteką", command=manage_library)
manage_button.pack()

root.mainloop()
