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