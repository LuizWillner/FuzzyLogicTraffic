import random
import matplotlib as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


# Variáveis ​​Linguisticas. Termos Linguisticos 
### Se Antecedente Então Consequente 
### Novos objetos Antecedent / Consequent possuem variáveis ​​de universo e número de associação
pessoa = ctrl.Antecedent(np.arange(0,60,1), 'pessoas')
veiculo = ctrl.Antecedent(np.arange(0,100,1), 'veiculos')

aberto = ctrl.Consequent(np.arange(0,100,1), 'tempo')
# Fuzzificação 
pessoa['muito baixo'] = fuzz.trapmf(pessoa.universe, [0,  0,  5, 10])
pessoa['baixo'] = fuzz.trapmf(pessoa.universe, [5, 10, 15, 20])
pessoa['medio'] = fuzz.trapmf(pessoa.universe, [15, 20, 25, 30])
pessoa['alto'] = fuzz.trapmf(pessoa.universe, [25, 30, 35, 40])
pessoa['muito alto'] = fuzz.trapmf(pessoa.universe, [35, 40, 60, 60])

veiculo['muito baixo'] = fuzz.trapmf(veiculo.universe, [0,0, 5,10])
veiculo['baixo'] = fuzz.trapmf(veiculo.universe, [5, 10, 15, 25])
veiculo['medio'] = fuzz.trapmf(veiculo.universe, [15,25, 30,40])
veiculo['alto'] = fuzz.trapmf(veiculo.universe, [30,40, 50,60])
veiculo['muito alto'] = fuzz.trapmf(veiculo.universe, [50,60,100,100])

### Uma função de pertinência personalizada pode ser construída de forma interativa com uma API Pythonic
aberto['Mais Fechado']= fuzz.trapmf(aberto.universe, [0,0,15, 30])
aberto['Fechado']= fuzz.trimf(aberto.universe, [15,30,45])
aberto['Equilibrado']= fuzz.trimf(aberto.universe, [30,45,60])
aberto['Aberto']= fuzz.trimf(aberto.universe, [45,60,75])
aberto['Mais Aberto'] = fuzz.trapmf(aberto.universe, [60,75,100,100])

# Maquina de Inferência 
ruleMA  = ctrl.Rule(
        (pessoa['muito baixo'] & (veiculo['medio'] | veiculo['alto'] | veiculo['muito alto'])) | 
        (pessoa['baixo'] & (veiculo['alto'] | veiculo['muito alto'])) | 
        (pessoa['medio'] & veiculo['muito alto']), 
    aberto['Mais Aberto']
)
ruleA = ctrl.Rule(
        (pessoa['muito baixo'] & veiculo['baixo']) | 
        (pessoa['baixo'] & veiculo['medio']) | 
        (pessoa['medio'] & veiculo['alto']) | 
        (pessoa['alto'] & veiculo['muito alto']), 
    aberto['Aberto']
)
ruleE  = ctrl.Rule (
        (veiculo ['muito baixo'] & pessoa ['muito baixo']) | 
        (veiculo ['muito baixo'] & pessoa ['baixo']) | 
        (veiculo ['baixo'] & pessoa ['baixo']) | 
        (veiculo ['baixo'] & pessoa ['medio']) | 
        (veiculo ['medio'] & pessoa ['medio']) | 
        (veiculo ['medio'] & pessoa ['alto']) | 
        (veiculo ['alto'] & pessoa ['alto']) | 
        (veiculo ['alto'] & pessoa ['muito alto']) | 
        (veiculo ['muito alto'] & pessoa ['muito alto']), 
    aberto['Equilibrado']
)
ruleF = ctrl.Rule(
        (pessoa['medio'] & veiculo['muito baixo']) |
        (pessoa['alto'] & veiculo['baixo']) |
        (pessoa['muito alto'] & veiculo['medio']), 
    aberto['Fechado']
)
ruleMF  = ctrl.Rule(
        ((pessoa['alto'] | pessoa['muito alto'])& veiculo['muito baixo']) | 
        (pessoa['muito alto'] & veiculo['baixo']), 
    aberto['Mais Fechado']
)
aberto_ctrl = ctrl.ControlSystem([ruleMA, ruleA, ruleE, ruleF, ruleMF])
aberto_simulator = ctrl.ControlSystemSimulation(aberto_ctrl)