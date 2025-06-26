import numpy as np

def house():
    """
    Cria a matriz de vértices para a casa em wireframe,
    já em coordenadas homogêneas.
    """
    # Seus dados da casa
    house_points = np.array([
        [0, 0, 0], [0, -10, 0], [0, -10, 12], [0, -10.4, 11.5], [0, -5, 16],
        [0, 0, 12], [0, 0.5, 11.4], [0, 0, 12], [0, 0, 0], [-12, 0, 0],
        [-12, -5, 0], [-12, -10, 0], [0, -10, 0], [0, -10, 12], [-12, -10, 12],
        [-12, 0, 12], [0, 0, 12], [0, -10, 12], [0, -10.5, 11.4], [-12, -10.5, 11.4],
        [-12, -10, 12], [-12, -5, 16], [0, -5, 16], [0, 0.5, 11.4], [-12, 0.5, 11.4],
        [-12, 0, 12], [-12, -5, 16], [-12, -10, 12], [-12, -10, 0], [-12, -5, 0],
        [-12, 0, 0], [-12, 0, 12], [-12, 0, 0]
    ])

    # Transpor para (3, N)
    house_transposed = np.transpose(house_points)
    
    # Adicionar coordenada homogênea (w=1) para ter formato (4, N)
    house_homogeneous = np.vstack([house_transposed, np.ones(np.size(house_transposed, 1))])
    
    return house_homogeneous