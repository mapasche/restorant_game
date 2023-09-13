import sys
from PyQt5.QtWidgets import QApplication
import front_end as fe
import parametros as pr
import entidades as ent
import entidades_2 as ent_2
import controladores as control


def hook(type, value, traceback):
    print(type)
    print(traceback)
    sys.__excepthook__ = hook 

app = QApplication([])


#instanciar clases
ventana_inicio = fe.VentanaInicio()
ventana_ronda = fe.RondaVentanaPrincipal()
ventana_tienda = fe.VentanaTienda(ventana_ronda.x(), ventana_ronda.y())
ventana_post_ronda = fe.VentanaPostRonda()
mesero = ent_2.Mesero(0)
ai = control.AI()
dccafe = ent.DCCafe()

#conecto una clase
ai.mesero = mesero
ai.dccafe = dccafe


#conectar señales
ai.senal_crear_label.connect(ventana_ronda.crear_label)
ai.senal_act_pos.connect(ventana_ronda.act_posicion)
ai.senal_preronda.connect(ventana_tienda.preronda)
ai.senal_fin_preronda.connect(ventana_tienda.fin_preronda)
ai.senal_clientes_proximos.connect(ventana_ronda.act_proximos)
ai.senal_limpiar_mesas.connect(dccafe.comenzar_limpiar_mesas)
ai.senal_eliminar_label.connect(ventana_ronda.quitar_labels_eliminadas)
ai.senal_post_ronda.connect(ventana_post_ronda.post_ronda)
ai.senal_crear_label_random.connect(ventana_ronda.create_label_random)
ai.senal_fin_postronda.connect(ventana_post_ronda.fin_post_ronda)

dccafe.senal_reputacion.connect(ventana_ronda.act_reputacion)
dccafe.senal_dinero.connect(ventana_ronda.act_dinero)
dccafe.senal_ronda.connect(ventana_ronda.act_ronda)
dccafe.senal_cuenta_clientes.connect(ventana_ronda.act_perdidos_atendidos)

mesero.senal_labels_choque.connect(ventana_ronda.labels_posible_choque_mesero)

ventana_inicio.senal_iniciar_partida.connect(ventana_ronda.iniciar_partida)
ventana_inicio.senal_iniciar_partida.connect(ai.iniciar_partida)

ventana_ronda.senal_confirmar_choque.connect(ai.confirmar_choque_mesero)
ventana_ronda.senal_act_pos_tienda.connect(ventana_tienda.act_pos)
ventana_ronda.senal_confirmar_drop.connect(ai.desconfirmar_superposicion_labels)
ventana_ronda.senal_comenzar_ronda.connect(ai.comenzar_ronda)
ventana_ronda.senal_mover_mesero.connect(mesero.mover)
ventana_ronda.senal_confirmar_borrar_obj.connect(ai.borrar_obj_clickeado)
ventana_ronda.senal_crear_mesa.connect(ai.crear_mesa)
ventana_ronda.senal_crear_chef.connect(ai.crear_chef)
ventana_ronda.senal_crear_mesero.connect(ai.crear_mesero)
ventana_ronda.senal_dinero_trampa.connect(ai.dinero_trampa)
ventana_ronda.senal_reputacion_trampa.connect(ai.reputacion_trampa)
ventana_ronda.senal_ronda_trampa.connect(ai.ronda_trampa)

ventana_post_ronda.senal_guardar_partida.connect(ai.guardar_partida)
ventana_post_ronda.senal_comenzar_ronda.connect(ai.fin_post_ronda)




ventana_inicio.show()
sys.exit(app.exec_())