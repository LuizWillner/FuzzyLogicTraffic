import enum

OUTPUT_PATH = 'output/'


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
    @classmethod
    def get_var_name(cls):
        return 'pessoas'
 
class VeiculoState(State):
    MUITO_BAIXO = 'muito baixo'
    BAIXO = 'baixo'
    MEDIO = 'medio'
    ALTO = 'alto'
    MUITO_ALTO = 'muito alto'
    @classmethod
    def get_var_name(cls):
        return 'veiculos'

class SemaforoAbertoState(State):
    MAIS_FECHADO = 'Mais Fechado'
    FECHADO = 'Fechado'
    EQUILIBRADO = 'Equilibrado'
    ABERTO = 'Aberto'
    MAIS_ABERTO = 'Mais Aberto'
    @classmethod
    def get_var_name(cls):
        return 'tempo'