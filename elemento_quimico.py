# quimanima/elemento_quimico.py

import csv
import os

categorias_validas = (
    'Actinídeo',
    'Ametal',
    'Gás Nobre',
    'Halogênio',
    'Lantanídeo',
    'Metal Alcalino',
    'Metal Alcalino-terroso',
    'Metal de Transição',
    'Metal-representativo',
    'Semi-metal',
)

diagrama_pauling = {}
diagrama_pauling[1,1] = 2
diagrama_pauling[2,1] = 2; diagrama_pauling[2,2] = 6
diagrama_pauling[3,1] = 2; diagrama_pauling[3,2] = 6; diagrama_pauling[3,3] = 10
diagrama_pauling[4,1] = 2; diagrama_pauling[4,2] = 6; diagrama_pauling[4,3] = 10; diagrama_pauling[4,4] = 14
diagrama_pauling[5,1] = 2; diagrama_pauling[5,2] = 6; diagrama_pauling[5,3] = 10; diagrama_pauling[5,4] = 14
diagrama_pauling[6,1] = 2; diagrama_pauling[6,2] = 6; diagrama_pauling[6,3] = 10
diagrama_pauling[7,1] = 2; diagrama_pauling[7,2] = 6

subniveis = {2:'s', 6:'p', 10:'d', 14:'f'}


class ElementoQuimico:
    
    def __init__(self, numero_atomico:int,
                 simbolo:str,
                 nome:str,
                 massa_atomica:float,
                 grupo:int,
                 periodo:int,
                 categoria:str):
        self._numero_atomico = int(numero_atomico)
        self._simbolo = simbolo
        self._nome = nome
        self._massa_atomica = float(massa_atomica)
        self._grupo = int(grupo)
        self._periodo = int(periodo)
        self._categoria = categoria
        self._camadas = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
        self.__distribuir_eletrons()

    def __str__(self):
        return self.nome
    
    def __repr__(self):
        return '<Elemento: {}, {}, {}>'.format(self._nome,
                                            self._simbolo,
                                            self._numero_atomico)
    
    @property
    def numero_atomico(self):
        return self._numero_atomico

    @property
    def simbolo(self):
        return self._simbolo

    @property
    def nome(self):
        return self._nome

    @property
    def massa_atomica(self):
        return self._massa_atomica

    @property
    def grupo(self):
        return self._grupo

    @property
    def periodo(self):
        return self._periodo

    @property
    def categoria(self):
        return self._categoria

    @property
    def camadas(self):
        return self._camadas

    # distribui os eletrons do átomo de acordo com o Diagrama de Pauling
    def __distribuir_eletrons(self): 
        global diagrama_pauling
        global subniveis
        numero_de_eletrons = self._numero_atomico
        for s in range(2,10):
            if s == 9:
                j = 4
                i = s - j
                # nmax_es: número máximo de elétrons no subnível
                # nes: número de elétrons no subnível
                # numerto_de_eletrons: número total de elétrons no átomo
                while j > 1:
                    nmax_es = diagrama_pauling.get((i,j),0)
                    if nmax_es != 0:
                        nes = nmax_es if (numero_de_eletrons > nmax_es)\
                              else numero_de_eletrons
                        self._camadas[i] += nes
                        numero_de_eletrons -= nes
                    j -= 1
                    i = s - j
                    if numero_de_eletrons == 0: break
                    
            elif s <= 5:
                i = 1
                j = s - i
                while i < s:
                    nmax_es = diagrama_pauling.get((i,j),0)
                    if nmax_es != 0:
                        nes = nmax_es if (numero_de_eletrons > nmax_es)\
                              else numero_de_eletrons
                        self._camadas[i] += nes
                        numero_de_eletrons -= nes   
                    i += 1
                    j = s - i
                    if numero_de_eletrons == 0: break
            else:
                j = 4
                i = s - j
                while j >= 1:
                    nmax_es = diagrama_pauling.get((i,j),0)
                    if nmax_es != 0:
                        nes = nmax_es if (numero_de_eletrons > nmax_es)\
                              else numero_de_eletrons
                        self._camadas[i] += nes
                        numero_de_eletrons -= nes
                    j -= 1
                    i = s - j
                    if numero_de_eletrons == 0: break
                    
            if numero_de_eletrons == 0: break
            
        toDel = {}
        for chave in self._camadas.keys():
            if self._camadas[chave] == 0:
                toDel[chave] = None
        for chave in toDel.keys():
            del self._camadas[chave]
        del toDel
    
    
def elementos_grupo(grupo:int):
    global elemento
    
    assert grupo in range(1, 18+1)
    
    lista = []
    for simbolo in elemento:
        if elemento[simbolo].grupo == grupo:
            lista.append(elemento[simbolo])

    return lista


def elementos_periodo(periodo:int):
    global elemento
    
    assert periodo in range(1, 7+1)
    
    lista = []
    for simbolo in elemento:
        if elemento[simbolo].periodo == periodo:
            lista.append(elemento[simbolo])

    return lista


def elementos_categoria(categoria:str):
    global elemento
    global categorias_validas
    
    assert categoria in categorias_validas
    
    lista = []
    for simbolo in elemento:
        if elemento[simbolo].categoria == categoria:
            lista.append(elemento[simbolo])

    return lista

def __gerar_imagens_elementos(caminho="."):
    global elemento
    modelo = '''
graph {simbolo} {{
  {simbolo} [shape = circle];
}}
'''
    comando = 'dot -Tgif {nome_arq_dot} -o {nome_arq_gif}'
    dir_dot = os.path.join(caminho, 'dot')
    dir_gif = os.path.join(caminho, 'gif')
    if not os.path.exists(dir_dot):
        os.makedirs(dir_dot)
        
    if not os.path.exists(dir_gif):
        os.makedirs(dir_gif)
        
    for simbolo in elemento:
        nome_arq_dot = os.path.join(dir_dot, '{}.dot'.format(simbolo))
        nome_arq_gif = os.path.join(dir_gif, '{}.gif'.format(simbolo))
        with open(nome_arq_dot, 'w') as arq_dot:
            arq_dot.write(modelo.format(simbolo=simbolo))
        
        # AFAZER: Verificar a existência do comando *dot*
        os.system(comando.format(nome_arq_dot=nome_arq_dot,
                                 nome_arq_gif=nome_arq_gif))


elemento = {}
def __carregar_atomos():
    with open('elementos.csv') as arquivo:
        arquivo.readline()
        registros = csv.reader(arquivo)
        for dados_atomo in registros:            
            atomo = ElementoQuimico(*dados_atomo)
            
            elemento[atomo.simbolo] = atomo
__carregar_atomos()
