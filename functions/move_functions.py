import numpy as np
from math import pi,cos,sin
import matplotlib.pyplot as plt

# Classe que delimita todas as movimentações padrão do objeto
class Move():
  def rotate_X(angulo):
    M = np.array([[1,0,0,0],[0,cos(angulo),-sin(angulo),0],[0,sin(angulo),cos(angulo),0],[0,0,0,1]])
    return M
  def rotate_Y(angulo):
    M = np.array([[cos(angulo),0,sin(angulo),0],[0,1,0,0],[-sin(angulo),0,cos(angulo),0],[0,0,0,1]])
    return M
  def rotate_Z(angulo):
    M = np.array([[cos(angulo),-sin(angulo),0,0],[sin(angulo),cos(angulo),0,0],[0,0,1,0],[0,0,0,1]])
    return M
  def translate(x,y,z):
    T = np.array([[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]])
    return T

# Função para transformar graus em radianos
def translate_degree_rad(angle):
  return angle*pi/180

# Classe com funções que aplicam movimentação em relação ao referencial do mundo
class WorldMove():
  def apply_rotate_x(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_X(ang)
    cam = R @ cam
    return cam

  def apply_rotate_y(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_Y(ang)
    cam = R @ cam
    return cam

  def apply_rotate_z(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_Z(ang)
    cam = R @ cam
    return cam

  def apply_translate(cam,x,y,z):
    T = Move.translate(x,y,z)
    cam = T @ cam
    return cam

# Classe com funções que aplicam movimentação em relação ao eixo da câmera

class CameraMove():
  def apply_rotate_x(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_X(ang)
    cam = cam @ R
    return cam

  def apply_rotate_y(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_Y(ang)
    # Apply rotation to the camera vector
    cam = R @ cam
    return cam

  def apply_rotate_z(cam,ang):
    ang = translate_degree_rad(ang)
    R = Move.rotate_Z(ang)
    # Apply rotation to the camera vector
    cam = R @ cam
    return cam

  def apply_translate(cam,x,y,z):
    T = Move.translate(x,y,z)
    cam = cam @ T
    return cam
