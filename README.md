# FuzzyTraffic

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
Há dois tipos de simuladores:
- [no_fuzzy_sim.py](): Simulador sem aplicação de lógica nebulosa.
- [fuzzy_sim.py](): Simulador com módulo nebuloso aplicado.

### Input
Os parâmetros de entrada para os dois simuladores podem ser configurados através do arquivo [input/sim_parameters.json](). Os parâmetros são descritos a seguir:
n_roads": 3,
simulation_time_limit": 1800,
car_limit_road": 100,

traffic:
	"intensity": 1.0,
	"dynamic_intensity": false,
	"intensity_upper_limit": 10.0,
	"intensity_lower_limit": 1.0

pedestrian "upper_limit": 50 "dynamic_upper_limit": false


	no_fuzzy >> "opened_time": 50,
	no_fuzzy >> "closed_time": 50
