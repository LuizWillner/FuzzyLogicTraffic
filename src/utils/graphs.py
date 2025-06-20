import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
from src.fuzzymodule.fuzzy import pessoa, veiculo, aberto, fuzzy_decision_rules
from src.utils.generalparams import PessoaState, VeiculoState, SemaforoAbertoState


BLUE = '#3383BA'
GREEN = '#2CA02C'
ORANGE = '#FF7F0E'


def save_graph(dir_path: str, file_name: str):
    """
    Cria o diretório se não existir e salva o gráfico no caminho especificado.
    """
    os.makedirs(dir_path, exist_ok=True)
    plt.savefig(dir_path + file_name)
    plt.close()
    
    
def generate_membership_graphs(output_save_path: str | None = None):
    # Visualização das funções de pertinência para 'pessoa'
    pessoa.view(sim=None, title='Gráfico de pertinência - Pessoas', xlabel='Quantidade de pessoas', ylabel='Pertinência')
    plt.title('Funções de pertinência - Pessoas')
    plt.xlabel('Quantidade de pessoas')
    plt.ylabel('Pertinência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if output_save_path:
        save_graph(output_save_path, 'pessoa_membership.png')
    else:
        # Exibe o gráfico
        plt.show()
    
    # Visualização das funções de pertinência para 'veiculo'
    veiculo.view(sim=None, title='Gráfico de pertinência - Veículos', xlabel='Quantidade de veículos', ylabel='Pertinência')
    plt.title('Funções de pertinência - Veículos')
    plt.xlabel('Quantidade de veículos')
    plt.ylabel('Pertinência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if output_save_path:
        save_graph(output_save_path, 'veiculo_membership.png')
    else:
        # Exibe o gráfico
        plt.show()
    
    # Visualização das funções de pertinência para 'aberto'
    aberto.view(sim=None, title='Gráfico de pertinência - Semáforo Inteligente', xlabel='Abertura do semáforo', ylabel='Pertinência')
    plt.title('Funções de pertinência - Semáforo Aberto')
    plt.xlabel('Tempo de semáforo aberto')
    plt.ylabel('Pertinência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if output_save_path:
        save_graph(output_save_path, 'aberto_membership.png')
    else:
        # Exibe o gráfico
        plt.show()


def generate_simulation_graphs(sim_time_series: dict, output_save_path=None):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    total_time = sim_time_series['total_time']
    dir_path = output_save_path+f'sim_{date}_total_time_{total_time}/'
    
    # Gráfico de série temporal do tempo com as variáveis carros e pessoas
    plt.figure(figsize=(10, 6))
    plt.plot(sim_time_series['time_x'], sim_time_series['cars_y'], label='Carros', marker='s', color=BLUE)
    plt.plot(sim_time_series['time_x'], sim_time_series['people_y'], label='Pessoas', marker='^', color=GREEN)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Quantidade')
    plt.title(f'Simulação ({total_time:.1f}s) - Quant. Carros e Pessoas pelo Tempo')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    if output_save_path:
        save_graph(dir_path, 'sim_cars_people.png')
    else:
        # Exibe o gráfico
        plt.show()
        
    # Gráfico de série temporal do tempo com a variável tempo aberto
    plt.figure(figsize=(10, 6))
    plt.plot(sim_time_series['time_x'], sim_time_series['opened_time_y'], label='Tempo aberto', marker='o', color=ORANGE)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Tempo aberto (s)')
    plt.title(f'Simulação ({total_time:.1f}s) - Quant. Tempo do Semáforo Aberto pelo Tempo')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    if output_save_path:
        save_graph(dir_path, 'sim_opened_time.png')
    else:
        # Exibe o gráfico
        plt.show()
    
    # Gráfico de série temporal do tempo com todas as variáveis juntas (carros, pessoas e tempo aberto)
    plt.figure(figsize=(10, 6))
    plt.plot(sim_time_series['time_x'], sim_time_series['cars_y'], label='Carros', marker='s', color=BLUE)
    plt.plot(sim_time_series['time_x'], sim_time_series['people_y'], label='Pessoas', marker='^', color=GREEN)
    plt.plot(sim_time_series['time_x'], sim_time_series['opened_time_y'], label='Tempo aberto', marker='o', color=ORANGE)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Valores')
    plt.title(f'Simulação ({total_time:.1f}s) - Semáforo Aberto, Carros e Pessoas pelo Tempo')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    if output_save_path:
        save_graph(dir_path, 'sim_full_aggregate.png')
    else:
        # Exibe o gráfico
        plt.show()
        
        
def generate_rules_heatmap(output_save_path: str):
    veiculo_terms = VeiculoState.values()
    pessoa_terms = PessoaState.values()
    outputs = SemaforoAbertoState.values()
    
    # Monta a matriz de saída (como índices)
    matriz_idx = []
    for veic in veiculo_terms:
        linha = []
        for pess in pessoa_terms:
            saida = fuzzy_decision_rules(veic, pess)
            if saida in outputs:
                linha.append(outputs.index(saida))
            else:
                linha.append(np.nan)
        matriz_idx.append(linha)

    matriz_idx = np.array(matriz_idx)

    # Plotando o heatmap
    plt.figure(figsize=(8, 6))
    cmap = plt.get_cmap('coolwarm', len(outputs))
    im = plt.imshow(matriz_idx, cmap=cmap, vmin=0, vmax=len(outputs)-1)

    # Adiciona os rótulos nas células
    for i in range(len(veiculo_terms)):
        for j in range(len(pessoa_terms)):
            saida = fuzzy_decision_rules(veiculo_terms[i], pessoa_terms[j])
            plt.text(j, i, saida, ha='center', va='center', color='black', fontsize=9)

    plt.xticks(np.arange(len(pessoa_terms)), pessoa_terms, rotation=45)
    plt.yticks(np.arange(len(veiculo_terms)), veiculo_terms)
    cbar = plt.colorbar(im, ticks=range(len(outputs)))
    cbar.ax.set_yticklabels(outputs)
    plt.xlabel('Pessoa')
    plt.ylabel('Veículo')
    plt.title('Matriz de decisão fuzzy (Tempo de Semáforo Aberto)')
    plt.tight_layout()
    
    if output_save_path:
        save_graph(output_save_path, 'base_rules_heatmap.png')
    else:
        # Exibe o gráfico
        plt.show()
    