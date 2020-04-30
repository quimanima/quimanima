# quimanima/estado_fisico.py

from turtle import Screen, Turtle, Pen
from math import sqrt
from random import randint, choice

tela = Screen()
caneta_cenario = Pen()
caneta_dados = Pen()
cores = ('blue',
          'red',
          'yellow',
          'green',
          'orange',
          'purple',
          'pink',
          'gray',
          'black',
          'white')


class Recipiente:
    def __init__(self):
        self._desenho = Turtle()
        self._desenho.speed('fastest')

    def subir(self):
        self._desenho.up()

    def mudar_posicao(self, x:float=0, y:float=0):
        self._desenho.setpos(x, y)

    def descer(self):
        self._desenho.down()

    def mudar_largura_caneta(self, tamanho:float=1.0):
        self._desenho.pensize(tamanho)
        
    def desaparecer(self):
        self._desenho.hideturtle()
        

class Particula:
    def __init__(self, cor:str):
        self._desenho = Turtle()
        self._cor = cor
        self._desenho.speed('fastest')
        self._desenho.up()
        self._desenho.shape('circle')
        self._desenho.color(self._cor)
        self._desenho.shapesize(0.8)
    
    def clonar(self):
        return Particula(self._cor)

    def verificar_posicao(self):
        return self._desenho.position()

    def mudar_posicao(self, x:float=0, y:float=0):
        self._desenho.setpos(x, y)

    def mudar_direcao(self, angulo:float=0):
        self._desenho.setheading(angulo)

    def mover_para_frente(self, distancia:float=10):
        self._desenho.forward(distancia)
        
    def desaparecer(self):
        self._desenho.hideturtle()

    def virar_direita(self, angulo:float=0):
        self._desenho.right(angulo)
    
    def colidir_particula(self, outras_particulas:list):
        particulas = outras_particulas[:]
        particulas.remove(self)
        for p in particulas:
            x_self, y_self = self.verificar_posicao()
            x_p, y_p = p.verificar_posicao()
            xcor = x_self - x_p
            ycor = y_self - y_p
            distancia_entre_particulas = sqrt(xcor**2 + ycor**2)
            if distancia_entre_particulas <= 10:
                self.virar_direita(randint(0, 360))
                p.virar_direita(randint(0, 360))
                    
    def colidir_parede(self):
        x_self, y_self = self.verificar_posicao()
        if x_self >= 600//2:
            self.mudar_posicao(595//2, y_self)
            self.mudar_direcao(randint(0,360))
            
        if x_self <= -600//2:
            self.mudar_posicao(-595//2, y_self)
            self.mudar_direcao(randint(0, 360))
            
        if y_self >= 600//2:
            self.mudar_posicao(x_self, 595//2)
            self.mudar_direcao(randint(0, 360))
            
        if y_self <= -195:
            self.mudar_posicao(x_self, -190)
            self.mudar_direcao(randint(0,360))

    def colidir_recipiente(self):
        x_self, y_self = self.verificar_posicao()
        if x_self >= -99\
           and x_self <= -97\
           and y_self < 50:
            self.mudar_posicao(-96, y_self)
            self.mudar_direcao(80)
            
        if x_self <= 99\
           and x_self >= 97\
           and y_self < 50:
            self.mudar_posicao(96, y_self)
            self.mudar_direcao(95)

        if x_self >= -103\
           and x_self <= -101\
           and y_self < 50:
            self.mudar_posicao(-104, y_self)
            self.mudar_direcao(115)

        if x_self <= 103\
           and x_self >= 101\
           and y_self < 50:
            self.mudar_posicao(104, y_self)
            self.mudar_direcao(45)
        

class Substancia:
    def __init__(self, materia: str,
                 ponto_fusao: int,
                 ponto_ebulicao: int,
                 temperatura_ambiente:float=20):
        self._materia = materia
        self._ponto_fusao = ponto_fusao
        self._ponto_ebulicao = ponto_ebulicao
        self._temperatura = temperatura_ambiente
        self._analisar_estado()
        self.particulas = []

    @property
    def materia(self):
        return self._materia

    @property
    def ponto_fusao(self):
        return self._ponto_fusao

    @property
    def ponto_ebulicao(self):
        return self._ponto_ebulicao

    @property
    def temperatura(self):
        return self._temperatura

    @property
    def estado(self):
        return self._estado
    
    def movimentar_particulas_solido(self):
        global tela
        for p in self.particulas:
            x, y = p.verificar_posicao()
            p.mudar_posicao(x, -186)
        while self._estado == 'Sólido':
            for p in self.particulas:
                p.mover_para_frente(0)
            self._analisar_estado()
            
    def movimentar_particulas_liquido(self):
        global tela
        tela.tracer(1)
        for p in self.particulas:
            x, y = p.verificar_posicao()
            p.mudar_posicao(x, -186)
            p.mudar_direcao(90)
        while self._estado == 'Líquido':
            for p in self.particulas:
                x_p, y_p = p.verificar_posicao()
                if y_p > -180:
                    p.mudar_direcao(270)
                if y_p < -186:
                    p.mudar_direcao(90)
                p.mover_para_frente(5)
            self._analisar_estado()
        
    def movimentar_particulas_gas(self):
        global tela
        tela.tracer(6)
        while self._estado == 'Gasoso':
            for p in self.particulas:
                p.mover_para_frente(1)
                p.colidir_particula(self.particulas)
                p.colidir_parede()
                p.colidir_recipiente()
            self._analisar_estado()

    def _analisar_estado(self):
        if self._temperatura < self._ponto_fusao:
            self._estado = 'Sólido'
        elif self._temperatura < self._ponto_ebulicao:
            self._estado = 'Líquido'
        else:
            self._estado = 'Gasoso'
        
    def alterar_quantidade_particulas(self, atomo):
        self.particulas.append(atomo)
        
    def aumentar_temperatura(self):
        global caneta_dados
        
        self._temperatura += 10
        self._analisar_estado()
        caneta_dados.clear()
        caneta_dados.write('''Substância: {}
Ponto de fusão: {} °C
Ponto de ebulição: {} °C
Temperatura: {} °C
Estado físico: {}'''.format(self._materia,
                            self._ponto_fusao,
                            self._ponto_ebulicao,
                            self._temperatura,
                            self._estado),
                      False,
                      align='left',
                      font=('Times', 14, 'normal'))
        
        if self._estado == 'Gasoso':
            self.movimentar_particulas_gas()
        elif self._estado == 'Líquido':
            self.movimentar_particulas_liquido()
        else:
            self.movimentar_particulas_solido()

    def reduzir_temperatura(self):
        global caneta_dados
        self._temperatura -= 10
        self._analisar_estado()
        caneta_dados.clear()
        caneta_dados.write('''Substância: {}
Ponto de fusão: {} °C
Ponto de ebulição: {} °C
Temperatura: {} °C
Estado físico: {}'''.format(self._materia,
                            self._ponto_fusao,
                            self._ponto_ebulicao,
                            self._temperatura,
                            self._estado),
                      False,
                      align='left',
                      font=('Times', 14, 'normal'))
        
        if self._estado == 'Gasoso':
            self.movimentar_particulas_gas()
        elif self._estado == 'Líquido':
            self.movimentar_particulas_liquido()
        else:
            self.movimentar_particulas_solido()    


def main():
    try:
        tela.setup(600,600)
        tela.title('Mudança de estado físico')

        caneta_cenario.speed('fastest')
        caneta_dados.speed('fastest')
        
        caneta_cenario.up()
        caneta_cenario.setpos(-300,-200)
        caneta_cenario.down()
        caneta_cenario.color('aquamarine')  
        
        caneta_cenario.begin_fill()
        for i in range(2):
            caneta_cenario.fd(600)
            caneta_cenario.left(90)
            caneta_cenario.fd(500)        
            caneta_cenario.left(90)
        caneta_cenario.end_fill()
        
        caneta_cenario.color('tan')
        caneta_cenario.begin_fill()
        for i in range(2):
            caneta_cenario.fd(600)
            caneta_cenario.right(90)
            caneta_cenario.fd(100)        
            caneta_cenario.right(90)
        caneta_cenario.end_fill()

        caneta_cenario.color('black')
        x = -300 + 600/4
        for i in range(3):
            caneta_cenario.setpos(x,-200)
            caneta_cenario.left(210)
            caneta_cenario.fd(20)
            caneta_cenario.up()
            caneta_cenario.setpos(x+10, -200)
            caneta_cenario.down()
            caneta_cenario.fd(20)
            caneta_cenario.right(210)
            caneta_cenario.up()
            caneta_cenario.setpos(x, -200)
            caneta_cenario.down()
            x += 600/4

        caneta_cenario.setpos(300,-200)
        caneta_cenario.hideturtle()

        titulo = 'Substância'
        subtitulo = 'Informe o nome da substância\nEx: Água'
        material = tela.textinput(titulo, subtitulo)

        titulo = 'Ponto de Fusão'
        subtitulo = 'Informe o ponto de fusão em graus Celcius\nEx: 0'
        ponto_fusao = tela.textinput(titulo, subtitulo)
        ponto_fusao = float(ponto_fusao.replace(',', '.'))

        titulo = 'Ponto de Ebulição'
        subtitulo = 'Informe o ponto de ebulição em graus Celcius\nEx: 100'
        ponto_ebulicao = tela.textinput(titulo, subtitulo)
        ponto_ebulicao = float(ponto_ebulicao.replace(',', '.')) 

        recipiente = Recipiente()   
        substancia = Substancia(material, ponto_fusao, ponto_ebulicao)
        particula = Particula(choice(cores))

        recipiente.subir()
        recipiente.mudar_posicao(-100, 50)
        recipiente.descer()
        recipiente.mudar_largura_caneta(3)
        recipiente.mudar_posicao(-100, -200)
        recipiente.mudar_posicao(100, -200)
        recipiente.mudar_posicao(100, 50)
        recipiente.desaparecer()
        
        x, y = particula.verificar_posicao()
        x += -85
        y += -155
        for i in range(8):
            substancia.alterar_quantidade_particulas(particula.clonar())
            substancia.particulas[i].mudar_posicao(x, y)
            if i%2 == 0: substancia.particulas[i].mudar_direcao(0)
            else: substancia.particulas[i].mudar_direcao(180)
            x += 24
            
        x, y = particula.verificar_posicao()
        x += -85
        y += -180
        
        for i in range(8,16):
            substancia.alterar_quantidade_particulas(particula.clonar())
            substancia.particulas[i].mudar_posicao(x, y)
            if i%2 == 0: substancia.particulas[i].mudar_direcao(0)
            else: substancia.particulas[i].mudar_direcao(180)
            x += 24
        particula.desaparecer()
        
        tela.listen()
        tela.onkey(substancia.reduzir_temperatura, 'Left')
        tela.onkey(substancia.reduzir_temperatura, 'Down')
        tela.onkey(substancia.reduzir_temperatura, '-')
        tela.onkey(substancia.aumentar_temperatura, 'Right')
        tela.onkey(substancia.aumentar_temperatura, 'Up')
        tela.onkey(substancia.aumentar_temperatura, '+')

        caneta_dados.hideturtle()
        caneta_dados.up()
        caneta_dados.setposition(-290,190)
        caneta_dados.down()
        caneta_dados.write('''Substância: {}
Ponto de fusão: {} °C
Ponto de ebulição: {} °C
Temperatura: {} °C
Estado físico: {}'''.format(substancia.materia,
                                substancia.ponto_fusao,
                                substancia.ponto_ebulicao,
                                substancia.temperatura,
                                substancia.estado),
                     False,
                     align='left',
                     font=('Times', 14, 'normal'))

        if substancia.estado == 'Sólido':
            substancia.movimentar_particulas_solido()
        elif substancia.estado == 'Líquido':
            substancia.movimentar_particulas_liquido()
        else:
            substancia.movimentar_particulas_gas()
    except: exit()
    

if __name__ == '__main__':
    main()
