class Company:
    next = 0  # Variable de clase(estatica) para almacenar el próximo ID disponible
    # meetodo constructor que s eejecuta cuando se instancia la clase
    def __init__(self, name="SuperMaxi", ruc="0943213456001"):
        # Incrementa el contador de ID para cada nueva instancia
        Company.next += 1
        # variables de instancias
        self.__id = Company.next  # Asigna el ID único a la instancia actual privada
        self.business_name = name  # Asigna el nombre de la empresa a la instancia actual
        self.ruc = ruc  # Asigna el RUC de la empresa a la instancia actual
        
    # metodo de usuraio que muestra la información de la empresa (ID, nombre y RUC)
    def show(self):
        print(f"Id:{self.__id} Empresa: {self.business_name} ruc:{self.ruc}")
        
    def getJson(self):
        return {"id":self.__id, "rasonsocial": self.business_name, "ruc":self.ruc}
    
    @staticmethod
    def get_business_name():
        return f"Empresa:Corporacion el Rosado ruc:0876543294001"
        

    
