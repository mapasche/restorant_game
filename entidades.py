from PyQt5.QtCore import pyqtSignal, QObject, QThread,QTimer
from entidades_2 import Chef, Mesa, Mesero, Bocadillo 
from os import path
import parametros as pr 
import time
import random
import math

class Cliente(QThread):

    def __init__(self, id, senal_crear_label, senal_act_pos, senal_eliminar_label):
        super().__init__()
        self.__id = id
        self.mesa = None
        self.__x = pr.ENTRADA_RESTO_X
        self.__y = pr.ENTRADA_RESTO_Y
        self.__frame = 10
        self.sprite = "hamster"
        self.width = pr.WIDTH_CLIENTE
        self.height = pr.HEIGHT_CLIENTE
        self.carpeta = "clientes"
        self.senal_crear_label = senal_crear_label
        self.senal_act_pos = senal_act_pos
        self.senal_eliminar_label = senal_eliminar_label
        self.tiempo_espera = self.obtener_tipo()
        self.sentado = False
        self._animo = "alegre"

    def __del__(self):
        self.senal_act_pos.emit({"label" : self.id, "delete" : True})
        self.senal_eliminar_label.emit()

    @property
    def id(self):
        return self.__id

    @property
    def frame(self):
        return self.__frame // 10
        

    @frame.setter
    def frame(self, value):
        if value > 39:
            self.__frame = 10
        else:
            self.__frame = value

    @property
    def animo(self):
        return self._animo
    
    @animo.setter
    def animo(self, value):
        if value == "alegre": #no se q pasa en este caso
            pass
        elif value == "enojado":
            for i in range(4):
                path_cliente = path.join("sprites", f"{self.carpeta}",    
                    f"{self.sprite}" ,f"{self.sprite}_{i + 18}.png")

                self.senal_act_pos.emit({
                    "label" : self.id, "x" : self.__x, "y" : self.__y, "width" : self.width,
                    "height": self.height, "path" : path_cliente
                })
                time.sleep(1)
                #arreglar detalle q se encoje imagen
                

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if self.__x > value:
            #se mueve hacia la izq
            base_frame = 6
        else:
            base_frame = 9
        self.frame = 1 + self.__frame
        self.__x = value

        if base_frame + self.frame < 10:
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_0{self.frame + base_frame}.png")
        else:
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_{self.frame + base_frame}.png")

        self.senal_act_pos.emit({
            "label" : self.id, "x" : self.__x, "y" : self.__y, "width" : self.width,
            "height": self.height, "path" : path_cliente
        })

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if self.__y > value:
            #se mueve hacia arriba de la pantalla (decreciendo el y)
            base_frame = 3
        else:
            base_frame = 0
        self.frame = 1 + self.__frame

        self.__y = value
        if self.frame + base_frame < 10:
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_0{self.frame + base_frame}.png")
        else:
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_0{self.frame + base_frame}.png")

        self.senal_act_pos.emit({
            "label" : self.id, "x" : self.__x, "y" : self.__y, "width" : self.width,
            "height": self.height, "path" : path_cliente
        })


    def obtener_tipo(self):
        prob = random.random()
        if prob < pr.PROB_RELAJADO: #sera relajado
            return pr.TIEMPO_ESPERA_RELAJADO
        else:
            return pr.TIEMPO_ESPERA_APURADO

    def comiendo(self): 
        comida = self.mesa.comida
        calidad_pedido = comida.calcular_calidad_pedido() #prob para propina
        prob = random.random()

        #se guarda el dinero en la mesa. Se podria implementar un lock
        propina = True  if prob < calidad_pedido else False

        for i in range(5):
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_{i + 13}.png")

            self.senal_act_pos.emit({
                "label" : self.id, "x" : self.__x, "y" : self.__y, "width" : self.width,
                "height": self.height, "path" : path_cliente
            })
            time.sleep(0.5)

        self.mesa.cliente_retirandose(True, propina)
        
    def sin_comer(self):
        self.mesa.cliente_retirandose(False)
        for i in range(5):
            path_cliente = path.join("sprites", f"{self.carpeta}",    
                f"{self.sprite}" ,f"{self.sprite}_{i + 26}.png")

            self.senal_act_pos.emit({
                "label" : self.id, "x" : self.__x, "y" : self.__y, "width" : self.width,
                "height": self.height, "path" : path_cliente
            })
            time.sleep(0.5)
        
    def salir_restoran(self):
        salida_x = pr.ENTRADA_RESTO_X
        salida_y = pr.ENTRADA_RESTO_Y

        while self.x < salida_x:
            self.x += pr.VEL_CLIENTE
            time.sleep(0.05)
        while self.x > salida_x:
            self.x -= pr.VEL_CLIENTE
            time.sleep(0.05)
        time.sleep(0.1)
        while self.y < salida_y:
            self.y += pr.VEL_CLIENTE
            time.sleep(0.05)
        time.sleep(0.1)
        del self

    def llega_restoran(self):
        dic_crear_label = {
            "label" : self.id, "x" : self.x, "y" : self.y, "width" : self.width,
            "height" : self.height, "path" : pr.PATH_CLIENTE,
        }
        self.senal_crear_label.emit(dic_crear_label)

    def caminar_hacia_mesa(self):
        self.mesa.tomada = True
        mesa_x = self.mesa.x
        mesa_y = self.mesa.y
        #subir hasta llegar a la altura de la mesa
        while self.y > mesa_y - 20:
            self.y -= pr.VEL_CLIENTE
            time.sleep(0.05)

        time.sleep(0.1)

        while self.x < mesa_x:
            self.x += pr.VEL_CLIENTE
            time.sleep(0.05)
        while self.x > mesa_x:
            self.x -= pr.VEL_CLIENTE
            time.sleep(0.05)
        self.y += 1
    
    def run(self):
        #mover personaje
        self.caminar_hacia_mesa()
        self.sentado = True
        tiempo_inicio = time.time()
        #esperar comida hasta la mitad del tiempo de espera
        while not self.mesa.comida and time.time() - tiempo_inicio < self.tiempo_espera // 2:
            time.sleep(1)
        if not self.mesa.comida:
            self.animo = "enojado"
            while not self.mesa.comida and time.time() - tiempo_inicio < self.tiempo_espera:
                time.sleep(0.5)
            if not self.mesa.comida:
                self.sin_comer()
            else:
                if self.mesa.comida == True:
                    self.mesa.cliente_retirandose(False)
                else:
                    self.comiendo()
        else:
            if self.mesa.comida == True:
                self.mesa.cliente_retirandose(False)
            else:
                self.comiendo()
        self.salir_restoran()
        

