from turtle import Turtle, Screen
from random import randint
from math import sqrt, pow, cos, sin, acos, pi

tela = Screen()

class Particula_Alfa(object):
    def __init__(self):
        self._desenho = Turtle()
        self._desenho.color('red')
        self._desenho.shapesize(0.3,0.3)
        self._desenho.shape('circle')
        self._desenho.speed('fastest')
        self._angulo = 0

    def vetor_deslocamento(self):
        ang = self._angulo
        ang_rad = (pi*ang)/180
        return (cos(ang_rad), sin(ang_rad))
    
    def movimentar_particula(self, atomos):
        self._desenho.down()
        x, y = self._desenho.position()
        self._angulo = randint(-30, 25) # em graus
        
        self._desenho.setheading(self._angulo)
        while True:
            colidir = False
            while (self._desenho.xcor() < 500)\
                  and (self._desenho.xcor() > -500)\
                  and (self._desenho.ycor() < 300)\
                  and (self._desenho.ycor() > -300):
                self._desenho.fd(3)
                if colidir == False: colidir = self._colidir_atomo(atomos)
            self._desenho.up()
            self._desenho.setpos(x,y)
            self._desenho.down()
            self._desenho.setheading(270)
            self._desenho.left(randint(60, 115))
            
    def _colidir_atomo(self, atomos):
        colidir = False
        for a in atomos:
            distancia_entre_particulas = sqrt(pow(self._desenho.xcor()-a._desenho.xcor(),2) + pow(self._desenho.ycor()-a._desenho.ycor(),2))
            if distancia_entre_particulas <= 10:
                xa, ya = a._desenho.position()
                xp, yp = self._desenho.position()
                vz = (xa-xp, ya-yp)
                vd = self.vetor_deslocamento()
                cos_fi = (vz[0]*vd[0] + vz[1]*vd[1])/ \
                         (sqrt(vz[0]**2 + vz[1]**2)* sqrt(vd[0]**2 + vd[1]**2))
                
                angulo_incidencia = acos(cos_fi)*180/pi 
                self._desenho.left(180-2*angulo_incidencia)
                print(angulo_incidencia)

                
                
                break
            
        if colidir == True: return True
        else: return False
        
class Atomo_Ouro(object):
    def __init__(self, nome, cor, tamanho_nucleo):
        self._nome = nome
        self._cor = cor
        self._tamanho_nucleo = tamanho_nucleo
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.color(cor)
        self._desenho.shapesize(tamanho_nucleo,tamanho_nucleo)
        self._desenho.shape('circle')
        
    def __str__(self): return self._nome
    def __repr__(self): return self._nome
    def _clonar(self): return Atomo_Ouro(self._nome, self._cor, self._tamanho_nucleo)
    
class Placa_Ouro(object):
    def __init__(self, componente, quantidade):
        self._atomos = []
        for i in range(quantidade):
            self._atomos.append(componente._clonar())

class Material_Radioativo(object):
    def __init__(self, nome, cor):
        self._nome = nome
        self._cor = cor
        self._desenho = Turtle()
        self._desenho.color(cor)
        self._desenho.shapesize(7,6)
        self._desenho.shape('circle')
    
def main():
    tela.setup(1000, 600)
    tela.tracer(2)
    
    alfa = Particula_Alfa()
    alfa._desenho.up()
    alfa._desenho.setpos(-200, 0)
    
    polonio = Material_Radioativo('Polônio', 'orangered')
    polonio._desenho.up()
    polonio._desenho.setpos(-200, 0)
    
    ouro = Atomo_Ouro('Ouro', 'gold', 0.8)    
    liga_ouro = Placa_Ouro(ouro, 19)
    ouro._desenho.hideturtle()
    
    x, y, pos = 200, 200, 0
    for atomos in liga_ouro._atomos:
        atomos._desenho.up()
        if (pos >= 0) and (pos <= 5):
            atomos._desenho.setpos(x,y)
            y -= 75

        elif (pos >= 6) and (pos <= 12):
            if pos == 6: x, y = 250, (200 + 75//2)
            atomos._desenho.setpos(x,y)
            y -= 75

        else:
            if pos == 13: x, y = 300, 200
            atomos._desenho.setpos(x,y)
            y -= 75
        pos += 1

        x2, y2 = atomos._desenho.position()
        atomos._desenho.setpos(x2, y2-(75//2))
        atomos._desenho.down()
        atomos._desenho.circle(75//2)
        atomos._desenho.up()
        atomos._desenho.setpos(x2,y2)

    alfa.movimentar_particula(liga_ouro._atomos)
    
    def exibir_posicao(x, y): print('x = {}\ny = {}'.format(x, y))
    tela.onclick(exibir_posicao)
    
if __name__ == '__main__': main()
