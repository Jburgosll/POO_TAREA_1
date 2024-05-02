class Product:
    next = 0
    def __init__(self,id=0, descrip="Ninguno", preci=0, stock=0):
        # Método constructor para inicializar los atributos de la clase Cliente
        Product.next += 1
        # variables de instancias
        #self.__id = Product.next  # Asigna el ID único a la 
        self.__id = id  # Asigna el ID único a la 
        self.descrip = descrip
        self.preci = preci
        self.__stock = stock  # Atributo privado para almacenar el número de identificación del cliente
                    
    @property
    def stock(self):
        # Getter para obtener el valor del atributo privado __stock
        return self.__stock
    
    def __repr__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'Producto:{self.__id} {self.descrip} {self.preci} {self.stock}'  
    
    def __str__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'Producto:{self.__id} {self.descrip} {self.preci} {self.stock}'  
    
    def getJson(self):
        # Método especial para representar la clase Cliente como una cadena
        return {"id":self.__id,"descripcion":self.descrip,"precio":self.preci,"stock": self.stock}
      
    def show(self):
        # Método para imprimir los detalles del cliente en la consola
       
        print(f'{self.__id}  {self.descrip}           {self.preci}  {self.stock}')  
          
