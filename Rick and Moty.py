import requests
import tkinter as tk
from PIL import Image, ImageTk
import io

def get_characters(url):
    r = requests.get(url)
    data = r.json()
    return data

def open_character_url(url):
    import webbrowser
    webbrowser.open(url)

def open_episode_url(url):
    import webbrowser
    webbrowser.open(url)

def show_character(index):
    global characters, img_label, name_label, species_label, url_btn, photo_img, episodes_frame
    character = characters[index]
    name_label.config(text=f"Имя: {character['name']}")
    species_label.config(text=f"Вид: {character['species']}")
    url_btn.config(command=lambda: open_character_url(character['url']))
    url_btn.config(text="Открыть страницу персонажа")
    # Загрузка фото
    response = requests.get(character['image'])
    img_data = response.content
    image = Image.open(io.BytesIO(img_data)).resize((200, 200))
    photo_img = ImageTk.PhotoImage(image)
    img_label.config(image=photo_img)
    img_label.image = photo_img
    # Получение названий эпизодов и создание кнопок
    for widget in episodes_frame.winfo_children():
        widget.destroy()
    episode_urls = character['episode']
    tk.Label(episodes_frame, text="Эпизоды:", font=("Arial", 10, "bold"), anchor="w").pack(fill=tk.X)
    for ep_url in episode_urls:
        try:
            ep_data = requests.get(ep_url).json()
            ep_text = f"{ep_data['episode']}: {ep_data['name']}"
            btn = tk.Button(episodes_frame, text=ep_text, font=("Arial", 9), anchor="w", justify=tk.LEFT,
                            command=lambda url=ep_url: open_episode_url(url))
            btn.pack(fill=tk.X, padx=5, pady=1)
        except Exception:
            tk.Label(episodes_frame, text="Ошибка загрузки эпизода", font=("Arial", 9), fg="red").pack(fill=tk.X)

def next_character():
    global current_index, characters, next_url
    if current_index < len(characters) - 1:
        current_index += 1
        show_character(current_index)
    elif next_url:
        # Загружаем следующую страницу персонажей
        data = get_characters(next_url)
        characters.extend(data['results'])
        next_url = data['info']['next']
        current_index += 1
        show_character(current_index)

def prev_character():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_character(current_index)

root = tk.Tk()
root.title("Rick and Morty Characters")

start_url = "https://rickandmortyapi.com/api/character"
data = get_characters(start_url)
characters = data['results']
next_url = data['info']['next']
current_index = 0

img_label = tk.Label(root)
img_label.pack()

name_label = tk.Label(root, font=("Arial", 14, "bold"))
name_label.pack()
species_label = tk.Label(root, font=("Arial", 12))
species_label.pack()
url_btn = tk.Button(root, font=("Arial", 10), fg="blue")
url_btn.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

prev_btn = tk.Button(btn_frame, text="<< Назад", command=prev_character)
prev_btn.pack(side=tk.LEFT, padx=10)
next_btn = tk.Button(btn_frame, text="Вперёд >>", command=next_character)
next_btn.pack(side=tk.LEFT, padx=10)

photo_img = None
episodes_frame = tk.Frame(root)
episodes_frame.pack(fill=tk.BOTH, padx=10, pady=10)
show_character(current_index)

root.mainloop()