from PPlay import window
from PPlay import keyboard
from PPlay import sprite


width, height = 800, 600
screen = window.Window(width, height)
inputs = keyboard.Keyboard()
screen.set_title("FUZZY: Semáforo Inteligente")

# Definições de cores
backgroud_color = [135, 206, 235]  # cor de fundo da tela
time_text_color = (0, 77, 101)  # cor do texto de tempo
signal_closed_text_color = (179, 34, 34)  # cor do texto de duração do semáforo fechado
signal_open_text_color = (5, 128, 49)  # cor do texto de duração do semáforo aberto
vehicle_people_text_color = (24, 26, 25)  # cor do texto de veículos e pessoas

# Definindo objeto semáforo
sinal_aberto = sprite.Sprite('src/sprites/semaforo_aberto.png')
sinal_aberto.set_position(600, 200 - sinal_aberto.height)
sinal_fechado = sprite.Sprite('src/sprites/semaforo_fechado.png')
sinal_fechado.set_position(600, 200 - sinal_fechado.height)
