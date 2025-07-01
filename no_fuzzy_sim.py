import json
import random
from src.model.Road import Road
from src.utils.generalconfig import SIMULATION_PARAMETERS_FILE_PATH
from src.utils.simconfig import (
    width, height, screen, inputs, 
    backgroud_color, time_text_color, signal_closed_text_color, signal_open_text_color, vehicle_people_text_color,
    sinal_aberto, sinal_fechado
)

with open(SIMULATION_PARAMETERS_FILE_PATH, 'r') as json_file:
    sim_params = json.load(json_file)

total_time = 0
current_time = 0
n_roads = sim_params["n_roads"] #Numero de rodovias
road = Road(n_roads, width) #Chamada da classe rodovias
signal = True #Estado do sinal

traffic_intensity: float = sim_params["traffic"]["intensity"] # Intensidade do tráfego
traffic_intensity_upper_limit: float = sim_params["traffic"]["intensity_upper_limit"] # Limitante superior da intensidade do tráfego
traffic_intensity_lower_limit: float = sim_params["traffic"]["intensity_lower_limit"]  # Limitante inferior da intensidade do tráfego
# 0.0001; 0.0005; 0.001
traffic_intensity = traffic_intensity/10000
traffic_intensity_upper_limit = traffic_intensity_upper_limit/10000
traffic_intensity_lower_limit = traffic_intensity_lower_limit/10000

dynamic_traffic_intensity: bool = sim_params["traffic"]["dynamic_intensity"] # Se True, a intensidade do tráfego varia dinamicamente
if dynamic_traffic_intensity and not traffic_intensity:
    # Intensidade do tráfego dinâmica
    traffic_intensity = random.uniform(traffic_intensity_lower_limit, traffic_intensity_upper_limit)  

# inteiro que varia de 0 a 50
people_upper_limit: int = sim_params["pedestrians"]["upper_limit"] # Limitante superior de pessoas geradas aleatoriamente
dynamic_people_upper_limit: bool = sim_params["pedestrians"]["dynamic_upper_limit"]  # Se True, o limitante superior de pessoas varia dinamicamente
if dynamic_people_upper_limit:
    people_upper_limit = random.randint(0, 50)  # Intensidade de pessoas dinâmica

car_limit = sim_params["car_limit_road"]  # Limite de carros gerados na road
n_people = 0 #Numero de pessoas querendo atravessar
end = False #Controle do termino da simulação
fechou = False #Controle do sinal
closed_time = sim_params["no_fuzzy"]["closed_time"] #Tempo que deverá ficar fechado
opened_time = sim_params["no_fuzzy"]["opened_time"] #Tempo que deverá ficar aberto
time_limit = sim_params["simulation_time_limit"]  # Tempo limite da simulação

while(not(end)):
    delta = screen.delta_time()
    screen.set_background_color(backgroud_color)
    current_time += delta
    total_time += delta
    
    if fechou:
        road.car_frequency = 0
        current_time = 0
        fechou = False
        n_people = random.randint(0, people_upper_limit)
        
        if dynamic_traffic_intensity:
            traffic_intensity = random.uniform(traffic_intensity_lower_limit, traffic_intensity_upper_limit)
                
        if dynamic_people_upper_limit:
            people_upper_limit = random.randint(0, 50)

    if signal and current_time > opened_time:
        fechou = True
        signal = False
        current_time = 0
    elif not(signal) and current_time > closed_time:
        signal = True
        fechou = False
        current_time = 0

    for i in range(n_roads):
        road.add_car(i, traffic_intensity, car_limit)

    screen.draw_text(f"Tempo atual: {current_time:.2f}s",10,10, 24, time_text_color)
    screen.draw_text(f"Duração do sinal aberto: {opened_time:.2f} |",10,34, 24, signal_open_text_color)
    screen.draw_text(f"Duração do sinal fechado: {closed_time:.2f} ",260,34, 24, signal_closed_text_color)
    screen.draw_text(f"Veículos na tela: {road.n_cars} | Vazão de veículos: {road.car_frequency} | Pessoas: {n_people} | Sinal: {signal} | Tráfego: {traffic_intensity*10000:.1f}",10,58, 24, vehicle_people_text_color)
    
    if(inputs.key_pressed('esc')) or total_time > time_limit:
        end = True
    if(inputs.key_pressed('a')):
        signal = True
        fechou = False
    if (inputs.key_pressed('f')):
        signal = False
        fechou = True
        
    road.update(screen.delta_time(), not(signal))
    road.draw()
    
    if(signal):
        sinal_aberto.draw()
    else:
        sinal_fechado.draw()
        
    screen.update()
