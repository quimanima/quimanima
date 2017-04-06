from turtle import Turtle
from math import sqrt, pow

caneta = Turtle()

lado_tri = 200

h_tri = sqrt(pow(lado_tri,2)-pow(lado_tri//2, 2))

lado_quad = h_tri//2

lado_hex = sqrt(pow(lado_quad//2, 2)+ pow(lado_quad//2, 2))

angulo = 360//3
for i in range(3):
    caneta.fd(lado_tri)
    caneta.left(angulo)

angulo = 360//4
for i in range(4):
    caneta.fd(lado_quad)
    caneta.left(angulo)

angulo = 360//5
for i in range(5):
    caneta.fd(lado_hex)
    caneta.left(angulo)
