from PyQt5.QtCore import pyqtSignal, QObject, QThread, QTimer
from PyQt5.QtWidgets import QLabel
import entidades as ent
import entidades_2 as ent_2
import parametros as pr 
import base_datos as bd
import time

class AI(QThread):

    senal_crear_label = pyqtSignal(dict) #base datos
    senal_act_pos = pyqtSignal(dict)
    senal_preronda = pyqtSignal()
    senal_fin_preronda = pyqtSignal()
    senal_clientes_proximos = pyqtSignal(int)
    senal_limpiar_mesas = pyqtSignal(bool)
    senal_eliminar_label = pyqtSignal()
    senal_post_ronda = pyqtSignal(dict)
    senal_crear_label_random = pyqtSignal(str)
    senal_fin_postronda = pyqtSignal()
     

    def __init__(self):
        super().__init__()
        self.base_datos = bd.BaseDatos()
        self.mesero = None
        self.dccafe = None
        
        self.contador_creaciones_chefs = 0
        self.contador_creaciones_mesas = 0
        self.__tipo_ronda = 0    # preronda a 1, ronda 2 y postronda 3
        self._clientes_proximos = 0
        self.mesas_libres = list()
        

    @property 
    def tipo_ronda(self):
        return self.__tipo_ronda

    @tipo_ronda.setter
    def tipo_ronda(self, value):
        if value > 3:
            self.__tipo_ronda = 1
        else:
            self.__tipo_ronda = value

    @property
    def clientes_proximos(self):
        return self._clientes_proximos

    @clientes_proximos.setter
    def clientes_proximos(self, value):
        self._clientes_proximos = value
        self.senal_clientes_proximos.emit(value)
        

    def iniciar_partida(self, tipo):
        
        if tipo == "continuar":

            dinero, reputacion, rondas, platos_servidos = self.base_datos.cargar_datos()
            self.dccafe.dinero = dinero
            self.dccafe.puntos_reputacion = reputacion
            self.dccafe.ronda = rondas + 1
            try:
                for dic in self.base_datos.cargar_labels():
                
                    if dic["label"] == "mesero":
                        self.senal_crear_label.emit(dic)
                        self.mesero.x = dic["x"]
                        self.mesero.y = dic["y"]
                    elif dic["label"] == "mesa":
                        self.crear_mesa(dic)
                    elif dic["label"] == "chef":
                        dic["platos_servidos"] = platos_servidos[self.contador_creaciones_chefs]
                        self.crear_chef(dic)

            except KeyError as error:
                print("Error: ", error)

            self.tipo_ronda = 1

        else: #reiniciar
            self.reiniciar_partida()
            self.tipo_ronda = 2

        self.start()
        
    def crear_mesa(self, dic):
        identidad = f"mesa_{self.contador_creaciones_mesas}"
        self.contador_creaciones_mesas += 1
        dic["label"] = identidad
        self.senal_crear_label.emit(dic)
        mesa = ent_2.Mesa(identidad, dic["x"], dic["y"], self.senal_act_pos, self.senal_crear_label)
        self.dccafe.agregar_mesa(mesa)

    def crear_chef(self, dic):
        identidad = f"chef_{self.contador_creaciones_chefs}"
        self.contador_creaciones_chefs += 1
        dic["label"] = identidad
        self.senal_crear_label.emit(dic)
        chef = ent_2.Chef(identidad, dic["x"], dic["y"], self.senal_act_pos, dic["platos_servidos"])
        self.dccafe.agregar_chef(chef)

    def crear_mesero(self, dic):
        dic["label"] = "mesero"
        self.senal_crear_label.emit(dic)
        self.mesero.x = dic["x"]
        self.mesero.y = dic["y"]

    def confirmar_choque_mesero(self, dic_labels, dic_mesero):
        label_m = dic_labels["mesero"]
        pos_inicial_x = label_m.x()
        pos_inicial_y = label_m.y()
        label_m.move(dic_mesero["x"], dic_mesero["y"])
        labels_totales = dic_labels.values()
        labels_no_nulas = list(filter(lambda x: x != None, labels_totales))
        labels_choc = list(filter(
            lambda x: label_m.geometry().intersects(x.geometry()), labels_no_nulas))
        
        if len(labels_choc) > 1:
            for label in labels_choc:
                if label != label_m:
                    #mesero choco
                    self.mesero.chocando = True
                    self.mesero._x = pos_inicial_x
                    self.mesero._y = pos_inicial_y
                    dic_mesero["x"] = pos_inicial_x
                    dic_mesero["y"] = pos_inicial_y
                    
                    if self.tipo_ronda == 2:
                        nombre_label = list(filter(
                            lambda x: label == dic_labels[x], dic_labels.keys()))
                        #chocar contra una mesa y tener comida
                        if "mesa" in nombre_label[0] and self.mesero.obj_comida:

                            mesa_objeto = list(filter(lambda x: x.id == nombre_label[0],
                                self.dccafe._mesas))

                            if mesa_objeto[0].tomada and not mesa_objeto[0].comida: 
                                #la mesa tiene a un cliente y no tiene comida
                                mesa_objeto[0].comida = self.mesero.obj_comida
                                self.mesero.obj_comida = None

                        elif "chef" in nombre_label[0]:#choco al chef
                            chef_obj = list(filter(lambda x: x.id == nombre_label[0],
                                self.dccafe._chefs)) 

                            if not self.mesero.obj_comida:

                                if chef_obj[0].plato_meson:

                                    self.mesero.obj_comida = chef_obj[0].entregar_plato_meson()

                                elif not chef_obj[0].isRunning():
                                    chef_obj[0].start()
                            else:
                                if not chef_obj[0].plato_meson and not chef_obj[0].isRunning():
                                    chef_obj[0].start()
                            
        else:
            self.mesero.chocando = False

        self.senal_act_pos.emit(dic_mesero)

    #ver si no hay superposicion de labels para hacer drop de mesa o chef
    def desconfirmar_superposicion_labels(self, dic_labels, dic_obj, label):

        labels = dic_labels.values()
        labels_choc = list(filter(lambda x: label.geometry().intersects(x.geometry()), labels))
        del label
        #no hay objetos debajo de este
        if not labels_choc:
            
            if dic_obj["label"] == "chef": #chef
                if self.dccafe.dinero >= pr.COSTO_CHEF: #se puede comprar el chef
                    self.dccafe.dinero -= pr.COSTO_CHEF
                    dic_obj["platos_servidos"] = 0
                    self.crear_chef(dic_obj)
                else:
                    print("Insuficiente saldo")
            elif dic_obj["label"] == "mesa": #mesa
                if self.dccafe.dinero >= pr.COSTO_MESA: #se puede comprar la mesa
                    self.dccafe.dinero -= pr.COSTO_MESA
                    self.crear_mesa(dic_obj)
                else:
                    print("Insuficiente saldo")

    def borrar_obj_clickeado(self, id_label):
        if self.tipo_ronda == 1:
            if "mesa" in id_label and len(self.dccafe._mesas) > 1:
                mesa_obj = list(filter(lambda x: x.id == id_label, self.dccafe._mesas))
                self.dccafe.eliminar_mesa(mesa_obj[0])

            elif "chef" in id_label and len(self.dccafe._chefs) > 1:
                chef_obj = list(filter(lambda x: x.id == id_label, self.dccafe._chefs))
                self.dccafe.eliminar_chef(chef_obj[0])

    def comenzar_ronda(self):
        if self.tipo_ronda == 1:
            self.tipo_ronda = 2
            self.senal_fin_preronda.emit()
        
            self.dccafe.comenzar_ronda()
        
            for chef in self.dccafe._chefs:
                chef.reputacion_local = self.dccafe.puntos_reputacion        
        
    def fin_ronda(self):
        if self.tipo_ronda == 2:
            self.tipo_ronda = 3
            for chef in self.dccafe._chefs:
                if chef.plato_meson is not None:
                    chef.plato_meson = None
            self.dccafe.calcular_reputacion()
        
    def guardar_partida(self):
        chefs = self.dccafe._chefs
        mesas = self.dccafe._mesas
        mesero = self.mesero
        self.base_datos.guardar_mapa(mesero, mesas, chefs)

        reputacion = self.dccafe.puntos_reputacion
        dinero = self.dccafe.dinero
        rondas_terminadas = self.dccafe.ronda
        self.base_datos.guardar_datos(dinero, reputacion, rondas_terminadas, chefs)

    def llegada_cliente(self): #funcion de qtimer
        #retorna el tiempo en q deberia llegar el siguiente cliente
        identidad = f"cliente_{self.clientes_proximos}"
        cliente = ent.Cliente(identidad, self.senal_crear_label, self.senal_act_pos,
            self.senal_eliminar_label)
        cliente.llega_restoran()
        self.clientes_proximos -= 1

        if len(self.dccafe.mesas_libres) > 0:
            mesa = self.dccafe.mesas_libres.pop()
            cliente.mesa = mesa
            mesa.cliente = cliente
            self.dccafe.agregar_cliente(cliente)
            cliente.start()      
            return int(pr.LLEGADA_CLIENTES)            

        else: #esperar a q desocupen las mesas
            time.sleep(5)

            if len(self.dccafe.mesas_libres) > 0:
                mesa = self.dccafe.mesas_libres.pop()
                cliente.mesa = mesa
                mesa.cliente = cliente
                self.dccafe.agregar_cliente(cliente)
                cliente.start()
            else:
                self.dccafe.pedidos_totales += 1
                del cliente

            return int(pr.LLEGADA_CLIENTES - 5)

    def fin_post_ronda(self):
        if self.dccafe.disponibilidad: #si el usuario aun no pierde
            self.tipo_ronda = 1
            self.dccafe.ronda += 1

        else: #el usuario perdio
            self.reiniciar_partida()
            self.tipo_ronda = 2
        
        self.senal_fin_postronda.emit()
        
    def reiniciar_partida(self):
        self.contador_creaciones_chefs = 0
        self.contador_creaciones_mesas = 0
        self.dccafe.reiniciar_partida()
        self.senal_eliminar_label.emit()
        for i in range(pr.MESAS_INICIALES):
            self.senal_crear_label_random.emit("mesa")
        for i in range(pr.CHEFS_INICIALES):
            self.senal_crear_label_random.emit("chef")
        self.senal_crear_label_random.emit("mesero")
        self.senal_eliminar_label.emit()

    def dinero_trampa(self):
        self.dccafe.dinero += pr.DINERO_TRAMPA

    def reputacion_trampa(self):
        self.dccafe.puntos_reputacion = pr.REPUTACION_TRAMPA

    def ronda_trampa(self):
        if self.__tipo_ronda == 2:
            self.clientes_proximos = 0
            for mesa in self.dccafe._mesas:
                mesa.comida = True

    def run(self):

        while True:
            if self.tipo_ronda == 1: #preronda
                self.senal_preronda.emit()

            elif self.tipo_ronda == 2: #ronda
                
                self.clientes_proximos = self.dccafe.clientes_ronda
                self.senal_limpiar_mesas.emit(True)
                time.sleep(1)
                while self.clientes_proximos > 0: #esperar a q se acaben los clientes
                    intervalo_llegada = self.llegada_cliente()
                    time.sleep(intervalo_llegada)

                while self.dccafe._clientes: #esperar q se vayan los clientes
                    time.sleep(1)

                for chef in self.dccafe._chefs:
                    if chef.isRunning():
                        chef.wait()

                self.senal_limpiar_mesas.emit(False)

                self.fin_ronda()

            elif self.tipo_ronda == 3: #post ronda
                self.senal_post_ronda.emit({
                    "perdidos" : self.dccafe.pedidos_totales - self.dccafe.pedidos_exitosos,
                    "atendidos" : self.dccafe.pedidos_exitosos,
                    "dinero" : self.dccafe.dinero,
                    "reputacion" : self.dccafe.puntos_reputacion,
                    "ronda" : self.dccafe.ronda,
                    "disponibilidad" : self.dccafe.disponibilidad,
                })
        

            time.sleep(1)

