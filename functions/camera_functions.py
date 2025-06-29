import numpy as np

import functions.move_functions as mvfn

# Função para criar câmera
def create_default_camera():
  point =np.array([[0],[0],[0],[1]])

  e1 = np.array([[1],[0],[0],[0]]) # X
  e2 = np.array([[0],[1],[0],[0]]) # Y
  e3 = np.array([[0],[0],[1],[0]]) # Z
  base = np.hstack((e1,e2,e3))

  camera = np.hstack((base,point))
  
  return camera


# Função para fazer ajuste inicial da câmera
def adjust_camera(cam):
  cam = mvfn.WorldMove.apply_rotate_x(cam, -90)
  cam = mvfn.WorldMove.apply_rotate_z(cam,90)
  cam = mvfn.WorldMove.apply_translate(cam,30, -5, 8)
  return cam

# Geração da matriz de parâmetros intrínsecos
def generate_intrinsic_matrix(f, w_p, h_p, w_mm, h_mm, s_theta=0):
    
    sx = w_p/w_mm
    sy = h_p/h_mm
    ox = w_p/2
    oy = h_p/2
    
    K = np.array([[f*sx, f*s_theta, ox],[0, f*sy, oy], [0,0,1]])
    
    return K