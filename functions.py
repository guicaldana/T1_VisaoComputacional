import numpy as np
from math import pi,cos,sin
import matplotlib.pyplot as plt

# Classe que elimita todas as movimentações padrão do objeto

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

# Funções que aplicam movimentação em relação ao referencial do mundo

def apply_world_rotate_x(cam,ang):
  R = Move.rotate_X(ang)
  cam = R @ cam
  return cam

def apply_world_rotate_y(cam,ang):
  R = Move.rotate_Y(ang)
  cam = R @ cam
  return cam

def apply_world_rotate_z(cam,ang):
  R = Move.rotate_Z(ang)
  cam = R @ cam
  return cam

def apply_world_translate(cam,x,y,z):
  T = Move.translate(x,y,z)
  cam = T @ cam
  return cam

# Funções que aplicam movimentação em relação ao eixo da câmera

def apply_cam_rotate_x(cam,ang):
  R = Move.rotate_X(ang)
  cam = cam @ R
  return cam

def apply_cam_rotate_y(cam,ang):
  R = Move.rotate_Y(ang)
  cam = cam @ R
  return cam

def apply_cam_rotate_z(cam,ang):
  R = Move.rotate_Z(ang)
  cam = cam @ R
  return cam

def apply_cam_translate(cam,x,y,z):
  T = Move.translate(x,y,z)
  cam = cam @ T
  return cam

# Geração da matriz de parâmetros intrínsecos

def generate_intrinsic_matrix(f, w_p, h_p, w_mm, h_mm, s_theta=0):
    
    sx = w_p/w_mm
    sy = h_p/h_mm
    ox = w_p/2
    oy = h_p/2
    
    K = np.array([[f*sx, f*s_theta, ox],[0, f*sy, oy], [0,0,1]])
    
    return K

