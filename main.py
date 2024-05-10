import requests
import pygame
import threading
from io import BytesIO
from PIL import Image
import urllib3
import pygetwindow
# Отключение предупреждений об небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Функция для загрузки и воспроизведения музыки
def play_music(music_url):
    song_file = "song.mp3"

    # Скачиваем песню
    response = requests.get(music_url, verify=False)  # Добавляем verify=False для отключения проверки сертификатов
    with open(song_file, "wb") as f:
        f.write(response.content)

    # Воспроизводим песню
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play(-1)  # -1 означает воспроизведение в цикле

# Функция для отображения изображения на весь экран
def show_image(image_url):
    # Инициализируем pygame
    pygame.init()

    # Устанавливаем экран на полноэкранный режим
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Загружаем изображение
    response = requests.get(image_url, verify=False)  # Добавляем verify=False для отключения проверки сертификатов
    image = Image.open(BytesIO(response.content))

    # Преобразуем изображение в формат RGB и масштабируем под размер экрана
    image = image.convert("RGB").resize((screen_width, screen_height))

    # Отображаем изображение на экране
    pygame_image = pygame.image.fromstring(image.tobytes(), image.size, "RGB")
    screen.blit(pygame_image, (0, 0))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 6:  # 6 означает сворачивание окна
                    pygame.display.iconify()  # Минимизируем окно

    pygame.quit()

# URL для музыки и изображения
music_url = "https://muz8.z3.fm/d/18/gimn_ukraini_-_shche_ne_vmerla_ukrani_(zf.fm).mp3?download=force"
image_url = "https://img.freepik.com/free-vector/ukrainian-flag-pattern-vector_53876-162417.jpg"

# Запускаем процессы параллельно
music_thread = threading.Thread(target=play_music, args=(music_url,))
image_thread = threading.Thread(target=show_image, args=(image_url,))

music_thread.start()
image_thread.start()
while True:
    try:
        while True:
            window = pygetwindow.getWindowsWithTitle("pygame window")[0]
            print(window)
            if window.isMinimized == True:
                window.maximize()
    except:
        ...

