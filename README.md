# Fuzzy Logic Traffic Lights - Um simulador de trânsito com semáforo nebuloso

Projeto da disciplina Lógica Nebulosa | Universidade Federal Fluminense | 2025.1

## Configurando ambiente de desenvolvimento
1. Baixar e instalar **Python 3.10**
	- No **Windows**, baixar e instalar pelo executável no [site](https://www.python.org/downloads/).
		
	- No **Ubuntu**, instalar pelo comando do terminal:
		```shell
		>> sudo apt-get install python3.10
		```

2. Criar ambiente virtual
	- No **Windows**:
		```shell
		>> py -m venv .venv
		```
		
	- No **Ubuntu**:
		```shell
		>> python3 -m venv .venv
		```

3. Ativar ambiente virtual. Sempre ativar quando ligar a máquina e iniciar o desenvolvimento.

	- No **Windows**:
		```shell
		>> .\.venv/Scripts/activate
		```

	- No **Ubuntu**:
		```shell
		>> source .venv/bin/activate
		```

4. Caso esteja no Windows, trocar politica de segurança do Windows, se necessário (executar comando abaixo no powershell como administrador):
	```shell
	>> Set-ExecutionPolicy AllSigned
	```

5. Instalar dependencies no venv.
	```shell
	>> pip install -r requirements.txt
	```

## Simulação
Para fazer uma simulação, basta executar um dos arquivos .py de simulação. Para parar a simulação, aperte a tecla ESC.
Há dois arquivos de simuladores:
- [*no_fuzzy_sim.py*](https://github.com/LuizWillner/FuzzyTraffic/blob/main/no_fuzzy_sim.py): Simulador sem aplicação de lógica nebulosa.
- [*fuzzy_sim.py*](https://github.com/LuizWillner/FuzzyTraffic/blob/main/fuzzy_sim.py): Simulador com módulo nebuloso aplicado.

### Input
Os parâmetros de entrada para os dois simuladores podem ser configurados através do arquivo [*input/sim_parameters.json*](https://github.com/LuizWillner/FuzzyTraffic/blob/main/input/sim_parameters.json). Os parâmetros são descritos a seguir:

- **n_roads**: quantidade de faixas de trânsito na simulação.
- **simulation_time_limit**: Tempo máximo em segundos da simulação.
- **car_limit_road:** Limite superior de carros por faixa.
- traffic:
	- **intensity**: Intensidade do tráfego de carros na simulação. Esse valor controla a probabilidade de um carro ser gerado a cada frame na simulação. Ele é dividido por 10000 no código para representar a probabilidade de fato. Empiricamente, constatas-e que o valor 1.0 representa uma intensidade baixa de tráfego, enquanto o valor 10.0 já representa uma intensidade moderada/alta.
	- **dynamic_intensity**: Valor booleano que controla se a intensidade do tráfego mudará dinamicamente na simulação.
	- **intensity_upper_limit**: A intensidade máxima que poderá ser assumida dinamicamente na simulação.
	- **intensity_lower_limit**: A intensidade mínima que poderá ser assumida dinamicamente na simulação.
- pedestrians:
	- **upper_limit**: O número máximo de pedestres que pode ser gerado na simulação.
	- **dynamic_upper_limit**: Valor booleano que controla se o limite máximo de pedestres na simulação mudará dinamicamente.
- no_fuzzy:
	- **opened_time**: Tempo que o sinal permanece aberto fixamente. Só afeta o simulador *no_fuzzy_sim.py*.
	- **closed_time**: Tempo que o sinal permanece fechado fixamente. Só afeta o simulador *no_fuzzy_sim.py*.

### Output
Para o simulador *fuzzy_sim.py*, os resultados da simulação podem ser encontrados em gráficos gerados em [*output/sim_graphs/*](https://github.com/LuizWillner/FuzzyTraffic/tree/main/output/sim_graphs). Cada subpasta agrupa os dados de uma simulação. Não há output para o simulador *no_fuzzy_sim.py*.

### Lógica Nebulosa
O módulo nebuloso, com a definição das funções de pertinência, regras base, etc., pode ser encontrado no script [*src/fuzzymodule/fuzzy.py*](https://github.com/LuizWillner/FuzzyTraffic/blob/main/src/fuzzymodule/fuzzy.py). A melhor forma de visualizar as configurações do módulo fuzzy, entretanto, é através dos gráficos gerados em [*output/membership_graphs/*](https://github.com/LuizWillner/FuzzyTraffic/tree/main/output/membership_graphs) e [*output/base_rules_heatmap/*](https://github.com/LuizWillner/FuzzyTraffic/tree/main/output/base_rules_heatmap). Caso alguma mudança seja feita nas regras de negócio do módulo fuzzy, basta rodar o script [*fuzzy_config_graphs.py*](https://github.com/LuizWillner/FuzzyTraffic/blob/main/fuzzy_config_graphs.py) que os gráficos serão gerados novamente de acordo com as mudanças feitas no *src/fuzzymodule/fuzzy.py*. Válido acrescentar que a defuzzificação é feita pelo método centroide, padrão da biblioteca Scikit-fuzzy.