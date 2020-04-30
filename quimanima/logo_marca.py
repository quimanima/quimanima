# quimanima/logo_marca.py

from turtle import Turtle, Screen
from random import choice

cores = ('blue',
         'aquamarine',
          'red',
          'yellow',
          'green',
          'orange',
          'purple',
          'pink',
          'gray',
          'white')

class LetraOrganica:
    def __init__(self, pontos):
        self._desenho = Turtle()
        self._desenho.hideturtle()
        self._desenho.pensize(2)
        self._pontos = pontos

    def desenhar_letra(self, pos:tuple=(0,0)):
        self._desenho.color(choice(cores))
        x, y = pos
        for coord in self._pontos:
            p_a, p_b = coord
            self._desenho.up()
            self._desenho.setpos(p_a[0]+x, p_a[1]+y)
            self._desenho.down()
            self._desenho.setpos(p_b[0]+x, p_b[1]+y)
        

def main():
    try:
        tela = Screen()
        tela.title('Quimanima')
        tela.bgcolor('black')
        tela.setup(1270, 500)
        quimanima = 'QUIMANIMA'
        quimanima_pos = ((-558,0),
                         (-390,0),
                         (-270,-32.5),
                         (-110, -65),
                         (25, -65),
                         (160, -65),
                         (260, -32.5),
                         (420,-65),
                         (560, -65))
        
        letras = {'Q': LetraOrganica((((0, 0), (0, 0)),
                                      ((0, 65), (56.29, 32.5)),
                                      ((56.29, 32.5), (56.29, -32.5)),
                                      ((56.29, -32.5), (0, -65)),
                                      ((0, -65), (-56.29, -32.5)),
                                      ((-56.29, -32.5), (-56.29, 32.5)),
                                      ((-56.29, 32.5), (0, 65)),
                                      ((0, 60), (51.29, 30.5)),
                                      ((51.29, -30.5), (0, -60)),
                                      ((-51.29, -32.5), (-51.29, 32.5)),
                                      ((56.29, -32.5), (56.29*2, -65)))),
                  'U': LetraOrganica((((0, 0), (0, 0)),
                                      ((-78, 46), (-78, -19)),
                                      ((-78, -19), (-32.5, -65)),
                                      ((-32.5, -65), (32.5, -65)),
                                      ((32.5, -65), (79, -19)),
                                      ((79, -19), (79, 46)),
                                      ((-74, -17), (-31.5, -60)),
                                      ((74, -17), (30.5, -60)))),
                  'I': LetraOrganica((((0, 0),(0, 65)),
                                      ((0, 0),(56.3, -32.5)),
                                      ((0, 0),(-56.3, -32.5)))),
                  'M': LetraOrganica((((0,0),(0,0)),
                                      ((-92, 0), (-46, 46)),
                                      ((-46, 46), (0, 0)),
                                      ((0, 0), (46, 46)),
                                      ((46, 46), (92, 0)),
                                      ((-86, 0), (-46, 40)),
                                      ((86, 0),(46, 40)))),
                  'A': LetraOrganica((((0, 0), (0, 0)),
                                      ((-32.5,0), (32.5,0)),
                                      ((32.5,0),(0, 56.3)),
                                      ((0, 56.3), (-32.5,0)),
                                      ((-25.5, 5), (25.5, 5)))),
                  'N': LetraOrganica((((0,0),(0,0)),
                                      ((-92, 0), (-46, 46)),
                                      ((-46, 46), (0, 0)),
                                      ((0, 0), (46, 46)),
                                      ((-86, 0), (-46, 40))))}

        for i in range(len(quimanima)):
            letras[quimanima[i]].desenhar_letra(quimanima_pos[i])
        tela.exitonclick()
    except: pass

if __name__ == '__main__':
    main()