class DCCafe (QObject):

    senal_reputacion = pyqtSignal(int)
    senal_dinero = pyqtSignal(int)
    senal_cuenta_clientes = pyqtSignal(int, int)
    senal_ronda = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.__dinero = int()
        self.__puntos_reputacion = int()
        self.__ronda = int()
        self.disponibilidad = True
        self._ganancia_ronda = 0
        self.pagos = 0
        self.propinas = 0
        self.pedidos_exitosos = 0
        self.__pedidos_totales = 0
        self.clientes_ronda = 0
        self._clientes = []
        self._mesas = []
        self._chefs = []
        self.mesas_libres = []
        self.timer_mesas = QTimer()
        self.timer_mesas.setInterval(500)
        self.timer_mesas.timeout.connect(self.limpiar_mesas)


    @property 
    def ronda(self):
        return self.__ronda

    @ronda.setter
    def ronda(self, value):
        if value >= 0:
            self.__ronda = value
            self.senal_ronda.emit(value)


    @property
    def puntos_reputacion(self):
        return self.__puntos_reputacion

    @puntos_reputacion.setter
    def puntos_reputacion(self, value):
        if 5 >= value >= 0:
            self.__puntos_reputacion = value
            self.senal_reputacion.emit(value)

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, valor):
        if valor < 0:
            raise ValueError
        self.__dinero = valor
        self.senal_dinero.emit(valor)


    @property
    def pedidos_totales(self):
        return self.__pedidos_totales

    @pedidos_totales.setter
    def pedidos_totales(self, value):
        self.__pedidos_totales = value
        self.senal_cuenta_clientes.emit(value - self.pedidos_exitosos, self.pedidos_exitosos)


    def pasar_ronda(self):
        #revisar
        self.__ronda += 1

    def comenzar_ronda(self):
        self.calcular_clientes_ronda()
        self.ganancia_ronda = 0
        self.pagos = 0
        self.propinas = 0
        self.pedidos_exitosos = 0
        self.pedidos_totales = 0
        self.mesas_libres = list(self._mesas)

    def agregar_mesa(self, mesa):
        self._mesas.append(mesa)        

    def eliminar_mesa(self, mesa):
        self._mesas.remove(mesa)
        del mesa

    def agregar_cliente(self, cliente):
        self._clientes.append(cliente)

    def eliminar_cliente(self, cliente):
        self._clientes.remove(cliente)

    def agregar_chef(self, chef):
        self._chefs.append(chef)
    
    def eliminar_chef(self, chef):
        self._chefs.remove(chef)
        del chef

    def reiniciar_partida(self):
        self.dinero = pr.DINERO_INICIAL
        self.puntos_reputacion = pr.REPUTACION_INICIAL
        self.ronda = 1
        self.disponibilidad = True
        self._ganancia_ronda = 0
        self.pagos = 0
        self.propinas = 0
        self.pedidos_exitosos = 0
        self.pedidos_totales = 0
        self.clientes_ronda = pr.CLIENTES_INICIALES
        self.mesas_libres = []
                
        for mesa in self._mesas:
            del mesa
        self._mesas = []

        for cliente in self._clientes:
            del cliente
        self._clientes = []

        for chef in self._chefs:
            chef.delete()
        self._chefs = []

    def calcular_reputacion(self):
        try:
            floor = math.floor(4 * self.pedidos_exitosos / self.clientes_ronda - 2)
        except ZeroDivisionError as error:
            print("Error ", error)

        reputacion = max(0, min(5, self.__puntos_reputacion + floor))
        self.__puntos_reputacion = reputacion
        if reputacion == 0:
            self.disponibilidad = False

    def calcular_clientes_ronda(self):
        self.clientes_ronda = (5 * (1 + self.__ronda))

    def comenzar_limpiar_mesas(self, bool_comenzar):
        if bool_comenzar:
            self.timer_mesas.start()
        else:
            self.timer_mesas.stop()

    def limpiar_mesas(self):
        #pasa por las mesas del juego
        self.mesas_libres = []
        for mesa in self._mesas:
            if mesa.cliente_exitoso != None:
                if mesa.cliente_exitoso == True:
                    self.pagos += mesa.dinero
                    self.propinas += mesa.propina
                    self.pedidos_exitosos += 1
                    self.pedidos_totales += 1
                    self.ganancia_ronda = self.propinas + self.pagos
                    self.dinero += mesa.dinero + mesa.propina
                    mesa.dinero = 0
                    mesa.propina = 0
                    
                else:
                    self.pedidos_totales += 1

                self.eliminar_cliente(mesa.cliente)
                mesa.cliente = None
                mesa.cliente_exitoso = None

            if not mesa.tomada:

                self.mesas_libres.append(mesa)