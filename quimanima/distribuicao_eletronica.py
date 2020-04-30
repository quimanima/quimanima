# quimanima/distribuicao_eletronica.py

import elemento_quimico
from turtle import Turtle, Screen, Pen
from math import sqrt, pi, sin, cos
from random import choice

#=========================#
# DISTRIBUIÇÃO ELETRÔNICA #
#-------------------------#
#   1s2                   #
#   2s2  2p6              #
#   3s2  3p6  3d10        #
#   4s2  4p6  4d10  4f14  #  
#   5s2  5p6  5d10  5f14  #
#   6s2  6p6  6d10        #
#   7s2  7p6              #
#_________________________#

tela = Screen()
caneta = Pen()
caneta.hideturtle()

raio_camada = (70, 85, 100, 115, 130, 145, 160)

subniveis = elemento_quimico.subniveis
diagrama_pauling = elemento_quimico.diagrama_pauling

cores = ('blue',
         'red',
         'yellow',
         'green',
         'aquamarine',
         'orange',
         'purple',
         'pink',
         'gray',
         'black')

class ElementoDistribuicao:
    def __init__(self, simbolo):       
        self.elemento = elemento_quimico.elemento[simbolo]

        self._distribuicao_eletronica = {}
        self._distribuir_eletrons()
        
        self._raio = 0
        
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.shape('circle')
        self._desenho.color(choice(cores))
        
        self._eletron = Turtle()
        self._eletron.speed('fastest')
        self._eletron.shape('circle')
        self._eletron.shapesize(0.3,0.3)
        self._eletron.color('black','red')
        self._eletron.hideturtle()
        self._eletron.up()

    def marcar(self):
        self._desenho.stamp()
    
    def imprimir(self):
        self._exibir_eletrons()
        self._imprimir_dados()
        self._imprimir_distribuicao_eletronica()

    # mostra todos os elétrons do átomo em suas respectivas camadas
    def _exibir_eletrons(self): 
        global raio_camada
        global tela
        
        x1, y1 = self._desenho.position()
        
        self._eletron.showturtle()
        
        parar = False
        
        for i in range(len(self.elemento.camadas)):
            aparecer = 1
            a = raio_camada[i]
            b = a
            for angulo in range(360):
                ang_rad = pi*angulo/180
                r = (a * b)/   \
                    sqrt(a**2*sin(ang_rad)**2 + b**2*cos(ang_rad)**2)
                
                x = r*cos(pi*angulo/180) + x1
                y = r*sin(pi*angulo/180) + y1
                
                if angulo == 0:
                    self._eletron.up()
                    self._eletron.setpos(x, y)
                    self._eletron.showturtle()
                    self._eletron.down()
                self._eletron.setpos(x, y)
                aparecer += 1
                
                if aparecer >= 360//self.elemento.camadas[i+1]\
                   and i+1 == len(self.elemento.camadas)\
                   and angulo == 356 and self.elemento.grupo == 17:
                    aparecer = 1
                    self._eletron.stamp()
                    parar = True
                    
                else:
                    if aparecer > 360/self.elemento.camadas[i+1]:
                        aparecer = 1
                        self._eletron.stamp()
                        
                if parar == True: break              
            if parar == True: break
            
        self._raio = r

    # mostrar a distribuição de acordo com o Diagrama de Pauling
    def _imprimir_distribuicao_eletronica(self):
        x, y = self._desenho.position()
        cor = self._desenho.color()
        espaco = ''    
        self._desenho.setheading(270)
        self._desenho.stamp()
        self._desenho.up()
        self._desenho.setpos(self._raio+20+x, self._raio+y)
        self._desenho.pencolor('black')
        self._desenho.write('Distribuição eletrônica do {}'.format(self.elemento.simbolo),
                            False,
                            align = 'left',
                            font = ('Times', 13, 'normal'))
        
        self._desenho.fd(20)
        for i in range(1, 8):
            for j in range(1, i+1):
                if self._distribuicao_eletronica.get((i,j),0) != 0:                    
                    self._desenho.write('{}{}'.format(espaco,
                                                      self._distribuicao_eletronica[i,j]),
                                        False,
                                        align='left',
                                        font=('Times', 13, 'normal'))
                    
                    espaco += '           '
            espaco = ''
            self._desenho.fd(20)
        self._desenho.setpos(x,y)
        self._desenho.color('white')
        self._desenho.stamp()
        self._desenho.color(cor[0])

    # mostra o número atômico, o nome e a massa do átomo
    def _imprimir_dados(self): 
        cor = self._desenho.color()
        x, y = self._desenho.position()
        
        self._desenho.stamp()
        self._desenho.setheading(90)
        self._desenho.up()
        self._desenho.fd(70 + len(self.elemento.camadas)*15)
        self._desenho.color('black')
        self._desenho.write(self.elemento.nome,
                           False,
                           align='center',
                           font=('Times', 13, 'normal'))
        
        self._desenho.forward(15)
        self._desenho.write(self.elemento.numero_atomico,
                           False,
                           align='center', font=('Times', 13, 'normal'))
        
        self._desenho.backward((15 + (70+len(self.elemento.camadas)*15))*2)
        self._desenho.write(self.elemento.massa_atomica,
                           False,
                           align='center',
                           font=('Times', 10, 'normal'))
        self._desenho.setpos(x,y)
        self._desenho.down()
        self._desenho.color(cor[0])

    # distribui os eletrons do átomo de acordo com o Diagrama de Pauling
    def _distribuir_eletrons(self):        
        numero_de_eletrons = self.elemento.numero_atomico
        
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
                        numero_de_eletrons -= nes
                        self._distribuicao_eletronica[i,j]='{}{}{}'.format(i,
                                                                           subniveis[nmax_es],
                                                                           nes)
                    else:
                        self._distribuicao_eletronica[i,j] = 0                        
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
                        numero_de_eletrons -= nes   
                        self._distribuicao_eletronica[i,j]='{}{}{}'.format(i,
                                                                          subniveis[nmax_es],
                                                                          nes)
                    else:
                        self._distribuicao_eletronica[i,j] = 0
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
                        numero_de_eletrons -= nes
                        self._distribuicao_eletronica[i,j]='{}{}{}'.format(i,
                                                                           subniveis[nmax_es],
                                                                           nes)
                    else:
                        self._distribuicao_eletronica[i,j] = 0
                    j -= 1
                    i = s - j
                    if numero_de_eletrons == 0: break
            if numero_de_eletrons == 0: break
            
        toDel = {}
        for chave in self.elemento.camadas.keys():
            if self.elemento.camadas[chave] == 0:
                toDel[chave] = None
        for chave in toDel.keys():
            del self.elemento.camadas[chave]
        del toDel

      
