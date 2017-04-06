from turtle import Screen, Turtle
from math import sqrt, pow
from random import randint
tela = Screen()
caneta = Turtle()
matriz_tela = {}
matriz_posicao = {}
class Particula(object):
    def __init__(self, cor):
        self._cor = cor
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.up()
        self._desenho.shape('circle')
        self._desenho.color(cor)
        self._desenho.shapesize(0.8)
        
    def _clonar(self):
        p = Particula(self._cor)
        return p
    
    def _colidir_particula(self, outras_particulas):
        particulas = outras_particulas[:]
        particulas.remove(self)
        for p in particulas:
            distancia_entre_particulas = sqrt(pow(self._desenho.xcor()-p._desenho.xcor(),2) + pow(self._desenho.ycor()-p._desenho.ycor(),2))
            if distancia_entre_particulas <= 10:
                self._desenho.right(randint(0,360))
                p._desenho.right(randint(0,360))
                    
    def _colidir_parede(self):
        if self._desenho.xcor() >= 600//2:
            x, y = self._desenho.position()
            self._desenho.setpos(595//2, y)
            self._desenho.setheading(randint(0,360))
            
        if self._desenho.xcor() <= -600//2:
            x, y = self._desenho.position()
            self._desenho.setpos(-595//2, y)
            self._desenho.setheading(randint(0,360))
            
        if self._desenho.ycor() >= 600//2:
            x, y = self._desenho.position()
            self._desenho.setpos(x, 595//2)
            self._desenho.setheading(randint(0,360))
            
        if self._desenho.ycor() <= -195:
            x, y = self._desenho.position()
            self._desenho.setpos(x, -190)
            self._desenho.setheading(randint(0,360))

    def _colidir_recipiente(self):
        if self._desenho.xcor() >= -99 and self._desenho.xcor() <= -97 and self._desenho.ycor() < 50:
            x, y = self._desenho.position()
            self._desenho.setpos(-96, y)
            self._desenho.setheading(80)
            
        if self._desenho.xcor() <= 99 and self._desenho.xcor() >= 97 and self._desenho.ycor() < 50:
            x, y = self._desenho.position()
            self._desenho.setpos(96, y)
            self._desenho.setheading(95)

        if self._desenho.xcor() >= -103 and self._desenho.xcor() <= -101 and self._desenho.ycor() < 50:
            x, y = self._desenho.position()
            self._desenho.setpos(-104, y)
            self._desenho.setheading(115)

        if self._desenho.xcor() <= 103 and self._desenho.xcor() >= 101 and self._desenho.ycor() < 50:
            x, y = self._desenho.position()
            self._desenho.setpos(104, y)
            self._desenho.setheading(45)

class Recipiente(object):
    def __init__(self):
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        
class Substancia(object):
    def __init__(self, materia: str, ponto_fusao: int, ponto_ebulicao: int, temperatura_inicial:int=0):
        self._temperatura = temperatura_inicial
        self._ponto_fusao = ponto_fusao
        self._ponto_ebulicao = ponto_ebulicao
        self._analisar_estado()
        self._particulas = []
        
    def _movimentar_particulas_gas(self):
        global tela
        tela.tracer(3)
        while self._estado == 'Gasoso':
            for i in range(len(self._particulas)):
                self._particulas[i]._desenho.fd(1)
                self._particulas[i]._colidir_particula(self._particulas)
                self._particulas[i]._colidir_parede()
                self._particulas[i]._colidir_recipiente()
            self._analisar_estado()

    def _movimentar_particulas_liquido(self):
        global tela
        tela.tracer(1)
        for i in range(len(self._particulas)):
            x, y = self._particulas[i]._desenho.position()
            self._particulas[i]._desenho.setpos(x, -186)
            self._particulas[i]._desenho.setheading(90)
        while self._estado == 'Líquido':
            for i in range(len(self._particulas)):
                if self._particulas[i]._desenho.ycor() > -180:
                    self._particulas[i]._desenho.setheading(270)
                if self._particulas[i]._desenho.ycor() < -186:
                    self._particulas[i]._desenho.setheading(90)
                self._particulas[i]._desenho.fd(5)
            self._analisar_estado()

    def _movimentar_particulas_solido(self):
        global tela
        tela.tracer(1)
        for i in range(len(self._particulas)):
            x, y = self._particulas[i]._desenho.position()
            self._particulas[i]._desenho.setpos(x, -186)
        while self._estado == 'Sólido':
            for i in range(len(self._particulas)):
                self._particulas[i]._desenho.fd(0)
            self._analisar_estado()
            
    def _analisar_estado(self):
        self._estado = 'Sólido' if self._temperatura < self._ponto_fusao else \
                       'Líquido' if self._temperatura < self._ponto_ebulicao else \
                       'Gasoso'
        
    def _alterar_quantidade_particulas(self, atomo):
        self._particulas.append(atomo)
        
    def aumentar_temperatura(self):
        global caneta
        self._temperatura += 10
        self._analisar_estado()
        caneta.clear()
        caneta.write('Temperatura: {} °C\nEstado Físico: {}'.format(self._temperatura, self._estado), False, align='left', font=('Times', 14, 'normal'))
        if self._estado == 'Gasoso': self._movimentar_particulas_gas()
        elif self._estado == 'Líquido': self._movimentar_particulas_liquido()
        else: self._movimentar_particulas_solido()

    def reduzir_temperatura(self):
        global caneta
        self._temperatura -= 10
        self._analisar_estado()
        caneta.clear()
        caneta.write('Temperatura: {} °C\nEstado Físico: {}'.format(self._temperatura, self._estado), False, align='left', font=('Times', 14, 'normal'))
        if self._estado == 'Gasoso': self._movimentar_particulas_gas()
        elif self._estado == 'Líquido': self._movimentar_particulas_liquido()
        else: self._movimentar_particulas_solido()

    @property
    def temperatura(self):return self._temperatura

    @property
    def estado(self):return self._estado    
    

def main():
    caneta.hideturtle()
    
    tela.setup(600,600)
    tela.title('Mudança de estado físico')
    
    recipiente = Recipiente()
    recipiente._desenho.up()
    recipiente._desenho.setpos(-300,-200)
    recipiente._desenho.down()
    recipiente._desenho.color('aquamarine')
    recipiente._desenho.begin_fill()
    for i in range(2):
        recipiente._desenho.fd(600)
        recipiente._desenho.left(90)
        recipiente._desenho.fd(500)        
        recipiente._desenho.left(90)
    recipiente._desenho.end_fill()
    recipiente._desenho.color('tan')
    recipiente._desenho.begin_fill()
    for i in range(2):
        recipiente._desenho.fd(600)
        recipiente._desenho.right(90)
        recipiente._desenho.fd(100)        
        recipiente._desenho.right(90)
    recipiente._desenho.end_fill()
    recipiente._desenho.color('black')
    x = -300 + 600/4
    for i in range(3):
        recipiente._desenho.setpos(x,-200)
        recipiente._desenho.left(210)
        recipiente._desenho.fd(20)
        recipiente._desenho.up()
        recipiente._desenho.setpos(x+10, -200)
        recipiente._desenho.down()
        recipiente._desenho.fd(20)
        recipiente._desenho.right(210)
        recipiente._desenho.up()
        recipiente._desenho.setpos(x, -200)
        recipiente._desenho.down()
        x += 600/4
    recipiente._desenho.setpos(300,-200)
    recipiente._desenho.up()
    recipiente._desenho.setpos(-100, 50)
    recipiente._desenho.down()
    recipiente._desenho.pensize(3)
    recipiente._desenho.setpos(-100, -200)
    recipiente._desenho.setpos(100, -200)
    recipiente._desenho.setpos(100, 50)
    recipiente._desenho.hideturtle()

    particula = Particula('blue')
    
    substancia = Substancia('água', 0, 100, -10)
    x, y = particula._desenho.position()
    x += -85
    y += -155
    for i in range(10):
        substancia._alterar_quantidade_particulas(particula._clonar())
        substancia._particulas[i]._desenho.setpos(x, y)
        if i%2 == 0: substancia._particulas[i]._desenho.setheading(0)
        else: substancia._particulas[i]._desenho.setheading(180)
        x += 24
    x, y = particula._desenho.position()
    x += -85
    y += -180
    for i in range(10,20):
        substancia._alterar_quantidade_particulas(particula._clonar())
        substancia._particulas[i]._desenho.setpos(x, y)
        if i%2 == 0: substancia._particulas[i]._desenho.setheading(0)
        else: substancia._particulas[i]._desenho.setheading(180)
        x += 24
    particula._desenho.hideturtle()
    
    tela.listen()
    tela.onkey(substancia.reduzir_temperatura, 'Left')
    tela.onkey(substancia.reduzir_temperatura, 'Down')
    #tela.onkey(substancia.reduzir_temperatura, '-')
    tela.onkey(substancia.aumentar_temperatura, 'Right')
    tela.onkey(substancia.aumentar_temperatura, 'Up')
    #tela.onkey(substancia.aumentar_temperatura, '+')

    caneta.speed('fastest')
    caneta.hideturtle()
    caneta.up()
    caneta.setposition(-290,250)
    caneta.down()
    caneta.write('Temperatura: {} °C\nEstado Físico: {}'.format(substancia.temperatura, substancia.estado), False, align='left', font=('Times', 14, 'normal'))

    def desenha(x1, y1, x2, y2):
        caneta.up()
        caneta.setpos(x1, y1)
        caneta.down()
        caneta.setpos(x2, y2)
    
    for k in range(600//20):
        x = -300 + k*20
        y = 300 - k*20
        desenha(-300, y, 300, y)
        desenha(x, 300, x, -200)

    for i in range(1,26):
        for j in range(1,31): matriz_tela[(i,j)] = False
    
    for i in range(24, 26):
        for j in range(11,21): matriz_tela[i,j] = True

    largura = 20
    linha = 0
    for i in range(-300, 301):
        for j in range(-300, 301):
            matriz_posicao[i+linha+largura//2,j+largura//2] = (i+linha+largura//2,j+largura//2)
        
        
    def exibir_posicao(x, y):
        print('({}, {})'.format(x, y))
        i = ((300-y)//20)+1
        j = ((x+300)//20)+1
        print('a[{},{}]'.format(int(i),int(j)))
        
    tela.onclick(exibir_posicao)
    
    if substancia.estado == 'Sólido': substancia._movimentar_particulas_solido()
    elif substancia.estado == 'Líquido': substancia._movimentar_particulas_liquido()
    else: substancia._movimentar_particulas_gas()

if __name__ == '__main__': main()
