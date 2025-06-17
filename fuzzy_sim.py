# Modelagem de semaforos inteligentes usando lógica fuzzy
#### Para o nosso exemplo o tempo de semaforo varia de 0-100, em que 0 indica estar fechado e 100 aberto. 
import random
from skfuzzy import control as ctrl
from src.model.Road import Road
from src.fuzzymodule.fuzzy import aberto_ctrl
from src.utils.simparams import (
    width, height, screen, inputs, 
    backgroud_color, time_text_color, signal_closed_text_color, signal_open_text_color, vehicle_people_text_color,
    sinal_aberto, sinal_fechado
)


aberto_simulator = ctrl.ControlSystemSimulation(aberto_ctrl)

### Simulação
#### Passe entradas para o ControlSystem usando rótulos Antecedent com *** Pythonic API ***
# Defuzzificação 
aberto_simulator.input['pessoas'] = 35
aberto_simulator.input['veiculos'] = 35
aberto_simulator.compute()

print(aberto_simulator.output['tempo'])

# pessoa.view(sim = aberto_simulator)
# veiculo.view(sim = aberto_simulator)
# aberto.view(sim = aberto_simulator)
# input()

total_time = 0  # Tempo total da simulação
cycle_time = 0
phase_time = 0  # Tempo da fase do semáforo
n_roads = 3  # Numero de rodovias
road = Road(n_roads, width)  # Chamada da classe rodovias
signal = True  # Estado do sinal
n_people = 0  # Numero de pessoas querendo atravessar
end = False  # Controle do termino da simulação
fechou = False  # Controle do sinal
closed_time = 0  # Tempo que deverá ficar fechado
opened_time = 0  # Tempo que deverá ficar aberto

while(not(end)):
    screen.set_background_color(backgroud_color)
    delta = screen.delta_time()
    cycle_time += delta
    phase_time += delta
    total_time += delta
    
    if fechou:  # Calculo Fuzzy para o tempo do sinal
        aberto_simulator.input['pessoas'] = n_people  # Enviando o número de pessoas que desejam atravessar para realização do calculo
        n_people = random.randint(0,50)
        aberto_simulator.input['veiculos'] = road.car_frequency  # Enviando o fluxo de carros para realização do calculo
        aberto_simulator.compute()  # Realizando a fuzzyficação
        road.car_frequency = 0
        closed_time = 100 - float(aberto_simulator.output['tempo'])
        opened_time = float(aberto_simulator.output['tempo'])
        cycle_time = 0
        phase_time = 0
        fechou = False
        
    if signal and cycle_time > opened_time + closed_time:
        fechou = True
        signal = False
    elif not(signal) and cycle_time > closed_time:
        signal = True
        fechou = False
        phase_time = 0

    for i in range(n_roads):
        road.add_car(i)

    screen.draw_text(f"Tempo total: {total_time:.2f}s",10,10, 24, time_text_color)
    screen.draw_text(f"Tempo ciclo: {cycle_time:.2f}s",260,10, 24, time_text_color)
    screen.draw_text(f"Tempo fase: {phase_time:.2f}s",510,10, 24, time_text_color)
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
