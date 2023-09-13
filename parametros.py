import os

PATH_POST_RONDA = "post_ronda.ui"
PATH_RONDA = "ronda.ui"
PATH_PRERONDA = "preronda.ui"
PATH_VENTANA_INICIAL = "ventana_inicial.ui"
PATH_DATOS = os.path.join("datos.csv")
PATH_MAPA = os.path.join("mapa.csv")
PATH_MESA = os.path.join("sprites", "mapa", "accesorios", "silla_mesa_roja.png")
PATH_MESERO = os.path.join("sprites", "mesero", "down_02.png")
PATH_CHEF = os.path.join("sprites", "chef", "meson_01.png")
PATH_CLIENTE = os.path.join("sprites", "clientes", "hamster", "hamster_05.png")


#origen referencia restoran
X_RESTO = 80
Y_RESTO = 170
LARGO_MAPA = 650
ANCHO_MAPA = 400

LARGO_MAINWINDOW = 800
ANCHO_MAINWINDOW = 600

#mesa
WIDTH_MESA = 30
HEIGHT_MESA = 40
COSTO_MESA = 100

#mesero
WIDTH_MESERO = 30
HEIGHT_MESERO = 40
VEL_MESERO = 9



#chef
WIDTH_CHEF = 80
HEIGHT_CHEF = 75
PLATOS_INTERMEDIO = 20 #por cambiar
PLATOS_EXPERTO = 20 #por cambiar
X_CHEF_TIENDA = 110
Y_CHEF_TIENDA = 130
COSTO_CHEF = 200

#Bocadillo
PRECIO_BOCADILLO = 10
WIDTH_BOCADILLO = 20
HEIGHT_BOCADILLO = 20


#clientes
LLEGADA_CLIENTES = 7
TIEMPO_ESPERA_MESA = 5
PROPINA = 5
TIEMPO_ESPERA_RELAJADO = 50
PROB_RELAJADO = 0.5
TIEMPO_ESPERA_APURADO = 25
PROB_APURADO = 1 - PROB_RELAJADO
WIDTH_CLIENTE = 30
HEIGHT_CLIENTE = 30
ENTRADA_RESTO_X = 255
ENTRADA_RESTO_Y = 535
VEL_CLIENTE = 3


#DCCafe
DINERO_INICIAL = 200
REPUTACION_INICIAL = 3
CHEFS_INICIALES = 1
MESAS_INICIALES = 2
CLIENTES_INICIALES = 8


#trampa
DINERO_TRAMPA = 100
REPUTACION_TRAMPA = 5