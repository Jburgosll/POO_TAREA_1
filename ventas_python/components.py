from utilities import borrarPantalla, gotoxy,purple_color
import time
import datetime

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(purple_color+self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)          
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor
    def solo_numeros2(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)          
            valor = input()
            try:
                if int(valor) >= 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor


    def solo_letras_enter(self,client_anterior,mensajeError,col,fil): 
        while True:
            gotoxy(col,fil)
            new_name = str(input()).lower().capitalize()
            if new_name.isalpha():
                break
            elif new_name=="":
                new_name=client_anterior
                break
            else:
                gotoxy(col,fil);print(" {}".format(mensajeError))
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return new_name

    def solo_letras(self,mensajeError,col,fil): 
        while True:
            gotoxy(col,fil)
            valor = str(input())
            if valor.isalpha():
                break
            else:
                gotoxy(col,fil);print(" {}".format(mensajeError))
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def solo_decimales(self,mensajeError,col,fil):
        while True:
            gotoxy(col,fil)
            valor = input()
            try:
                valor = float(valor)
                if valor >= float(0):
                    break
            except:
                gotoxy(col,fil);print(" {}".format(mensajeError))
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
        return valor
    
    def ecuadorian_id_base_10(func):
        def wrapper(*args, **kwargs):
            mensajeError = "Cédula no válida o no está en base 10."
            while True:
                valor = func(*args, **kwargs)
                if valor.isdigit() and len(valor) == 10:
                    # Verificar si es cédula ecuatoriana
                    primer_digito = int(valor[0])
                    if primer_digito >= 0 and primer_digito <= 5:
                        return valor
                gotoxy(args[2], args[3])
                print(mensajeError)
                time.sleep(1)
                gotoxy(args[2], args[3])
                print(" " * 50)
        return wrapper



    @ecuadorian_id_base_10
    def cedula(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)          
            valor = input()
            if len(valor) ==10 and valor.isdigit():
                break
            else:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
        return valor
        

   