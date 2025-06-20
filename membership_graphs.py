import matplotlib.pyplot as plt
from src.utils.graphs import generate_membership_graphs, generate_simulation_graphs, generate_rules_heatmap
from src.fuzzymodule.fuzzy import aberto
from src.utils.generalconfig import OUTPUT_PATH


MEMBERSHIP_GRAPHS_PATH = OUTPUT_PATH + 'membership_graphs/'
BASE_RULES_HEATMAP_PATH = OUTPUT_PATH + 'base_rules_heatmap/'

if __name__ == "__main__":
    generate_membership_graphs(output_save_path=MEMBERSHIP_GRAPHS_PATH)
    
    # sim_time_series = {
    #     'time_x': [0.153, 100.15799999999126, 200.16199999981217, 300.16799999959113, 400.170999999424, 500.17599999926483, 600.1809999996893, 700.1850000001388, 800.1890000004607, 900.1940000008116, 1000.2020000014077],
    #     'opened_time_y': [45.0, 45.0, 45.0, 82.95238095238095, 79.42857142857137, 82.95238095238095, 82.95238095238095, 45.0, 59.99999999999999, 82.639534883721, 82.95238095238095],
    #     'cars_y': [0, 47, 45, 47, 79, 77, 79, 80, 48, 59, 81],
    #     'people_y': [0, 45, 43, 10, 26, 22, 25, 47, 22, 3, 21],
    #     'total_time': 1020.06
    # }
    # generate_simulation_graphs(sim_time_series, output_save_path=OUTPUT_PATH+'sim_graphs/')
    
    generate_rules_heatmap(output_save_path=BASE_RULES_HEATMAP_PATH)