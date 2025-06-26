import numpy as np
from math import pi,cos,sin
import matplotlib.pyplot as plt

# Função para criar plot
def create_plot(ax=None, figure=None, lim=[-20, 20]):
  if figure is None:
      figure = plt.figure(figsize=(8, 8))
  if ax is None:
      ax = plt.axes(projection='3d')
  ax.set_title("Mundo")
  ax.set_xlim(lim)
  ax.set_ylim(lim)
  ax.set_zlim(lim)
  ax.set_xlabel("x axis")
  ax.set_ylabel("y axis")
  ax.set_zlabel("z axis")
  return ax

# Função para criar os eixos
def create_axes(origin, base, axis, length=1.5):
  axis.quiver(origin[0], origin[1], origin[2], base[0, 0], base[1, 0], base[2, 0], color='red', length=length)
  axis.quiver(origin[0], origin[1], origin[2], base[0, 1], base[1, 1], base[2, 1], color='green', length=length)
  axis.quiver(origin[0], origin[1], origin[2], base[0, 2], base[1, 2], base[2, 2], color='blue', length=length)
  return axis

# Função para renderizar arquivo que será exibido
def render_wireframe(ax, vertices):
  points_3d = vertices[:3, :]
  ax.plot(points_3d[0, :], points_3d[1, :], points_3d[2, :], color='blue')
  

# Função de projeção 2D 

def generate_projection_2d(K, cam, obj):
  
    # Obter as matrizes de transformação
    inv_camera = np.linalg.inv(cam) 
    P_can = np.eye(3, 4)

    # 1. Transformar todos os pontos para o espaço da câmera
    camera_space_coords = inv_camera @ obj

    # 2. Projetar para o plano de projeção
    projected_space = P_can @ camera_space_coords
    
    # 3. Aplicar intrínsecos para obter coordenadas de pixel (ainda com profundidade z)
    projected_2d_homogeneous = K @ projected_space

    # 4. Divisão de Perspectiva
    z = projected_2d_homogeneous[2, :]
    z[z == 0] = 1e-9 # Evita divisão por zero
    
    final_2d_points = projected_2d_homogeneous[:2, :] / z
    
    return final_2d_points



# Função para resetar o canvas
def refresh_canvas( ax1, ax2, pixel_width, pixel_height, object_wireframe, cam, canvas1, canvas2, intrinsic):
  plt.close('all')
  projected_points = generate_projection_2d(intrinsic, cam, object_wireframe)
  ax1.clear()
  ax1.set_xlim([0, pixel_width])
  ax1.set_ylim([pixel_height, 0])
  ax1.plot(projected_points[0, :], projected_points[1, :], color='blue')
  ax1.grid(True)
  ax1.set_aspect('equal')
  ax2.clear()
  ax2 = create_plot(ax=ax2, lim=[-15, 30])
  render_wireframe(ax2, object_wireframe)
  create_axes(cam[:, -1], cam[:, 0:3], ax2)
  canvas1.draw()
  canvas2.draw()
