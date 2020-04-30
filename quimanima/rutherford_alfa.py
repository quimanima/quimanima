# quimanima/rutherford_alfa.py

from turtle import Turtle, Screen
from random import randint
from math import sqrt, cos, sin, acos, pi

tela = Screen()

class ParticulaAlfa:
    def __init__(self):
        self._angulo = 0
        self._desenho = Turtle()
        self._desenho.color('red')
        self._desenho.shapesize(0.3, 0.3)
        self._desenho.shape('circle')
        self._desenho.speed('fastest')
        self._desenho.up()
        self._desenho.setpos(-200, 0)
    
    def movimentar_particula(self, atomosouro:list):
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
                self._desenho.fd(1)
                if colidir == False:
                    colidir = self._colidir_atomo(atomosouro)
                    
            self._desenho.up()
            self._desenho.setpos(x,y)
            self._desenho.down()
            self._angulo = randint(-30, 25)
            self._desenho.setheading(self._angulo)
            
    def _colidir_atomo(self, atomosouro:list):
        colidir = False
        for Au in atomosouro:
            #x_ouro e y_ouro: coordenadas x e y do objeto da ouro
            #x_particula e y_particula: coordenadas x e y da particula alfa
            x_ouro, y_ouro = Au.verificar_posicao()
            x_particula, y_particula = self._desenho.position()
            
            xcor = x_particula - x_ouro
            ycor = y_particula - y_ouro
            distancia_entre_particulas = sqrt(xcor**2 + ycor**2)
            
            if distancia_entre_particulas < 11:                

                xcol = x_ouro - x_particula
                ycol = y_ouro - y_particula

                hipotenusa = sqrt((xcol**2) + (ycol**2))
                cos_teta = xcol/hipotenusa
                ang_colisao_rad = acos(cos_teta)
                ang_colisao_grau = ang_colisao_rad*pi/180
                
                # vz: Vetor deslocamento do plano normal (N)
                # vd: Vetor deslocamento da particula alfa
                vz = (cos(ang_colisao_rad), sin(ang_colisao_rad))
                
                vd = self._verificar_vetor_deslocamento()
                
                cos_fi = (vz[0]*vd[0] + vz[1]*vd[1])/ \
                         (sqrt(vz[0]**2 + vz[1]**2) * sqrt(vd[0]**2 + vd[1]**2))

                ang_inc_rad = acos(cos_fi)
                ang_inc_grau = ang_inc_rad*180/pi

                self._desenho.up()
                self._desenho.setheading(180+self._angulo + ang_inc_grau*2)
                self._desenho.fd(2)

                x, y = self._desenho.position()
                
                x2 = x - x_ouro
                y2 = y - y_ouro 
                d_nova = sqrt(x2**2 + y2**2)
                if d_nova < 11:
                    self._desenho.setheading(180+self._angulo - ang_inc_grau*2)
                    self._desenho.setpos(x,y)
                    self._desenho.down()
                else:
                    self._desenho.setpos(x_particula,y_particula)
                    self._desenho.down()

                self._angulo = self._desenho.heading()
                self._retirar_do_nucleo(Au)
                break
            
        if colidir == True: return True
        else: return False
        
    def _retirar_do_nucleo(self, Au):
        xo, yo = Au.verificar_posicao()
        xp, yp = self._desenho.position()
        self._desenho.up()
        if xp > xo and yp > yo:
            self._desenho.setpos(xp+1, yp+1)
            
        elif xp < xo and yp > yo:
            self._desenho.setpos(xp-1, yp+1)
            
        elif xp < xo and yp < yo:
            self._desenho.setpos(xp-1, yp-1)
            
        elif xp > xo and yp < yo:
            self._desenho.setpos(xp+1, yp-1)
            
        elif xp < xo and yp == yo:
            self._desenho.setpos(xp-1, yp)
            
        elif xp > xo and yp == yo:
            self._desenho.setpos(xp+1, yp)
            
        elif xp == xo and yp > yo:
            self._desenho.setpos(xp, yp+1)
            
        elif xp == xo and yp < yo:
            self._desenho.setpos(xp, yp-1)

        self._desenho.down()

    def _verificar_vetor_deslocamento(self):
        ang = self._angulo
        ang_rad = (pi*ang)/180
        return (cos(ang_rad), sin(ang_rad))
    

class ElementoOuro:
    def __init__(self):
        self._nome = 'Ouro'
        self._desenho = Turtle()
        self._desenho.speed('fastest')
        self._desenho.color('gold')
        self._desenho.shapesize(0.8, 0.8)
        self._desenho.shape('circle')
        self._desenho.hideturtle()
               
    def __str__(self):
        return self._nome
    
    def __repr__(self):
        return self._nome
    
    def clonar(self):
        return ElementoOuro()

    def subir(self):
        self._desenho.up()

    def descer(self):
        self._desenho.down()

    def aparecer(self):
        self._desenho.showturtle()

    def verificar_posicao(self):
        return self._desenho.position()

    def mudar_posicao(self, x:float=0, y:float=0):
        self._desenho.setpos(x, y)

    def desenhar_circulo(self, raio:float=50):
        self._desenho.circle(raio)
    

class PlacaOuro:
    def __init__(self, elemento_componente, quantidade:int):
        self._componentes = []
        self._elemento_componente = elemento_componente
        self._quantidade = quantidade
        for i in range(self._quantidade):
            self._componentes.append(self._elemento_componente.clonar())

    @property
    def componentes(self):
        return self._componentes

    def posicionar_atomos_ouro(self):
        x, y, pos = 200, 200, 0
        for Au in self._componentes:
            Au.aparecer()
            Au.subir()
            if (pos >= 0) and (pos <= 5):
                Au.mudar_posicao(x,y)
                y -= 75

            elif (pos >= 6) and (pos <= 12):
                if pos == 6: x, y = 250, (200 + 75//2)
                Au.mudar_posicao(x,y)
                y -= 75

            else:
                if pos == 13: x, y = 300, 200
                Au.mudar_posicao(x,y)
                y -= 75
            pos += 1

            x2, y2 = Au.verificar_posicao()
            Au.mudar_posicao(x2, y2-(75//2))
            Au.descer()
            Au.desenhar_circulo(75//2)
            Au.subir()
            Au.mudar_posicao(x2,y2)
            

class MaterialRadioativo:
    def __init__(self):
        self._nome = 'Polônio'
        
        self._desenho = Turtle()
        self._desenho.color('orangered')
        self._desenho.shapesize(7, 6)
        self._desenho.shape('circle')            
        self._desenho.up()
        self._desenho.setpos(-200, 0)
    

def main():
    try:
        tela.setup(1000, 600)
        tela.tracer(10)
        tela.title('Rutherford - Partículas Alfa')
        
        alfa = ParticulaAlfa()
        
        polonio = MaterialRadioativo()
        
        ouro = ElementoOuro()
        
        liga_ouro = PlacaOuro(ouro, 19)
        liga_ouro.posicionar_atomos_ouro()
        
        alfa.movimentar_particula(liga_ouro.componentes)
    except: pass
if __name__ == '__main__':
    main()
