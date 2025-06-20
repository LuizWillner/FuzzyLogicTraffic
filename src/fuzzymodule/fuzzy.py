import random
import enum
import matplotlib as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl


class State(enum.Enum):
    @classmethod
    def values(cls):
        return [state.value for state in cls]

class PessoaState(State):
    MUITO_BAIXO = 'muito baixo'
    BAIXO = 'baixo'
    MEDIO = 'medio'
    ALTO = 'alto'
    MUITO_ALTO = 'muito alto'
    def get_var_name(cls):
        return 'pessoas'
 
class VeiculoState(State):
    MUITO_BAIXO = 'muito baixo'
    BAIXO = 'baixo'
    MEDIO = 'medio'
    ALTO = 'alto'
    MUITO_ALTO = 'muito alto'
    def get_var_name(cls):
        return 'veiculos'

class SemaforoAbertoState(State):
    MAIS_FECHADO = 'Mais Fechado'
    FECHADO = 'Fechado'
    EQUILIBRADO = 'Equilibrado'
    ABERTO = 'Aberto'
    MAIS_ABERTO = 'Mais Aberto'
    def get_var_name(cls):
        return 'tempo'


def fuzzy_decision_rules(veiculo: str, pessoa: str) -> str:
    '''
    Função que recebe a quantidade de veículos e pessoas e retorna a decisão do semáforo
    de acordo com as regras fuzzy definidas na main. Não serve para o módulo fuzzy e a 
    simulação em si, apenas para outros componentes do sistema que necessitem da aplicação
    das regras (por exemplo, a geração do heatmap das regras).
    '''
    if (
        (
            pessoa == PessoaState.MUITO_BAIXO.value and 
            veiculo in [VeiculoState.MEDIO.value, VeiculoState.ALTO.value, VeiculoState.MUITO_ALTO.value]
        ) or
        (
            pessoa == PessoaState.BAIXO.value and 
            veiculo in [VeiculoState.ALTO.value, VeiculoState.MUITO_ALTO.value]
        ) or
        (
            pessoa == PessoaState.MEDIO.value and 
            veiculo == VeiculoState.MUITO_ALTO.value
        )
    ):
        return SemaforoAbertoState.MAIS_ABERTO.value
    
    if (
        (pessoa == PessoaState.MUITO_BAIXO.value and veiculo == VeiculoState.BAIXO.value) or
        (pessoa == PessoaState.BAIXO.value and veiculo == VeiculoState.MEDIO.value) or
        (pessoa == PessoaState.MEDIO.value and veiculo == VeiculoState.ALTO.value) or
        (pessoa == PessoaState.ALTO.value and veiculo == VeiculoState.MUITO_ALTO.value)
    ):
        return SemaforoAbertoState.ABERTO.value
    
    if (
        (veiculo == VeiculoState.MUITO_BAIXO.value and pessoa == PessoaState.MUITO_BAIXO.value) or
        (veiculo == VeiculoState.MUITO_BAIXO.value and pessoa == PessoaState.BAIXO.value) or
        (veiculo == VeiculoState.BAIXO.value and pessoa == PessoaState.BAIXO.value) or
        (veiculo == VeiculoState.BAIXO.value and pessoa == PessoaState.MEDIO.value) or
        (veiculo == VeiculoState.MEDIO.value and pessoa == PessoaState.MEDIO.value) or
        (veiculo == VeiculoState.MEDIO.value and pessoa == PessoaState.ALTO.value) or
        (veiculo == VeiculoState.ALTO.value and pessoa == PessoaState.ALTO.value) or
        (veiculo == VeiculoState.ALTO.value and pessoa == PessoaState.MUITO_ALTO.value) or
        (veiculo == VeiculoState.MUITO_ALTO.value and pessoa == PessoaState.MUITO_ALTO.value)
    ):
        return SemaforoAbertoState.EQUILIBRADO.value
    
    if (
        (pessoa == PessoaState.MEDIO.value and veiculo == VeiculoState.MUITO_BAIXO.value) or
        (pessoa == PessoaState.ALTO.value and veiculo == VeiculoState.BAIXO.value) or
        (pessoa == PessoaState.MUITO_ALTO.value and veiculo == VeiculoState.MEDIO.value)
    ):
        return SemaforoAbertoState.FECHADO.value
    
    if (
        (pessoa in [PessoaState.ALTO.value, PessoaState.MUITO_ALTO.value] and veiculo == VeiculoState.MUITO_BAIXO.value) or
        (pessoa == PessoaState.MUITO_ALTO.value and veiculo == VeiculoState.BAIXO.value)
    ):
        return SemaforoAbertoState.MAIS_FECHADO.value
    
    return '-'


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
rule_MaisAberto  = ctrl.Rule(
        (pessoa['muito baixo'] & (veiculo['medio'] | veiculo['alto'] | veiculo['muito alto'])) | 
        (pessoa['baixo'] & (veiculo['alto'] | veiculo['muito alto'])) | 
        (pessoa['medio'] & veiculo['muito alto']), 
    aberto['Mais Aberto']
)
rule_Aberto = ctrl.Rule(
        (pessoa['muito baixo'] & veiculo['baixo']) | 
        (pessoa['baixo'] & veiculo['medio']) | 
        (pessoa['medio'] & veiculo['alto']) | 
        (pessoa['alto'] & veiculo['muito alto']), 
    aberto['Aberto']
)
rule_Equilibrado  = ctrl.Rule (
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
rule_Fechado = ctrl.Rule(
        (pessoa['medio'] & veiculo['muito baixo']) |
        (pessoa['alto'] & veiculo['baixo']) |
        (pessoa['muito alto'] & veiculo['medio']), 
    aberto['Fechado']
)
rule_MaisFechado  = ctrl.Rule(
        ((pessoa['alto'] | pessoa['muito alto'])& veiculo['muito baixo']) | 
        (pessoa['muito alto'] & veiculo['baixo']), 
    aberto['Mais Fechado']
)
aberto_ctrl = ctrl.ControlSystem(
    [
        rule_MaisAberto, 
        rule_Aberto, 
        rule_Equilibrado, 
        rule_Fechado, 
        rule_MaisFechado
    ]
)