def main():
    try: 
        outro_elemento = True
        while outro_elemento == True:
            tela.title("Distribuição Eletrônica")
            tela.reset()
            tela.clear()
            tela.tracer(2)
            tela.setup(810, 600)

            id_atomo = tela.textinput("Identificação do Elemento",
                                   """
    Digite o símbolo ou o nome de um elemento
    Ex: H ou Hidrogênio""")

            id_atomo = id_atomo.lower()
            id_atomo = id_atomo[0].upper() + id_atomo[1::]
                
            for e in elemento_quimico.elemento:
                funcionou = False
                if elemento_quimico.elemento[e].nome == id_atomo or\
                   elemento_quimico.elemento[e].simbolo == id_atomo:
                    atomo = ElementoDistribuicao(e)
                    atomo.imprimir()
                    funcionou = True
                    atomo.marcar()
                    break
               
            if funcionou == False:
                tela.reset()
                tela.clear()
                caneta.write('Você informou indevidamente o símbolo ou nome do elemento!',
                              False,
                              align='center',
                              font=('Times', 13, 'normal'))

            for i in range(20): pass

            sim_ou_nao = tela.textinput('Novo elemento',
                                        '''
    Deseja ver a distribuição
    de outro elemento?
    Digite 'S' para Sim
    ou 'N' para Não
    ''')
            sim_ou_nao = sim_ou_nao.lower()
            outro_elemento = True if sim_ou_nao == 's'\
                             or sim_ou_nao == 'sim'\
                             else False

        tela.reset()
        tela.clear()
        caneta.write('Clique AQUI para fechar...',
                     False,
                     align='center',
                     font=('Times', 13, 'normal'))
        
        tela.exitonclick()
    except:
        pass
    

if __name__ == "__main__":
    main()
