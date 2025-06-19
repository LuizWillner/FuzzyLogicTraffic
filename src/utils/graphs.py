import matplotlib.pyplot as plt
from src.fuzzymodule.fuzzy import pessoa, veiculo, aberto
    
    
def generate_membership_graphs(output_save_path=None):
    # Visualização das funções de pertinência para 'pessoa'
    pessoa.view(sim=None, title='Gráfico de pertinência - Pessoas', xlabel='Quantidade de pessoas', ylabel='Pertinência')
    plt.title('Funções de pertinência - Pessoas')
    plt.xlabel('Quantidade de pessoas')
    plt.ylabel('Pertinência')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if output_save_path:
        plt.savefig(output_save_path+'pessoa_membership.png')
        plt.close()
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
        plt.savefig(output_save_path+'veiculo_membership.png')
        plt.close()
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
        plt.savefig(output_save_path+'aberto_membership.png')
        plt.close()
    else:
        # Exibe o gráfico
        plt.show()
