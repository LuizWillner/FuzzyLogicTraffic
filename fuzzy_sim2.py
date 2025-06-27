# Modelagem de semaforos inteligentes usando lógica fuzzy
#### Para o nosso exemplo o tempo de semaforo varia de 0-100, em que 0 indica estar fechado e 100 aberto. 
import random
import json
from skfuzzy import control as ctrl
from src.model.Road import Road
from src.utils.generalconfig import OUTPUT_PATH, SIMULATION_PARAMETERS_FILE_PATH
from src.utils.graphs import generate_simulation_graphs
from src.fuzzymodule.fuzzy import aberto_ctrl
from src.utils.simconfig import (
    width, screen, inputs, 
    backgroud_color, time_text_color, signal_closed_text_color, signal_open_text_color, vehicle_people_text_color,
    sinal_aberto, sinal_fechado
)


SIMULATION_GRAPH_PATH = OUTPUT_PATH + 'sim_graphs/'

with open(SIMULATION_PARAMETERS_FILE_PATH, 'r') as json_file:
    sim_params = json.load(json_file)

aberto_simulator = ctrl.ControlSystemSimulation(aberto_ctrl)

### Simulação
total_time = 0  # Tempo total da simulação
cycle_time = 0
phase_time = 0  # Tempo da fase do semáforo
n_roads = sim_params["n_roads"]  # Numero de rodovias
road = Road(n_roads, width)  # Chamada da classe rodovias
signal = True  # Estado do sinal

traffic_intensity: float = sim_params["traffic"]["intensity"] # Intensidade do tráfego
traffic_intensity_upper_limit: float = sim_params["traffic"]["intensity_upper_limit"] # Limitante superior da intensidade do tráfego
traffic_intensity_lower_limit: float = sim_params["traffic"]["intensity_lower_limit"]  # Limitante inferior da intensidade do tráfego
# 0.0001; 0.0005; 0.001
linear_step: float = sim_params["traffic"]["linear_step"] # Passo linear para a intensidade do tráfego

dynamic_traffic_intensity: bool = sim_params["traffic"]["dynamic_intensity"] # Se True, a intensidade do tráfego varia dinamicamente
linear_intensity : bool = sim_params["traffic"]["linear_intensity"]  # Se True, a intensidade do tráfego é dinâmica e varia linearmente. Se False, a intensidade do tráfego varia aleatoriamente]
if dynamic_traffic_intensity:
    if linear_intensity:
        # Intensidade do tráfego dinâmica linear
        traffic_intensity = traffic_intensity_lower_limit  
    else:
        # Intensidade do tráfego dinâmica aleatória
        traffic_intensity = random.uniform(traffic_intensity_lower_limit, traffic_intensity_upper_limit) 

# inteiro que varia de 0 a 50
people_upper_limit: int = sim_params["pedestrians"]["upper_limit"] # Limitante superior de pessoas geradas aleatoriamente
dynamic_people_upper_limit: bool = sim_params["pedestrians"]["dynamic_upper_limit"]  # Se True, o limitante superior de pessoas varia dinamicamente
if dynamic_people_upper_limit:
    people_upper_limit = random.randint(0, 50)  # Intensidade de pessoas dinâmica
    
car_limit = sim_params["car_limit_road"]  # Limite de carros gerados na road
n_people = 0  # Numero de pessoas querendo atravessar
end = False  # Controle do termino da simulação
fechou = False  # Controle do sinal
closed_time = 0  # Tempo que deverá ficar fechado
opened_time = 0  # Tempo que deverá ficar aberto
sim_time_series = {
    'time_x': [],
    'opened_time_y': [],
    'cars_y': [],
    'people_y': [],
    'traffic_intensity_y': [],
    'total_time': 0
}
time_limit = sim_params["simulation_time_limit"]  # Tempo limite da simulação em segundos
# 3600 segundos = 1 hora
# 2700 segundos = 45 minutos
# 1800 segundos = 30 minutos
# 900 segundos = 15 minutos
# 600 segundos = 10 minutos
# 300 segundos = 5 minutos

