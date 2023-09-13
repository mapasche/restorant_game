import parametros as pr 

class BaseDatos:

    def cargar_datos(self):

        with open(pr.PATH_DATOS, "rt", encoding = "UTf-8") as archivo:
            lineas = list(map(lambda x : x.strip().split(","), archivo.readlines()))
        
        dinero = int(lineas[0][0])
        reputacion = int(lineas[0][1])
        rondas = int(lineas[0][2])
        lista_platos_servidos = list(map(lambda x: int(x), lineas[1]))
        return dinero, reputacion, rondas, lista_platos_servidos


    def cargar_labels(self):
        
        with open(pr.PATH_MAPA, "rt", encoding = "UTF-8") as archivo:
            lineas = list(map(lambda x : x.strip().split(","), archivo.readlines()))

        for linea in lineas:
            if linea[0] == "mesero":
                width = pr.WIDTH_MESERO
                height = pr.HEIGHT_MESERO
                path = pr.PATH_MESERO
            elif linea[0] == "mesa":
                width = pr.WIDTH_MESA
                height = pr.HEIGHT_MESA
                path = pr.PATH_MESA
            else:
                width = pr.WIDTH_CHEF
                height = pr.HEIGHT_CHEF
                path = pr.PATH_CHEF

            dic = {
                "label" : linea[0],
                "x" : int(linea[1]) + pr.X_RESTO,
                "y" : int(linea[2]) + pr.Y_RESTO,
                "width" : width,
                "height" : height,
                "path" : path,
            }

            yield dic


    def guardar_datos(self, dinero, reputacion, ronda, chefs):
        
        filas = list()
        filas.append(f"{dinero},{reputacion},{ronda}")
        linea_chefs = ""
        for indice, chef in enumerate(chefs):

            if indice + 1 == len(chefs):#si es el ultimo objeto de la lista
                linea_chefs += str(chef.platos_preparados)
            else: #todos los demas objetos
                linea_chefs += str(chef.platos_preparados)
                linea_chefs += ","

        filas.append(linea_chefs)

        with open(pr.PATH_DATOS, "wt", encoding = "UTF-8") as archivo:
            for fila in filas:
                archivo.write(fila + "\n")


    def guardar_mapa(self, mesero, mesas, chefs):
        filas = list()
        fila_mesero = f"mesero,{mesero.x - pr.X_RESTO},{mesero.y - pr.Y_RESTO}"
        filas.append(fila_mesero)
        for mesa in mesas:
            filas.append(f"mesa,{mesa.x - pr.X_RESTO},{mesa.y - pr.Y_RESTO}")
        for chef in chefs:
            filas.append(f"chef,{chef.x - pr.X_RESTO},{chef.y - pr.Y_RESTO}")
        
        with open(pr.PATH_MAPA, "wt", encoding = "UTF-8") as archivo:
            for fila in filas:
                archivo.write(fila + "\n")
   
       