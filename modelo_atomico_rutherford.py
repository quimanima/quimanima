# quimanima/modelo_atomico_rutherford.py

from turtle import Screen, Turtle
from math import sqrt, pi, cos, sin
from random import randint

tela = Screen()

class Proton:
    def __init__(self):
        self._carga = '+'
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.shape('circle')
        self._desenho.color('blue')        

    def mover_para(self, x:float, y:float):
        self._desenho.up()
        self._desenho.setpos(x, y)
        self._desenho.down()
        

class Neutron:
    def __init__(self):
        self._carga = '+-'
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.shape('circle')
        self._desenho.color('green')        
        
    def mover_para(self, x:float, y:float):
        self._desenho.up()
        self._desenho.setpos(x, y)
        self._desenho.down()


class Eletron:
    def __init__(self):
        self._carga = '-'
        self._angulo = None
        self._primeira_rotacao = True
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.shape('circle')
        self._desenho.color('gold')        
        self._desenho.shapesize(0.5, 0.5)
            
    def mover_na_eletrosfera(self, angulo_rotacao:float=0, raio_a:float=200, raio_b:float=60):
        if self._angulo == None:
            self._angulo = randint(0, 360)
            
        # ang: angulo (valor convertido em graus) do raio do elétron em relação ao eixo polar
        # ang_rot: angulo de rotação (valor convertido em graus) para rotacionar o elétron
        ang = pi*self._angulo/180
        ang_rot = pi*angulo_rotacao/180
        
        r = (raio_a * raio_b)/   \
            sqrt(raio_a**2*sin(ang)**2 + raio_b**2*cos(ang)**2)
        
        x = r*cos(ang)
        y = r*sin(ang)
        
        x1 = x*cos(ang_rot) - y*sin(ang_rot)
        y1 = x*sin(ang_rot) + y*cos(ang_rot)

        if self._angulo == 0 or self._primeira_rotacao == True:
            self._desenho.up()
            self._desenho.setpos(x1, y1)
            self._desenho.down()
            self._desenho.showturtle()
            self._primeira_rotacao = False
            
        self._angulo = (self._angulo+1) % 360
        self._desenho.setpos(x1, y1)

def main():
    try:
        tela.title('Modelo atômico de Rutherford')
        tela.tracer(2)
        
        proton1 = Proton()
        proton1.mover_para(5, 5)
        proton2 = Proton()
        proton2.mover_para(-5, -5)
        
        neutron1 = Neutron()
        neutron1.mover_para(-5, 5)
        neutron2 = Neutron()
        neutron2.mover_para(5, -5)
        
        eletron1 = Eletron()
        eletron2 = Eletron()
        eletron3 = Eletron()
        eletron4 = Eletron()
        
        while True:
            eletron1.mover_na_eletrosfera()
            eletron2.mover_na_eletrosfera(90)
            eletron3.mover_na_eletrosfera(45)
            eletron4.mover_na_eletrosfera(135)
    except: pass

if __name__ == '__main__':
    main()
