from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtGui import QPixmap, QMoveEvent, QDrag
from PyQt5.QtCore import pyqtSignal, QMimeData, Qt, QRect
from os import path
import sys
import parametros as pr 
import random


window_ronda, clase_base = uic.loadUiType(pr.PATH_RONDA)
widget_vetana_inicial, clase_base_ventana_inicial = uic.loadUiType(pr.PATH_VENTANA_INICIAL)
widget_ventana_tienda, clase_base_tienda = uic.loadUiType(pr.PATH_PRERONDA)
widget_ventana_post_ronda, clase_post_ronda = uic.loadUiType(pr.PATH_POST_RONDA)


class RondaVentanaPrincipal(window_ronda, clase_base):
    
    senal_mover_mesero = pyqtSignal(str)
    senal_confirmar_choque = pyqtSignal(dict, dict)
    senal_act_pos_tienda = pyqtSignal(QMoveEvent)
    senal_confirmar_drop = pyqtSignal(dict, dict, QLabel)
    senal_comenzar_ronda = pyqtSignal()
    senal_confirmar_borrar_obj = pyqtSignal(str)
    senal_crear_mesa = pyqtSignal(dict)
    senal_crear_chef = pyqtSignal(dict)
    senal_crear_mesero = pyqtSignal(dict)
    senal_dinero_trampa = pyqtSignal()
    senal_reputacion_trampa = pyqtSignal()
    senal_ronda_trampa = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.labels = dict()
        self.setAcceptDrops(True)
        self.secuencia_teclas = ""

    #recibe la señal de preronda e inicia este window
    def iniciar_partida(self, tipo):
        self.show()

    #para mantener sincornizada el mov de la ventana tienda
    def moveEvent(self, event):
        super().moveEvent(event)
        #cambiar posicion de la otra widget
        self.senal_act_pos_tienda.emit(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        coord_rest = self.restoran.geometry().getCoords()
        if self.restoran.geometry().contains(event.pos()):
            tipo_obj = event.mimeData().text()
            #chef
            if tipo_obj == "chef":
                if (coord_rest[2] - pr.WIDTH_CHEF > event.pos().x() 
                    and coord_rest[3] - pr.HEIGHT_CHEF > event.pos().y() > coord_rest[1] + 60):

                    path = pr.PATH_CHEF
                    width = pr.WIDTH_CHEF
                    height = pr.HEIGHT_CHEF
                    label = "chef"
                else:
                    return

            elif tipo_obj == "mesa":
                if (coord_rest[2] - pr.WIDTH_MESA > event.pos().x() 
                    and coord_rest[3] - pr.HEIGHT_MESA > event.pos().y() > coord_rest[1] + 60):

                    path = pr.PATH_MESA
                    width = pr.WIDTH_MESA
                    height = pr.HEIGHT_MESA
                    label = "mesa"
                else:
                    return
            else:
                return

            dic = {
                "path" : path, "width" : width, "height" : height, "x" : event.pos().x(),
                "y" : event.pos().y(), "label" : label,
            }
            label_temporal = QLabel(self)
            label_temporal.setGeometry(dic["x"], dic["y"], width, height)

            self.senal_confirmar_drop.emit(self.labels, dic, label_temporal)
            
    def keyPressEvent(self, event):
        #mandar direccion del mesero
        tecla = event.text()
        if tecla == "a":
            self.senal_mover_mesero.emit("izq")
        elif tecla == "d":
            self.senal_mover_mesero.emit("der")
        elif tecla == "w":
            self.senal_mover_mesero.emit("sub")
        elif tecla == "s":
            self.senal_mover_mesero.emit("baj")
        elif tecla == "p":
            pass
        self.secuencia_teclas += tecla
        if len(self.secuencia_teclas) > 3:
            self.secuencia_teclas = self.secuencia_teclas[1:]

        if ("m" in self.secuencia_teclas and "o" in self.secuencia_teclas
            and "n" in self.secuencia_teclas):
            self.senal_dinero_trampa.emit()
            self.secuencia_teclas = ""
        elif ("f" in self.secuencia_teclas and "i" in self.secuencia_teclas
            and "n" in self.secuencia_teclas):
            self.senal_ronda_trampa.emit()
            self.secuencia_teclas = ""
        elif ("r" in self.secuencia_teclas and "t" in self.secuencia_teclas
            and "g" in self.secuencia_teclas):
            self.senal_reputacion_trampa.emit()
            self.secuencia_teclas = ""


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for nombre, label in self.labels.items():
                if label is not None:
                    if label.geometry().contains(event.pos()):
                        if "mesa" in nombre or "chef" in nombre:
                            #clickeo mesa
                            self.senal_confirmar_borrar_obj.emit(nombre)
        
        self.quitar_labels_eliminadas()          

    #recibe señales de los botones en pantalla
    def configuracion_juego(self, event):
        #abrir barra con parametros de todo el juego
        pass

    def comenzar_ronda(self, event):
        #se comienza la siguiente ronda cuando se pueda
        self.senal_comenzar_ronda.emit()

    def pausar_juego (self, event):
        #pausar el juego completo
        pass

    def salir_juego(self, event):
        #salir del juego actual sin guardar
        sys.exit()
        
    def act_reputacion(self, reputacion):
        self.barra_reputacion.setValue(reputacion)

    def act_dinero(self, dinero):
        self.label_dinero_usuario.setText(f"$ {dinero}")

    def act_ronda(self, ronda):
        self.label_ronda.setText(f"RONDA N°{ronda}")

    def act_proximos(self, proximos):
        self.label_proximos_usuarios.setText(f"{proximos}")

    def act_perdidos_atendidos(self, perdidos, atendidos):
        self.label_perdidos_usuario.setText(f"{perdidos}")
        self.label_atendidos_usuario.setText(f"{atendidos}")

    #recibe señal para q cree labels, objetos
    def crear_label(self, event):
        #se recibe un dict con un id de label, pos x, pos y, width, height y path
        label = QLabel(self)
        label.setGeometry(event["x"], event["y"], event["width"], event["height"])
        pixeles = QPixmap(event["path"])
        label.setPixmap(pixeles)
        label.setScaledContents(True)

        label.show()
        #añadimos el label al diccionario de labels
        self.labels[event["label"]] = label

    def labels_posible_choque_mesero(self, dic_mesero):
        self.senal_confirmar_choque.emit(self.labels, dic_mesero)
       
    #para actualizar posiscion de label (mesero) y tambein cambiar el frame
    def act_posicion(self, event):
        #recibe un dict con nombre_label, pos x e y , path/eliminar
        #width y height del frame
        try:
            label = self.labels[event["label"]]
            if event.get("path"):
                pixeles = QPixmap(event["path"])
                pixeles.scaled(event["width"], event["height"])
                label.setPixmap(pixeles)
                label.move(event["x"], event["y"])
                label.raise_()
            elif event.get("delete"):
                if label is not None:
                    label.setPixmap(QPixmap(None))
                    self.labels[event["label"]] = None
                    
        except KeyError as error:
            print(f"Error act pos: {error}")
            sys.exit()
        self.update()

    def quitar_labels_eliminadas(self):
        nombre_labels = []
        for nombre, label in self.labels.items():
            if label == None:
                nombre_labels.append(nombre)

        for nombre in nombre_labels:
            del self.labels[nombre]

    def create_label_random(self, tipo):
        self.quitar_labels_eliminadas()
        if self.labels.get("mesero"):
            self.labels["mesero"].setPixmap(QPixmap(None))
            del self.labels["mesero"]
        if tipo == "mesero":
            rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_MESERO - 10) + pr.X_RESTO
            rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_MESERO - 10) + pr.Y_RESTO
            label_temp = QLabel(self)
            label_temp.setGeometry(rand_x, rand_y, pr.WIDTH_MESERO, pr.HEIGHT_MESERO)
            labels = self.labels.values()
            labels_choc = list(filter(
                lambda x: label_temp.geometry().intersects(x.geometry()), labels))
            while labels_choc:
                rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_MESA - 10) + pr.X_RESTO
                rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_MESA - 10) + pr.Y_RESTO
                label_temp.move(rand_x, rand_y)
                labels_choc = list(filter(
                    lambda x: label_temp.geometry().intersects(x.geometry()), labels))

            del label_temp
            self.senal_crear_mesero.emit({"x" : rand_x, "y" : rand_y, "width" : pr.WIDTH_MESERO, 
                "height" : pr.HEIGHT_MESERO, "path" : pr.PATH_MESERO})

        elif tipo == "mesa":
            rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_MESA - 10) + pr.X_RESTO
            rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_MESA - 10) + pr.Y_RESTO
            label_temp = QLabel(self)
            label_temp.setGeometry(rand_x, rand_y, pr.WIDTH_MESA, pr.HEIGHT_MESA)
            labels = self.labels.values()
            labels_choc = list(filter(
                lambda x: label_temp.geometry().intersects(x.geometry()), labels))
            while labels_choc:
                rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_MESA - 10) + pr.X_RESTO
                rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_MESA - 10) + pr.Y_RESTO
                label_temp.move(rand_x, rand_y)
                labels_choc = list(filter(
                    lambda x: label_temp.geometry().intersects(x.geometry()), labels))

            del label_temp
            self.senal_crear_mesa.emit({"x" : rand_x, "y" : rand_y, "width" : pr.WIDTH_MESA, 
                "height" : pr.HEIGHT_MESA, "path" : pr.PATH_MESA})
         
        elif tipo == "chef":
            rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_CHEF - 10) + pr.X_RESTO
            rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_CHEF - 10) + pr.Y_RESTO
            label_temp = QLabel(self)
            label_temp.setGeometry(rand_x, rand_y, pr.WIDTH_CHEF, pr.HEIGHT_CHEF)
            labels = self.labels.values()
            labels_choc = list(filter(
                lambda x: label_temp.geometry().intersects(x.geometry()), labels))
            while labels_choc:
                rand_x = random.randint(10, pr.LARGO_MAPA - pr.WIDTH_CHEF - 10) + pr.X_RESTO
                rand_y = random.randint(60, pr.ANCHO_MAPA - pr.HEIGHT_CHEF - 10) + pr.Y_RESTO
                label_temp.move(rand_x, rand_y)
                labels_choc = list(filter(
                    lambda x: label_temp.geometry().intersects(x.geometry()), labels))

            del label_temp
            self.senal_crear_chef.emit({"x" : rand_x, "y" : rand_y, "width" : pr.WIDTH_CHEF, 
                "height" : pr.HEIGHT_CHEF, "path" : pr.PATH_CHEF, "platos_servidos" : 0})

