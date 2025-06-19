from src.model.Road import Road
from src.utils.simparams import (
    width, height, screen, inputs, 
    backgroud_color, time_text_color, signal_closed_text_color, signal_open_text_color, vehicle_people_text_color,
    sinal_aberto, sinal_fechado
)


current_time = 0
n_roads = 3 #Numero de rodovias
road = Road(n_roads, width) #Chamada da classe rodovias
signal = True #Estado do sinal
n_people = 0 #Numero de pessoas querendo atravessar
end = False #Controle do termino da simulação
fechou = False #Controle do sinal
closed_time = 50 #Tempo que deverá ficar fechado
opened_time = 50 #Tempo que deverá ficar aberto

while(not(end)):
    screen.set_background_color(backgroud_color)
    current_time += screen.delta_time()
    
    if fechou:
        road.car_frequency = 0
        current_time = 0
        fechou = False

    if signal and current_time > opened_time:
        fechou = True
        signal = False
        current_time = 0
    elif not(signal) and current_time > closed_time:
        signal = True
        fechou = False
        current_time = 0

    for i in range(n_roads):
        road.add_car(i)

    screen.draw_text(f"Tempo atual: {current_time:.2f}s",10,10, 24, time_text_color)
    screen.draw_text(f"Duração do sinal aberto: {opened_time:.2f} |",10,34, 24, signal_open_text_color)
    screen.draw_text(f"Duração do sinal fechado: {closed_time:.2f} ",260,34, 24, signal_closed_text_color)
    screen.draw_text(f"Veículos na tela: {road.n_cars} | Vazão de veículos: {road.car_frequency} | Pessoas: {n_people} | Sinal: {signal}",10,58, 24, vehicle_people_text_color)
    
    if(inputs.key_pressed('esc')):
        signal = not(signal)
        
    road.update(screen.delta_time(), not(signal))
    road.draw()
    
    if(signal):
        sinal_aberto.draw()
    else:
        sinal_fechado.draw()
        
    screen.update()
