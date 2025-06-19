import matplotlib.pyplot as plt
from src.utils.graphs import generate_membership_graphs
from src.fuzzymodule.fuzzy import aberto
from src.utils.generalparams import OUTPUT_PATH


MEMBERSHIP_GRAPHS_PATH = OUTPUT_PATH + 'membership_graphs/'

if __name__ == "__main__":
    generate_membership_graphs(output_save_path=MEMBERSHIP_GRAPHS_PATH)
    # aberto.view(sim=None, title='Gráfico de pertinência - Semáforo Inteligente', xlabel='Abertura do semáforo', ylabel='Pertinência')
    # plt.show()