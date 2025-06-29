import numpy as np

def house():
    """
    Cria a matriz de vértices para a casa em wireframe,
    incluindo:
    - chaminé na água do telhado próxima da lateral esquerda (oposta à janela),
    - porta na frente (x = 0),
    - janela na lateral direita (y = 0).
    """
    # ===== Casa =====
    house_points = np.array([
        [0, 0, 0], [0, -10, 0], [0, -10, 12], [0, -10.4, 11.5], [0, -5, 16],
        [0, 0, 12], [0, 0.5, 11.4], [0, 0, 12], [0, 0, 0], [-12, 0, 0],
        [-12, -5, 0], [-12, -10, 0], [0, -10, 0], [0, -10, 12], [-12, -10, 12],
        [-12, 0, 12], [0, 0, 12], [0, -10, 12], [0, -10.5, 11.4], [-12, -10.5, 11.4],
        [-12, -10, 12], [-12, -5, 16], [0, -5, 16], [0, 0.5, 11.4], [-12, 0.5, 11.4],
        [-12, 0, 12], [-12, -5, 16], [-12, -10, 12], [-12, -10, 0], [-12, -5, 0],
        [-12, 0, 0], [-12, 0, 12], [-12, 0, 0]
    ])

    # ===== Chaminé: água esquerda do telhado, próxima de y = -10 =====
    x_center = -8.5          # sobre a água do telhado
    y_center = -8.5          # perto da parede oposta à janela
    z_base = 12 + ((x_center + 12) / 6) * 4  # inclinação do telhado

    height = 4
    size_base = 0.5
    size_top = 0.7

    chimney_points = np.array([
        [x_center - size_base, y_center - size_base, z_base],
        [x_center + size_base, y_center - size_base, z_base],
        [x_center + size_base, y_center + size_base, z_base],
        [x_center - size_base, y_center + size_base, z_base],
        [x_center - size_base, y_center - size_base, z_base],

        [x_center - size_top, y_center - size_top, z_base + height],
        [x_center + size_top, y_center - size_top, z_base + height],
        [x_center + size_top, y_center + size_top, z_base + height],
        [x_center - size_top, y_center + size_top, z_base + height],
        [x_center - size_top, y_center - size_top, z_base + height],

        [x_center + size_base, y_center - size_base, z_base],
        [x_center + size_top, y_center - size_top, z_base + height],
        [x_center + size_base, y_center + size_base, z_base],
        [x_center + size_top, y_center + size_top, z_base + height]
    ])

    # ===== Porta (frente da casa, x = 0) =====
    door_x = 0
    door_y1, door_y2 = -7, -3
    door_z1, door_z2 = 0, 6

    door_points = np.array([
        [door_x, door_y1, door_z1],
        [door_x, door_y2, door_z1],
        [door_x, door_y2, door_z2],
        [door_x, door_y1, door_z2],
        [door_x, door_y1, door_z1]
    ])

    # ===== Janela (parede lateral direita, y = 0) =====
    win_y = 0
    win_x1, win_x2 = -10, -7
    win_z1, win_z2 = 5, 8

    window_points = np.array([
        [win_x1, win_y, win_z1],
        [win_x2, win_y, win_z1],
        [win_x2, win_y, win_z2],
        [win_x1, win_y, win_z2],
        [win_x1, win_y, win_z1]
    ])

    # ===== Combinar tudo =====
    all_points = np.vstack([house_points, chimney_points, door_points, window_points])
    all_hom = np.vstack([all_points.T, np.ones(all_points.shape[0])])

    return all_hom
