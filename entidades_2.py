from PyQt5.QtCore import pyqtSignal, QObject, QThread, QTimer
from os import path
import parametros as pr 
import time
import random
import math


class Mesa(QObject):

    def __init__(self, id, x, y, senal_act_pos, senal_crear_label):
        super().__init__()
        self.__id = id
        self.__x = x
        self.__y = y
        self.width = pr.WIDTH_MESA
        self.height = pr.HEIGHT_MESA
        self.tomada = False
        self._comida = None
        self.senal_act_pos = senal_act_pos
        self.senal_crear_label = senal_crear_label
        self.propina = 0
        self.dinero = 0
        self.cliente_exitoso = None
        self.cliente = None

    def __del__(self):
        self.senal_act_pos.emit({"label" : self.id, "delete" : True})

    @property
    def x(self):
        return self.__x

    @property 
    def y(self):
        return self.__y

    @property
    def id(self):
        return self.__id

    @property
    def comida(self):
        return self._comida

    @comida.setter
    def comida(self, value):
        if value is not None and type(value).__name__ != "bool":
            #mostrar imagen de bocadillo
            frame_boca = value.id // 10
            if frame_boca < 10:
                path_comida = path.join("sprites", "bocadillos",f"bocadillo_0{frame_boca}.png")
            else:
                path_comida = path.join("sprites", "bocadillos", f"bocadillo_{frame_boca}.png")
            
            nombre_label_comida = f"comida_{value.id}"
            self.senal_crear_label.emit({
                "label" : nombre_label_comida, "x" : self.x + 5, "y" : self.y + 10,
                "path" : path_comida, "width" : pr.WIDTH_BOCADILLO,
                "height" : pr.HEIGHT_BOCADILLO,
            })

        else:
            #quitar imagen
            try:
                nombre_label_comida = f"comida_{self._comida.id}"
            
                self.senal_act_pos.emit({
                "label" : nombre_label_comida, "delete" : True
                })

            except AttributeError as error:
                print("Error Mesa Comida: ", error)

        self._comida = value

    def cliente_retirandose(self, exitoso, propina = False):
        self.cliente_exitoso = exitoso
        if exitoso:
            if propina:
                self.propina = pr.PROPINA
            else:
                self.propina = 0
            self.comida = None
            self.dinero = pr.PRECIO_BOCADILLO
        self.tomada = False


class Mesero (QObject):

    #señales
    senal_labels_choque = pyqtSignal(dict)

    def __init__(self, identidad):
        super().__init__()
        self._x = int()
        self._y = int()
        self.__id = identidad
        self.__frame = 3
        self.width = pr.WIDTH_MESERO
        self.height = pr.HEIGHT_MESERO
        self.chocando = False
        self.obj_comida = None
        self.__carpeta = "mesero"

    @property
    def id(self):
        return self.__id

    @property
    def carpeta(self):
        return self.__carpeta

    @property
    def frame(self):
        return self.__frame // 3

    @frame.setter
    def frame(self, value):
        if not self.chocando:
            if value > 11:
                self.__frame = 3
            else:
                self.__frame = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        value = int(value)
        if pr.X_RESTO < value < pr.X_RESTO - self.width + pr.LARGO_MAPA:
            if self.obj_comida:
                if self._x > value:
                #se mueve hacia la izq
                    sprite = "left_snack"
                else:
                    sprite = "right_snack"

            else:
                if self._x > value:
                    #se mueve hacia la izq
                    sprite = "left"
                else:
                    sprite = "right"

            self._x = value
            path_mesero = path.join("sprites", f"{self.carpeta}", f"{sprite}_0{self.frame}.png")
            self.senal_labels_choque.emit({
                "label" : "mesero", "x" : value, "y" : self._y, "width" : self.width,
                "height": self.height, "path" : path_mesero,
            })
            
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        value = int(value)
        if pr.Y_RESTO + 45 < value < pr.Y_RESTO - self.width + pr.ANCHO_MAPA - 10:
            if self.obj_comida:
                if self._y > value:
                    #se mueve hacia arriba
                    sprite = "up_snack"
                else:
                    sprite = "down_snack"

            else:
                if self._y > value:
                #se mueve hacia arriba
                    sprite = "up"
                else:
                    sprite = "down"

            self._y = value
            path_mesero = path.join("sprites", f"{self.carpeta}", f"{sprite}_0{self.frame}.png")
            self.senal_labels_choque.emit({
                "label" : "mesero", "x" : self._x, "y" : value, "width" : self.width,
                "height": self.height, "path" : path_mesero,
            })
            

    def mover(self, lado): #asia donde se movera el mesero
        self.frame = self.__frame + 1
        #debe enviar señal a act_pos
        if lado == "izq":
            self.x -= pr.VEL_MESERO
        elif lado == "der":
            self.x += pr.VEL_MESERO
        elif lado == "sub":
            self.y -= pr.VEL_MESERO
        elif lado == "baj":
            self.y += pr.VEL_MESERO
        else:
            print("Error")


