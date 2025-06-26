import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import functions.plot_functions as pltfn
import functions.move_functions as mvfn
import functions.camera_functions as camfn
from wireframe import house


###### Crie suas funções de translação, rotação, criação de referenciais, plotagem de setas e qualquer outra função que precisar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #definindo as variaveis
        self.set_variables()
        #Ajustando a tela    
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()
        self.update_canvas()

    def set_variables(self):
        
        self.objeto_original = house()
        self.objeto = self.objeto_original
        self.cam_original = camfn.create_default_camera()
        self.cam = camfn.adjust_camera(self.cam_original)
        self.px_base = 1280  
        self.px_altura = 720 
        self.dist_foc = 35 
        self.stheta = 0 
        self.ox = self.px_base/2 
        self.oy = self.px_altura/2 
        self.ccd = [36,24]
        self.K = self.intrinsic()
        
    def setup_ui(self):
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2  = self.create_cam_widget("Ref camera")
        line_edit_widget3  = self.create_intrinsic_widget("params instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

          # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)
    
    # Função para gerar a matriz de parâmetros intrínsecos
    def intrinsic(self):
        self.K = camfn.generate_intrinsic_matrix(self.dist_foc, self.px_base, self.px_altura, self.ccd[0], self.ccd[1])
        return self.K
    
    

    def create_intrinsic_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.ax2 = pltfn.create_plot(ax=self.ax2, lim=[-15, 30])
        pltfn.render_wireframe(self.ax2, self.objeto)
        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    # Funções para atualização dos parâmetros intrínsecos
    def update_params_intrinsc(self, line_edits):
        px_base = line_edits[0].text()
        px_altura = line_edits[1].text()
        ccd_x = line_edits[2].text()
        ccd_y = line_edits[3].text()
        dist_focal = line_edits[4].text()
        s_theta = line_edits[5].text()
        if px_base:
            self.px_base = float(px_base)
        if px_altura:
            self.px_altura = float(px_altura)
        if ccd_x:
            self.ccd[0] = float(ccd_x)
        if ccd_y:
            self.ccd[1] = float(ccd_y)
        if dist_focal:
            self.dist_foc = float(dist_focal)
        if s_theta:
            self.stheta = float(s_theta)
        self.intrinsic()
        self.update_canvas()
        for line in line_edits:
            line.clear()
        return 
    
    # Funções para atualização dos parâmetros no referencial do mundo
    def update_world(self,line_edits):
        x = line_edits[0].text()
        x_ang = line_edits[1].text()
        y = line_edits[2].text()
        y_ang = line_edits[3].text()
        z = line_edits[4].text()
        z_ang = line_edits[5].text()
        dx, dy, dz = float(x or 0), float(y or 0), float(z or 0)
        if x_ang:
            self.cam = mvfn.WorldMove.apply_rotate_x(self.cam,float(x_ang))
        if y_ang:
            self.cam = mvfn.WorldMove.apply_rotate_y(self.cam,float(y_ang))
        if z_ang:
            self.cam = mvfn.WorldMove.apply_rotate_z(self.cam,float(z_ang))
        self.cam = mvfn.WorldMove.apply_translate(self.cam,dx, dy, dz)
        self.update_canvas()
        for field in line_edits:
            field.clear()
        return

    # Funções para atualização dos parâmetros no referencial da câmera
    def update_cam(self,line_edits):
        x = line_edits[0].text()
        x_ang = line_edits[1].text()
        y = line_edits[2].text()
        y_ang = line_edits[3].text()
        z = line_edits[4].text()
        z_ang = line_edits[5].text()
        dx, dy, dz = float(x or 0), float(y or 0), float(z or 0)
        if dx or dy or dz:
            self.cam = mvfn.CameraMove.apply_translate(self.cam, dx, dy, dz)
        if x_ang:
            self.cam = mvfn.CameraMove.apply_rotate_x(self.cam,float(x_ang))
        if y_ang:
            self.cam = mvfn.CameraMove.apply_rotate_y(self.cam,float(y_ang))
        if z_ang:
            self.cam = mvfn.CameraMove.apply_rotate_z(self.cam,float(z_ang))
        self.update_canvas()
        for field in line_edits:
            field.clear()
        return 
    
    def projection_2d(self):

        view_matrix = np.linalg.inv(self.cam)

        intrinsic_matrix = self.intrinsic()

        projected_points = pltfn.generate_projection_2d(
            intrinsic_matrix=intrinsic_matrix,
            view_matrix=view_matrix,
            world_points=self.object_vertices
        )
        
        return projected_points
    
    def generate_intrinsic_params_matrix(self):
        return 
    

    def update_canvas(self):
        pltfn.refresh_canvas(self.ax1, self.ax2, self.px_base, self.px_altura, self.objeto, self.cam, self.canvas1, self.canvas2, self.K)
        return 
    
    def reset_canvas(self):
        self.initialize_variables()
        self.update_canvas()
        return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())