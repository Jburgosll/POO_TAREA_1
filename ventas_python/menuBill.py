from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        while True:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"*"*90+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Cliente")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(3,4);print("Cedula: ")
            dni=validar.cedula("Error: dato invalido",23,4)
            json_file = JsonFile(path+'/archivos/clients.json')
            client = json_file.find("dni",dni)
            if client:
                gotoxy(35,6);print("Cliente ya existe")
                time.sleep(1)

            else: 
                break
        gotoxy(3,5);print("Nombre: ")
        first_name=validar.solo_letras("Error: Solo letras",23,5).lower().capitalize()
        gotoxy(3,6);print("Apellido:")
        last_name=validar.solo_letras("Error: Solo letras",23,6).lower().capitalize()
        gotoxy(2,7);print("El cliente es VIP? (S/N): ")
        tip_client=validar.solo_letras("Error solo letras ",30,7).upper()
        if tip_client=="S":
            tip=VipClient(first_name,last_name,dni)
            tip2=VipClient.getJson(tip)
        else:
            gotoxy(2,8);print("el cliente tiene descuento? (S/N): ")
            cards=validar.solo_letras("Error solo letras ",40,8).upper()
            if cards=="S": cards=True 
            else: cards=False
            tip=RegularClient(first_name,last_name,dni,cards)
            tip2=RegularClient.getJson(tip)
        gotoxy(15,9);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10);print("😊 cliente Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/clients.json')
            invoices = json_file.read()
            invoices.append(tip2)
            json_file = JsonFile(path+'/archivos/clients.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10);print("🤣 Ingreso de cliente Cancelada 🤣"+reset_color)    
            
    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(cyan_color+"█"*90)
        gotoxy(2,2);print("██"+" "*30+"ACTUALIZACIÓN DE CLIENTES"+" "*31+"██"+reset_color)
        json_file = JsonFile(path+'/archivos/clients.json')
        clients=json_file.read()
        gotoxy(7,3);print(cyan_color+"Ingrese el dni del cliente a actualizar: ")
        gotoxy(7,3);dni=validar.cedula("Error: Cedula incorrecta",50,3)
        client_update = json_file.find("dni",dni)
        # for client in clients:
        #     if client["dni"] == dni:
        #         client_update = client
        #         break 
        if client_update:
            gotoxy(30,4);print(f"CLIENTE")
            gotoxy(2,5);print(green_color+"*"*90+reset_color)
            for cli in client_update:
                if isinstance(cli["valor"],int):
                    gotoxy(2,6);print(purple_color+"CLIENTE VIP"+reset_color)
                    gotoxy(2,7);print(green_color+"█"*60+reset_color)
                    gotoxy(2,8);print(blue_color+"Cedula")
                    gotoxy(20,8);print("Nombre")
                    gotoxy(35,8);print("Apellido")
                    gotoxy(50,8);print("Valor"+reset_color)
                    gotoxy(2,9);print(green_color+"="*60+reset_color)
                    gotoxy(2,10);print(f"{cyan_color}{cli['dni']}")
                    gotoxy(20,10);print(f"{cli['nombre']}")
                    gotoxy(35,10);print(f"{cli['apellido']}")
                    gotoxy(50,10);print(f"{cli['valor']}{reset_color}")
                elif isinstance(cli["valor"],float):
                    gotoxy(2,6);print(purple_color+"CLIENTE REGULAR"+reset_color)
                    gotoxy(2,7);print(green_color+"█"*60+reset_color)
                    gotoxy(2,8);print(blue_color+"Cedula")
                    gotoxy(20,8);print("Nombre")
                    gotoxy(35,8);print("Apellido")
                    gotoxy(50,8);print("Valor"+reset_color)
                    gotoxy(2,9);print(green_color+"="*60+reset_color)
                    gotoxy(2,10);print(f"{cyan_color}{cli['dni']}")
                    gotoxy(20,10);print(f"{cli['nombre']}")
                    gotoxy(35,10);print(f"{cli['apellido']}")
                    gotoxy(50,10);print(f"{cli['valor']}{reset_color}")
                for client in clients:
                    if client["dni"] == dni:
                  # Suponiendo que print_cliente es una función para mostrar los detalles del cliente
                        new_name = validar.solo_letras_enter(client['nombre'],"Error: solo letras",20,11)
                        new_surname = validar.solo_letras_enter(client['apellido'],"Error: Solo letras",35,11)
                        while True:
                            if client['valor'] > 1:
                                new_valuer = validar.solo_numeros("Error: Solo numeros",50,11)
                                break
                            elif client['valor'] < 1:
                                new_valuer = validar.solo_decimales("Error: solo decimales",50,11)
                                break
                        gotoxy(60,11);update=input(red_color+"Desea guardar(s/n):"+reset_color)
                        if update.lower() == "s":
                            client['nombre'] = new_name
                            client['apellido'] = new_surname
                            client['valor'] = new_valuer  
                            json_file.save(clients)
                            gotoxy(15,12);print(cyan_color+"Cliente actualizado exitosamente. :3")
                        break    
        else:
            print("No se encontró ningún cliente con el dni proporcionado.")
            print(red_color+f"{"DNI".ljust(10)}   {"Nombre".ljust(9)}   {"Apellido".ljust(9)}   {"Valor".ljust(5)}"+reset_color)    
            f=0          
            for cli in clients:
                print(green_color + f"{str(cli['dni']).ljust(10)}   {str(cli['nombre']).ljust(9)}   {str(cli['apellido']).ljust(9)}   {str(cli['valor']).ljust(5)}")
                f+=1

        input("Presione Enter para continuar...")
           
    def delete(self):
        validar=Valida()
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminar cliente"+" "*36+"██")
        json_file = JsonFile(path+'/archivos/clients.json')
        invoices1 = json_file.read()
        print(purple_color+"Clientes"+reset_color)
        gotoxy(2,4);print(green_color+"Cedula")
        gotoxy(15,4);print("Nombre")
        gotoxy(25,4);print("Apellido")
        gotoxy(40,4);print("Valor"+reset_color)
        d=1
        for fac in invoices1:
            gotoxy(2,4+d);print(f"{blue_color}{fac['dni']} ")
            gotoxy(15,4+d);print(f"{fac['nombre']} ")
            gotoxy(25,4+d);print(f"{fac['apellido']} ")
            gotoxy(40,4+d);print(f"{fac['valor']}")
            d+=1
        gotoxy(2,4+d);print("Ingrese cedula del cliente a eliminar:")
        invoice=validar.cedula("Error: dato invalido ",45,4+d)
        if invoice.isdigit():
            invoices = json_file.delete("dni",invoice)
            print(invoices)
        else:
            print("No ingreso el id correspondiente.... intentelo mas tarde..."+reset_color)
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*33+"██")
        json_file = JsonFile(path+'/archivos/clients.json')
        gotoxy(2,2);invoices = json_file.read()
        gotoxy(2,3);print("Ingrese la cedula del cliente que desea consultar:")
        gotoxy(2,3);invoice= validar.cedula("Error: Solo numeros",66,3)
        if invoice.isdigit():
            json_file = JsonFile(path+'/archivos/clients.json')
            invoices = json_file.find("dni",invoice)
            gotoxy(30,4);print(f"Cliente")
            gotoxy(2,5);print(green_color+"*"*90+reset_color)
            for fac in invoices:
                if isinstance(fac["valor"],int):
                    gotoxy(2,6);print("Cliente vip")
                    gotoxy(2,7);print(green_color+"-"*60+reset_color)
                    gotoxy(2,8);print(blue_color+"Cedula")
                    gotoxy(20,8);print("Nombre")
                    gotoxy(35,8);print("Apellido")
                    gotoxy(50,8);print("Valor"+reset_color)
                    gotoxy(2,9);print(green_color+"-"*60+reset_color)
                    gotoxy(2,10);print(f"{blue_color}{fac['dni']}")
                    gotoxy(20,10);print(f"{fac['nombre']}")
                    gotoxy(35,10);print(f"{fac['apellido']}")
                    gotoxy(50,10);print(f"{fac['valor']}{reset_color}")
                elif isinstance(fac["valor"],float) or isinstance(fac["valor"],0):
                    gotoxy(2,6);print(purple_color+"cliente regular"+reset_color)
                    gotoxy(2,7);print(green_color+"-"*60+reset_color)
                    gotoxy(2,8);print(blue_color+"Cedula")
                    gotoxy(20,8);print("Nombre")
                    gotoxy(35,8);print("Apellido")
                    gotoxy(50,8);print("Valor"+reset_color)
                    gotoxy(2,9);print(green_color+"-"*60+reset_color)
                    gotoxy(2,10);print(f"{blue_color}{fac['dni']}")
                    gotoxy(20,10);print(f"{fac['nombre']}")
                    gotoxy(35,10);print(f"{fac['apellido']}")
                    gotoxy(50,10);print(f"{fac['valor']}{reset_color}")
            x=input("presione una tecla para regresar...")    
        else:    
            print("Usted no ingreso dingun valor asi que sera redirigido al menu\nregresando.....") 

class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        while True:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"*"*90+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Cliente")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(3,4);print("Producto: ")
            new_produc=validar.solo_letras("Error: Solo numeros",23,4).lower().capitalize()
            json_file = JsonFile(path+'/archivos/products.json')
            produ = json_file.find("descripcion",new_produc)
            if produ:
                gotoxy(35,6);print("Producto ya existe")
                time.sleep(1)

            else: 
                break
        gotoxy(3,5);print("Precio: ")
        precio=validar.solo_decimales("Error: Solo decimales",23,5)
        gotoxy(3,6);print("Stock: ")
        stock=validar.solo_numeros("Error: Solo numeros ",23,6)
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        if products:
            last_id = max(product["id"] for product in products)
            new_id = last_id + 1
        else:
            new_id = 1
        product=Product(new_id,new_produc,precio,stock)
        product=Product.getJson(product)
        gotoxy(15,9);print(red_color+"Esta seguro de grabar este producto(s/n):")
        gotoxy(59,9);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10);print("😊 Produco Grabado satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            products.append(product)
            json_file = JsonFile(path+'/archivos/products.json')
            json_file.save(products)
        else:
            gotoxy(20,10);print("🤣 Ingreso de producto Cancelada 🤣"+reset_color)    
    
    def update(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualización de Producto"+" "*27+"██")
        validar= Valida()

        gotoxy(7,4); print("Ingrese el ID del producto que desea actualizar: ")
        product_id = validar.solo_numeros("Por favor, ingrese un número válido.",60,4)
        
        #product_id = int(input("Ingrese el ID del producto que desea actualizar: "))
        
        # Buscar el producto en el archivo JSON de productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        product_to_update = json_file.find("id",int(product_id))
        
        if product_to_update:
            for produc in product_to_update:
    # Verificar que las claves existan antes de acceder a ellas
                if "descripcion" in produc:
                    gotoxy(7,5);print("Nombre:", produc["descripcion"])
                if "precio" in produc:
                    gotoxy(7,6);print("Precio:", produc["precio"])
                if "stock" in produc:
                    gotoxy(7,7);print("Stock:", produc["stock"])
                
                for pro in products:
        
        # Solicitar la nueva información del producto
                    gotoxy(7,8); print("Ingrese el nuevo nombre del producto (deje vacío si no desea actualizar): ")
                    nuevo_nombre=validar.solo_letras_enter(pro["descripcion"],"Erro: solo letras",80,8)

                    gotoxy(7,9); print("Ingrese el nuevo precio del producto (deje vacío si no desea actualizar): ")
                    while True:
                        gotoxy(80,9);nuevo_precio=input()
                        if not nuevo_precio:
                            nuevo_precio=pro['precio']
                            break
                        elif float(nuevo_precio) >= float(0):
                            nuevo_precio=float(nuevo_precio)
                            break
                        else:
                            gotoxy(80,9);print("Error: solo numeros")
                            time.sleep(1)
                            gotoxy(80,9);print(" "*20)


                    gotoxy(7,10); print("Ingrese el nuevo stock del producto (deje vacío si no desea actualizar): ")
                    while True:
                        gotoxy(80,10);nuevo_stock=input()
                        if not nuevo_stock:
                            nuevo_stock=pro['stock']
                            break
                        elif int(nuevo_stock) >= 0:
                            break
                        else:
                            gotoxy(80,10);print("Error: solo numeros")
                            time.sleep(1)
                            gotoxy(80,10);print(" "*20)


            # Actualizar la información del producto si se proporciona
                    gotoxy(30,11);update=input(red_color+"Desea guardar(s/n):"+reset_color)
                    if update.lower() == "s":
                        pro["descripcion"] = nuevo_nombre
                        pro["precio"] = float(nuevo_precio)
                        pro["stock"] = int(nuevo_stock)
            # Guardar los cambios en el archivo JSON de productos
                        json_file.save(products)
                        gotoxy(30,12);print("Producto actualizado exitosamente. :3")
                    break

        else:
            gotoxy(18,12);print("No se encontró ningún producto con el ID proporcionado.")
        gotoxy(34,14);input("Presione Enter para continuar...")
    
    def delete(self):
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminar producto"+" "*36+"██")
        json_file = JsonFile(path+'/archivos/products.json')
        invoices1 = json_file.read()
        print(purple_color+"productos"+reset_color)
        gotoxy(2,4);print(green_color+"id")
        gotoxy(15,4);print("Descripcion")
        gotoxy(30,4);print("Precio")
        gotoxy(50,4);print("Stock"+reset_color)
        d=1
        for fac in invoices1:
            gotoxy(2,4+d);print(f"{blue_color}{fac['id']} ")
            gotoxy(15,4+d);print(f"{fac['descripcion']} ")
            gotoxy(30,4+d);print(f"{fac['precio']} ")
            gotoxy(50,4+d);print(f"{fac['stock']}")
            d+=1
        
        invoice= input("\tIngrese id de producto a eliminar: ")
        if invoice.isdigit():
            invoices = json_file.delete("id",int(invoice))
            print(invoices)
        else:
            print("No ingreso el id correspondiente.... intentelo mas tarde..."+reset_color)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de productos"+" "*35+"██")
        json_file = JsonFile(path+'/archivos/products.json')
        invoices = json_file.read()
        gotoxy(2,3);print(purple_color+"productos"+reset_color)
        gotoxy(2,4);print(green_color+"id")
        gotoxy(15,4);print("Descripcion")
        gotoxy(30,4);print("Precio")
        gotoxy(50,4);print("Stock"+reset_color)
        d=1
        for fac in invoices:
            gotoxy(2,4+d);print(f"{blue_color}{fac['id']} ")
            gotoxy(15,4+d);print(f"{fac['descripcion']} ")
            gotoxy(30,4+d);print(f"{fac['precio']} ")
            gotoxy(50,4+d);print(f"{fac['stock']}")
            d+=1
        gotoxy(2,4+d);x=input("presione una tecla para continuar...")       
        print("regresando.....") 

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    

    

    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices1 = json_file.read()
        gotoxy(2,3);print("Facturas")
        f=1
        for fac in invoices1:
                gotoxy(2,3+f);print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
                f+=1
        gotoxy(2,3+f);print(green_color+"Ingrese Factura a MODIFICAR: "+reset_color)
        gotoxy(2,3+f);invoice = int(validar.solo_numeros("ERROR: solo numeros",30,3+f))
        
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.find("factura",invoice)
        if invoices:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(30,1);print(yellow_color+f"Impresion de la Factura")
            gotoxy(2,2);print("*"*90+reset_color)
            for fac in invoices:
                follow="s"
                
                gotoxy(5,4);print(green_color+f"Factura#: {fac['factura']} {''*3} Fecha:{fac['Fecha']}")
                gotoxy(5,6);print(f"Comprador: {fac['cliente']}")
                gotoxy(66,4);print(f"Subtotal: {fac['subtotal']}")
                gotoxy(66,5);print(f"Decuento: {fac['descuento']}")
                gotoxy(66,6);print(f"Iva     : {fac['iva']}")
                gotoxy(66,7);print(f"Total   : {fac['total']}")
                gotoxy(2,8);print(purple_color+"*"*90+reset_color) 
                gotoxy(24,9);print(blue_color+"Articulo") 
                gotoxy(38,9);print("Precio") 
                gotoxy(48,9);print("Cantidad") 
                gotoxy(58,9);print("Subtotal") 
                gotoxy(70,9);print("s->para Modificar)"+reset_color)
                d=1
                iva_percentage = 0.12
                discount_percentage = 0.10
                #new_quantity = 0
                updated_details=[]
                new_subtotal=0
                #l=1
                for det in fac['detalle']:
                    d=+1
                    gotoxy(24,9+d);print(cyan_color+det['poducto']) 
                    gotoxy(38,9+d);print(det['precio']) 
                    gotoxy(48,9+d);print(det['cantidad']) 
                    gotoxy(53,9+d);qyt=int(validar.solo_numeros2("Error:Solo numeros",53,9+d))
                    gotoxy(58,9+d);print(qyt*det['precio'])
                    gotoxy(74,9+d);follow=input(reset_color) or "s" 
                    gotoxy(76,9+d);print(green_color+"✔"+reset_color)
                    if follow.lower()=="s":
                        if qyt > 0:
                            det["cantidad"] = qyt
                            updated_details.append(det)
                            new_subtotal += det["precio"] * det["cantidad"]                                
                    else:
                        updated_details.append(det)
                        new_subtotal += det["precio"] * det["cantidad"]                                  
                if updated_details==[]:    
                    invoices = json_file.delete("factura",int(invoice))
                    print(red_color+"Factura eliminada al quitar todos los productos"+reset_color)
                else:
                    fac['detalle'] =  updated_details
                    fac["subtotal"] = round(new_subtotal,2)
                    fac["descuento"] = round((new_subtotal * discount_percentage),2)
                    fac["iva"] = round(((new_subtotal - (new_subtotal * discount_percentage)) * iva_percentage),2)
                    fac["total"] = round((new_subtotal - (new_subtotal * discount_percentage) + ((new_subtotal - (new_subtotal * discount_percentage)) * iva_percentage)),2)   
                    #print(fac)
                    #print(invoices[0])
                    empty_invoice=[]
                    c=0
                    for fac2 in invoices1:
                        c+=1
                        if invoice==c:  
                            empty_invoice.append(fac)
                        else:
                                empty_invoice.append(fac2)      
                    json_file.save(empty_invoice)               
        else: 
            gotoxy(2,3);print(purple_color+"Facturas"+reset_color)
            f=0
            for fac in invoices1:
                    gotoxy(2,4+f);print(blue_color+f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}"+reset_color)
                    f+=1  
            print(red_color+"NO SE LOGRO REEMBOLSAR \nINTENTELO MAS TARDE"+reset_color)
            time.sleep(3)
    def delete(self):
        print('\033c', end='')
        gotoxy(2,1);print(red_color+"█"*90)
        gotoxy(2,2);print("██"+" "*35+"Eliminar factura"+" "*35+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices1 = json_file.read()
        print(purple_color+"Facturas"+reset_color)
        gotoxy(2,4);print(green_color+"Factura")
        gotoxy(15,4);print("Fecha")
        gotoxy(30,4);print("Cliente")
        gotoxy(50,4);print("Total"+reset_color)
        d=1
        for fac in invoices1:
            gotoxy(2,4+d);print(f"{blue_color}{fac['factura']} ")
            gotoxy(15,4+d);print(f"{fac['Fecha']} ")
            gotoxy(30,4+d);print(f"{fac['cliente']} ")
            gotoxy(50,4+d);print(f"{fac['total']}")
            d+=1
        invoice= input("\tIngrese Factura a eliminar: ")
        if invoice.isdigit():
            invoices = json_file.delete("factura",int(invoice))
            print(invoices)
        else:
            print("No ingreso el id correspondiente.... intentelo mas tarde..."+reset_color)


    
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        json_file = JsonFile(path+'/archivos/invoices.json')
        gotoxy(2,2);invoices = json_file.read()
        gotoxy(2,3);print("Facturas")
        f=4
        for fac in invoices:
                gotoxy(2,f);print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
                f+=1
        gotoxy(2,f);invoice= input("Factura: ")
        borrarPantalla()
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            gotoxy(30,1);print(f"Impresion de la Factura")
            gotoxy(2,2);print(green_color+"*"*90+reset_color)
            for fac in invoices:
                gotoxy(5,4);print(f"Factura#: {fac['factura']} {''*3} Fecha:{fac['Fecha']}")
                gotoxy(5,6);print(f"Comprador: {fac['cliente']}")
                gotoxy(66,4);print(f"Subtotal: {fac['subtotal']}")
                gotoxy(66,5);print(f"Decuento: {fac['descuento']}")
                gotoxy(66,6);print(f"Iva     : {fac['iva']}")
                gotoxy(66,7);print(f"Total   : {fac['total']}")
                gotoxy(2,8);print(green_color+"*"*90+reset_color) 
                gotoxy(5,9);print(purple_color) 
                gotoxy(12,9);print(" ")
                gotoxy(24,9);print("Articulo") 
                gotoxy(38,9);print("Precio") 
                gotoxy(48,9);print("Cantidad") 
                gotoxy(58,9);print("Subtotal") 
                gotoxy(68,9);print(reset_color)
                gotoxy(5,9);print(green_color) 
                d=1
                
                for det in fac['detalle']:
                    gotoxy(12,9+d);print(d)
                    gotoxy(24,9+d);print(det['poducto']) 
                    gotoxy(38,9+d);print(det['precio']) 
                    gotoxy(48,9+d);print(det['cantidad']) 
                    gotoxy(58,9+d);print(det['precio']*det['cantidad'])
                    d+=1
                gotoxy(58,d);print(reset_color)
                
            
            gotoxy(2,9+d);x=input("presione una tecla para continuar...")    
        else:    
            print("regresando.....") 

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()  
            client=CrudClients()  
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                client.create()
                time.sleep(1)
            elif opc1 == "2":
                client.update()
                time.sleep(1)
            elif opc1 == "3":
                client.delete()
                time.sleep(1)
                pass
            elif opc1 == "4":
                client.consult()
                time.sleep(1)
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()  
            product=CrudProducts()  
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                product.create()
                time.sleep(1)
            elif opc2 == "2":
                product.update()
                time.sleep(1)
            elif opc2 == "3":
                product.delete()
                time.sleep(1)
            elif opc2 == "4":
                product.consult()
                time.sleep(1)
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                time.sleep(2)
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
                time.sleep(2)
            elif opc3 == "4":
                sales.delete()
                time.sleep(2)
                
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

