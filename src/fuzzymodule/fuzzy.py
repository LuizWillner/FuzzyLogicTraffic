import random
import matplotlib as plt
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
from utils.generalconfig import PessoaState, VeiculoState, SemaforoAbertoState



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
pessoa = ctrl.Antecedent(np.arange(0,60,1), PessoaState.get_var_name())
veiculo = ctrl.Antecedent(np.arange(0,100,1), VeiculoState.get_var_name())
aberto = ctrl.Consequent(np.arange(0,100,1), SemaforoAbertoState.get_var_name())

# Fuzzificação 
pessoa[PessoaState.MUITO_BAIXO.value] = fuzz.trapmf(pessoa.universe, [0,  0,  5, 10])
pessoa[PessoaState.BAIXO.value] = fuzz.trapmf(pessoa.universe, [5, 10, 15, 20])
pessoa[PessoaState.MEDIO.value] = fuzz.trapmf(pessoa.universe, [15, 20, 25, 30])
pessoa[PessoaState.ALTO.value] = fuzz.trapmf(pessoa.universe, [25, 30, 35, 40])
pessoa[PessoaState.MUITO_ALTO.value] = fuzz.trapmf(pessoa.universe, [35, 40, 60, 60])

veiculo[VeiculoState.MUITO_BAIXO.value] = fuzz.trapmf(veiculo.universe, [0,0, 5,10])
veiculo[VeiculoState.BAIXO.value] = fuzz.trapmf(veiculo.universe, [5, 10, 15, 25])
veiculo[VeiculoState.MEDIO.value] = fuzz.trapmf(veiculo.universe, [15,25, 30,40])
veiculo[VeiculoState.ALTO.value] = fuzz.trapmf(veiculo.universe, [30,40, 50,60])
veiculo[VeiculoState.MUITO_ALTO.value] = fuzz.trapmf(veiculo.universe, [50,60,100,100])

### Fuzzificação dos termos linguísticos do consequente
aberto[SemaforoAbertoState.MAIS_FECHADO.value]= fuzz.trapmf(aberto.universe, [0,0,15, 30])
aberto[SemaforoAbertoState.FECHADO.value]= fuzz.trimf(aberto.universe, [15,30,45])
aberto[SemaforoAbertoState.EQUILIBRADO.value]= fuzz.trimf(aberto.universe, [30,45,60])
aberto[SemaforoAbertoState.ABERTO.value]= fuzz.trimf(aberto.universe, [45,60,75])
aberto[SemaforoAbertoState.MAIS_ABERTO.value] = fuzz.trapmf(aberto.universe, [60,75,100,100])

# Maquina de Inferência 
rule_MaisAberto  = ctrl.Rule(
        (pessoa[PessoaState.MUITO_BAIXO.value] & (veiculo[VeiculoState.MEDIO.value] | veiculo[VeiculoState.ALTO.value] | veiculo[VeiculoState.MUITO_ALTO.value])) | 
        (pessoa[PessoaState.BAIXO.value] & (veiculo[VeiculoState.ALTO.value] | veiculo[VeiculoState.MUITO_ALTO.value])) | 
        (pessoa[PessoaState.MEDIO.value] & veiculo[VeiculoState.MUITO_ALTO.value]), 
    aberto[SemaforoAbertoState.MAIS_ABERTO.value]
)
rule_Aberto = ctrl.Rule(
        (pessoa[PessoaState.MUITO_BAIXO.value] & veiculo[VeiculoState.BAIXO.value]) | 
        (pessoa[PessoaState.BAIXO.value] & veiculo[VeiculoState.MEDIO.value]) | 
        (pessoa[PessoaState.MEDIO.value] & veiculo[VeiculoState.ALTO.value]) | 
        (pessoa[PessoaState.ALTO.value] & veiculo[VeiculoState.MUITO_ALTO.value]), 
    aberto[SemaforoAbertoState.ABERTO.value]
)
rule_Equilibrado  = ctrl.Rule (
        (veiculo [VeiculoState.MUITO_BAIXO.value] & pessoa [PessoaState.MUITO_BAIXO.value]) | 
        (veiculo [VeiculoState.MUITO_BAIXO.value] & pessoa [PessoaState.BAIXO.value]) | 
        (veiculo [VeiculoState.BAIXO.value] & pessoa [PessoaState.BAIXO.value]) | 
        (veiculo [VeiculoState.BAIXO.value] & pessoa [PessoaState.MEDIO.value]) | 
        (veiculo [VeiculoState.MEDIO.value] & pessoa [PessoaState.MEDIO.value]) | 
        (veiculo [VeiculoState.MEDIO.value] & pessoa [PessoaState.ALTO.value]) | 
        (veiculo [VeiculoState.ALTO.value] & pessoa [PessoaState.ALTO.value]) | 
        (veiculo [VeiculoState.ALTO.value] & pessoa [PessoaState.MUITO_ALTO.value]) | 
        (veiculo [VeiculoState.MUITO_ALTO.value] & pessoa [PessoaState.MUITO_ALTO.value]), 
    aberto[SemaforoAbertoState.EQUILIBRADO.value]
)
rule_Fechado = ctrl.Rule(
        (pessoa[PessoaState.MEDIO.value] & veiculo[VeiculoState.MUITO_BAIXO.value]) |
        (pessoa[PessoaState.ALTO.value] & veiculo[VeiculoState.BAIXO.value]) |
        (pessoa[PessoaState.MUITO_ALTO.value] & veiculo[VeiculoState.MEDIO.value]), 
    aberto[SemaforoAbertoState.FECHADO.value]
)
rule_MaisFechado  = ctrl.Rule(
        ((pessoa[PessoaState.ALTO.value] | pessoa[PessoaState.MUITO_ALTO.value])& veiculo[VeiculoState.MUITO_BAIXO.value]) | 
        (pessoa[PessoaState.MUITO_ALTO.value] & veiculo[VeiculoState.BAIXO.value]), 
    aberto[SemaforoAbertoState.MAIS_FECHADO.value]
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