####### TODO: Remover gambiarra abaixo depois #######
lista_toda = []
lista_base = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
              40, 35, 30, 25, 20, 15, 10, 5]
for _ in range(20):
    lista_toda = lista_toda + lista_base
i_people = 0
######################################################

# GameLoop
while(not(end)):
    screen.set_background_color(backgroud_color)
    delta = screen.delta_time()
    cycle_time += delta
    phase_time += delta
    total_time += delta
    
    if fechou:  # Calculo Fuzzy para o tempo do sinal
        ###### TODO: GAMBIARRA PARA TESTE ######
        # n_people = random.randint(0, people_upper_limit)
        n_people = lista_toda[i_people]
        i_people += 1
        ########################################
        
        # Input de um novo número de pessoas e veículos ao sistema fuzzy
        aberto_simulator.input['pessoas'] = n_people  # Enviando o número de pessoas que desejam atravessar para realização do calculo
        sim_time_series['people_y'].append(n_people)   
        
        aberto_simulator.input['veiculos'] = road.car_frequency  # Enviando o fluxo de carros para realização do calculo
        sim_time_series['cars_y'].append(road.car_frequency)
        sim_time_series['time_x'].append(total_time)
        
        # compute() executa todo o ciclo fuzzy: fuzzificação das entradas, avaliação das regras, agregação e defuzzificação, 
        # retornando o valor final da saída do seu sistema através do método output().
        aberto_simulator.compute()  # Defuzzyficação é feita pela técnica de centroide por padrão
        road.car_frequency = 0
        closed_time = 100 - float(aberto_simulator.output['tempo'])
        opened_time = float(aberto_simulator.output['tempo'])
        sim_time_series['opened_time_y'].append(opened_time)
        
        sim_time_series['traffic_intensity_y'].append(traffic_intensity)
        
        if dynamic_traffic_intensity:
            if linear_intensity: 
                if (
                    traffic_intensity + linear_step > traffic_intensity_upper_limit or 
                    traffic_intensity + linear_step < traffic_intensity_lower_limit
                ):
                    linear_step = -1 * linear_step
                traffic_intensity += linear_step
            else:
                traffic_intensity = random.uniform(traffic_intensity_lower_limit, traffic_intensity_upper_limit)
            print(traffic_intensity)
            
        if dynamic_people_upper_limit:
            people_upper_limit = random.randint(0, 50)
            
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
        road.add_car(i, traffic_intensity/10_000, car_limit)

    screen.draw_text(f"Tempo total: {total_time:.2f}s",10,10, 24, time_text_color)
    screen.draw_text(f"Tempo ciclo: {cycle_time:.2f}s",260,10, 24, time_text_color)
    screen.draw_text(f"Tempo fase: {phase_time:.2f}s",510,10, 24, time_text_color)
    screen.draw_text(f"Duração do sinal aberto: {opened_time:.2f} |",10,34, 24, signal_open_text_color)
    screen.draw_text(f"Duração do sinal fechado: {closed_time:.2f} ",260,34, 24, signal_closed_text_color)
    screen.draw_text(f"Veículos na tela: {road.n_cars} | Vazão de veículos: {road.car_frequency} | Pessoas: {n_people} | Sinal: {signal} | Tráfego: {traffic_intensity:.1f}",10,58, 24, vehicle_people_text_color)
    
    if(inputs.key_pressed('esc')) or total_time > time_limit:
        end = True
        sim_time_series['total_time'] = total_time
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

if end:
    print("Simulação encerrada.")
    print(f"Tempo total de simulação: {sim_time_series['total_time']:.2f} segundos")
    print(f"Série temporal (tempo): {sim_time_series['time_x']}")
    print(f"Série temporal (tempo de semáforo aberto): {sim_time_series['opened_time_y']}")
    print(f"Série temporal (número de veículos): {sim_time_series['cars_y']}")
    print(f"Série temporal (número de pessoas): {sim_time_series['people_y']}")
    print(f"Série temporal (intensidade de tráfego): {sim_time_series['traffic_intensity_y']}")
    generate_simulation_graphs(sim_time_series, output_save_path=SIMULATION_GRAPH_PATH)
    