class Chef(QThread):

    def __init__(self, id, x, y, senal_act_pos, platos_preparados = 0):
        super().__init__()
        self.__id = id
        self.__x = x
        self.__y = y
        self.__platos_preparados = platos_preparados
        self.__frame = 1
        self.senal_act_pos = senal_act_pos
        self.experiencia = self.calcular_nivel_experiencia()
        self._plato_meson = None
        self.width = pr.WIDTH_CHEF
        self.height = pr.HEIGHT_CHEF
        self.reputacion_local = int()

    def delete(self):
        self.senal_act_pos.emit({"label" : self.id, "delete" : True})

    def __repr__(self):
        return str(self.__id)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def id(self):
        return self.__id

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if value > 17:
            self.__frame = 16
        else:
            self.__frame = value
        if self.__frame < 10:
            path_chef = path.join("sprites", "chef",f"meson_0{self.__frame}.png")
        else:
            path_chef = path.join("sprites", "chef", f"meson_{self.__frame}.png")

        
        self.senal_act_pos.emit({
            "label" : self.id, "x" : self.x, "y" : self.y, "width" : self.width,
            "height" : self.height, "path" : path_chef
        })

    @property
    def platos_preparados(self):
        return self.__platos_preparados

    @platos_preparados.setter
    def platos_preparados(self, valor):
        print(valor, self.id)
        if valor >= 0:
            self.__platos_preparados = valor
            self.experiencia = self.calcular_nivel_experiencia()

    @property
    def plato_meson(self):
        return self._plato_meson

    @plato_meson.setter
    def plato_meson(self, value):
        if value is not None:
            self.frame = 16
        else:
            self.frame = 1
        self._plato_meson = value


    def prob_fallar_plato(self):
        prob = 0.3 / (self.experiencia + 1)
        return prob

    def calcular_nivel_experiencia(self):
        if self.platos_preparados < pr.PLATOS_INTERMEDIO:
            return 1
        elif self.platos_preparados < pr.PLATOS_EXPERTO:
            return 2
        else:
            return 3

    def entregar_plato_meson(self):
        plato = self.plato_meson
        self.plato_meson = None
        self.platos_preparados += 1
        return plato


    def run(self):
        #crear alimento
        comida = Bocadillo(self.reputacion_local, self.experiencia)
        tiempo_prep = comida.tiempo_prep
        tiempo_inicio = time.time()

        while tiempo_prep > time.time() - tiempo_inicio:
            if (self.__frame * tiempo_prep) // 15 < time.time() - tiempo_inicio:
                self.frame = self.__frame + 1
            time.sleep(0.1)

        self.frame = self.__frame + 1

        prob_fallar = self.prob_fallar_plato()
        prob = random.random()

        if prob < prob_fallar:
            #fallo el plato
            self.plato_meson = None

        else:#esta bien el plato
            self.plato_meson = comida

        

class Bocadillo(QObject):

    def __init__(self, reputacion, nivel_chef):
        super().__init__()
        self.id = random.randint(1, 689) #el rango es para q sea unico el id, despues se hace //
        self.nivel_chef = int(nivel_chef)
        self.tiempo_prep = self.calcular_tiempo_prep(reputacion)
        self.tiempo_partida = time.time()

    def calcular_tiempo_prep(self, reputacion):
        tiempo = max(0, 15 - int(reputacion) - self.nivel_chef * 2)
        return tiempo

    def calcular_calidad_pedido(self):
        tiempo_espera = time.time() - self.tiempo_partida
        calidad = max(0, self.nivel_chef * (1 - tiempo_espera * 0.05) / 3)
        return calidad