class VentanaInicio(widget_vetana_inicial, clase_base_ventana_inicial):

    senal_iniciar_partida = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    #señales desde designer

    #boton seguir partida
    def seguir_partida(self):
        self.hide()
        self.senal_iniciar_partida.emit("continuar")

    #boton reiniciar juego
    def reiniciar_partida(self):
        self.hide()
        self.senal_iniciar_partida.emit("reiniciar")
        
class VentanaTienda(widget_ventana_tienda, clase_base_tienda):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.setupUi(self)
        self.move(pos_x + pr.LARGO_MAINWINDOW, pos_y + pr.ANCHO_MAINWINDOW // 10)

    def preronda(self):
        if not self.isVisible():
            self.show()

    def fin_preronda(self):
        if self.isVisible():
            self.hide()

    #hacer q window tenga la ubicacion sincronizada con el window principal
    def act_pos(self, event):
        diff = event.pos() - event.oldPos()
        geo = self.geometry()
        geo.moveTopLeft(geo.topLeft() + diff)
        self.setGeometry(geo)
        self.raise_()

    #hacer q las imagenes se puedan draggear
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.label_chef.geometry().contains(event.pos()):
                drag = QDrag(self)
                mimedata = QMimeData()
                
                mimedata.setText("chef")
                drag.setMimeData(mimedata)
                drag.setPixmap(self.label_chef.pixmap())
                drag.exec_()
        
            elif self.label_mesa.geometry().contains(event.pos()):
                drag = QDrag(self)
                mimedata = QMimeData()
                
                mimedata.setText("mesa")
                drag.setMimeData(mimedata)
                drag.setPixmap(self.label_mesa.pixmap())
                drag.exec_()

class VentanaPostRonda(widget_ventana_post_ronda, clase_post_ronda):

    senal_guardar_partida = pyqtSignal()
    senal_comenzar_ronda = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def post_ronda(self, dic_info):
        if not self.isVisible():
            self.show()
            self.label_clientes_perdidos.setText(str(dic_info["perdidos"]))
            self.label_clientes_atendidos.setText(str(dic_info["atendidos"]))
            self.label_dinero_acumulado.setText(str(dic_info["dinero"]))
            reputacion = str(dic_info["reputacion"])
            self.label_reputacion.setText(f"{reputacion}/5")
            ronda = str(dic_info["ronda"])
            self.label_resumen_ronda.setText(f"RESUMEN RONDA N°{ronda}")

            if dic_info["disponibilidad"]: #si sigue corriendo el local
                self.boton_continuar.setText("CONTINUAR")
                self.boton_guardar.show()
                self.label_status_usuario.setText("¡¡Felicitaciones usuario!! Buenas estadísticas")

            else:
                self.boton_guardar.hide()
                self.boton_continuar.setText("REINICIAR")
                self.label_status_usuario.setText("Ha perdido usuario. DCCafe cerrará su local")

                
    def fin_post_ronda(self):
        if self.isVisible():
            self.hide()

    def salir_juego(self, event):
        #salir del juego actual sin guardar
        sys.exit()

    def guardar_juego(self, event):
        self.senal_guardar_partida.emit()

    def continuar_juego(self, event):
        self.senal_comenzar_ronda.emit()
