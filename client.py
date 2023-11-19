#sudo docker run -d -p 5000:5000 jrgiadach/soabus:v1
import socket
import logging
import sys
from tabulate import tabulate
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# Función para enviar un mensaje al servidor
def enviar_mensaje(service, data):
    print(data)
    msg_len = len(service) + len(data)
    msg = f"{msg_len:05d}{service}{data}"
    print(msg)
    sock.sendall(msg.encode())

# Función para recibir la respuesta del servidor
def recibir_respuesta():
    print("respuesta recibida")
    response_len_str = sock.recv(5).decode()
    response_len = int(response_len_str)
    response_service = sock.recv(5).decode()
    response_data = sock.recv(response_len - 5).decode()
    print(f"Received: {response_data}")

def GetUsers():
    service = 'datos'
    msg = service + '8'
    msg_len = len(msg)
    final_msg = f"{msg_len:05d}{msg}"
    sock.sendall(final_msg.encode())
    logging.info ('sending to bbdd {!r}'.format (final_msg))
    response_len_str = sock.recv(5).decode()
    response_len = int(response_len_str)
    response_service = sock.recv(5).decode()
    response_data = sock.recv(response_len - 5).decode()
    #print(f"Received: {response_data}")

    linea=response_data[2:]
    datos = linea.split()
    users = [datos[i:i+4] for i in range(0, len(datos), 4)]
    #print(users)
    return users




    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
sock.connect(server_address)

print("Bienvenido a UDPInventory...")

while True:
    print("Por favor, inicie sesión antes de empezar a trabajar")
    email = input("Ingrese su email: ")
    password = input("Ingrese su contrasena: ")
    data_login = email + ' ' + password

    # Aquí estamos llamando al servicio LOGIN
    enviar_mensaje("login", data_login)
    response_len_str = sock.recv(5).decode()
    response_len = int(response_len_str)
    response_service = sock.recv(5).decode()
    response_data = sock.recv(response_len - 5).decode()
    print(f"Received: {response_data}")

    status_login = response_data[:2]
    print(status_login)

    if status_login == "OK":
        aux = response_data.split()
        name = aux[0][2:]
        role = aux[1]
        print(f"Inicio de sesión exitoso. Name: {name}, Role: {role}. Continuando...")
        break
    elif status_login == "NK":
        print("Credenciales incorrectas. Intente nuevamente.")
    else:
        print("Respuesta no reconocida. Saliendo del bucle por seguridad.")
        break  # Puedes ajustar esto según el comportamiento deseado para respuestas no reconocidas


try:
    if role == 'Administrador':
        while True:
            #PARA ESTE PUNTO TENDREMOS LAS VARIABLES DE SESION EN email,password,name,role
            print("BIENVENIDO " + name  + " ERES USUARIO TIPO: " +role)
            print("Seleccione una opcion:")
            print("1.Crear Usuario")
            print("2.Obtener informacion de stock de bodega")
            print("3.Obtener informacion de entrada y salida a la bodega")
            print("4.Obtener informacion de los reportes generados")
            print("5. Modificar Stock")
            print("6. Crear Producto")
            print("7. Registrar movimiento de producto")
            print("8. Salir")

            opcion = input("Ingrese la opción deseada: ")

            if opcion == "1":

                service = "userc"
                namenew = input("Ingrese nombre del trabajador: ")
                rolenew = input("Ingrese cargo del trabajador: ")
                emailnew = input("Ingrese correo del trabajador: ")
                password = input("Ingrese contraseña del trabajador: ") 
                data = namenew+ ' '+rolenew+' '+emailnew+' '+password  
                
                msg_len = len(service) + len(data)
                msg = f"{msg_len:05d}{service}{data}"
                print(msg)
                # Send message
                sock.sendall(msg.encode())

                # Receive response
                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()

                print(f"Received: {response_data}")

                

           
            

            elif opcion == "2":
                #####################FETCH PRODUCTS###############
                msg = 'bodga1'
                len_msg = len(msg)
                msg_final = f"{len_msg:05d}{msg}"
                logging.info('sending {!r}'.format(msg_final))
                sock.sendall(msg_final.encode())

                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                #print(response_data)
                linea = response_data[4:]
                # Dividir la línea en palabras
                palabras = linea.split()

                # Almacenar los valores en un arreglo de a 3
                productos = [palabras[i:i+3] for i in range(0, len(palabras), 3)]
                columnas_productos = ['ID_PRODUCTO','NOMBRE PRODUCTO', 'STOCK']
                print(tabulate(productos,headers=columnas_productos,tablefmt='grid'))
            elif opcion == "3":
                ####################FETCH MOVIMIENTOS###########
                msg = 'bodga2'
                len_msg = len(msg)
                msg_final = f"{len_msg:05d}{msg}"
                logging.info('sending {!r}'.format(msg_final))
                sock.sendall(msg_final.encode())

                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                print(response_data)

                linea=response_data[4:]
                palabras = linea.split()
                in_outs = [palabras[i:i+5] for i in range(0, len(palabras), 5)]
                columnas_in_out = ['ID','ID USUARIO A CARGO','TIPO PROCEDIMIENTO','FECHA','HORA']
                print(tabulate(in_outs,headers=columnas_in_out,tablefmt='grid'))
            elif opcion == "4":
                msg = 'bodga3'
                len_msg = len(msg)
                msg_final = f"{len_msg:05d}{msg}"
                logging.info('sending {!r}'.format(msg_final))
                sock.sendall(msg_final.encode())
                
                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                

                linea=response_data[5:]
                palabras = linea.split('|')
                
                in_outs = [palabras[i:i+5] for i in range(0, len(palabras), 5)]
                columnas_reports = ['ID','ID USUARIO REPORTE','DESCRIPCION','FECHA','HORA']
                print(tabulate(in_outs,headers=columnas_reports,tablefmt='grid'))



                


            elif opcion == "5":
                    service = "mdstk"
                    print("MODIFICAR STOCK")
                    
                    id_product = input("Ingrese el ID del producto: ")
                    cantidadnew = input("Ingrese el nuevo stock: ")
                    
                    data=  id_product + ' ' + cantidadnew
                    msg_len = len(service) + len(data)
                    msg = f"{msg_len:05d}{service}{data}"
                    print(msg)
                    # Send message
                    sock.sendall(msg.encode())

                    # Receive response
                    response_len_str = sock.recv(5).decode()
                    response_len = int(response_len_str)
                    response_service = sock.recv(5).decode()
                    response_data = sock.recv(response_len - 5).decode()
                    print(f"Received: {response_data}")
                    
            elif opcion == "6":
                service = "crprd"
                print("CREAR PRODUCTO")
                nombre = input("Ingrese el nombre del producto: ")
                caracteristicas = input("Ingrese la descripción: ")
                fecha_vencimiento = input("Ingrese la fecha en formato yyyy-mm-dd, (en caso de no tener aprete enter)")
                temperatura_optima = input("Indique la temperatura optima del producto: ")
                stock = input("Ingrese la cantidad del producto: ")
                
                data=  nombre + ' ' + caracteristicas + ' ' + fecha_vencimiento + ' ' + temperatura_optima + ' ' + stock
                msg_len = len(service) + len(data)
                msg = f"{msg_len:05d}{service}{data}"
                print(msg)
                # Send message
                sock.sendall(msg.encode())

                # Receive response
                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()

                print(f"Received: {response_data}") 
            elif opcion == "7": 
                service = "rgprd"
                print("REGISTRAR MOVIMIENTO DE PRODUCTO")
                id_product = input("Ingrese el ID del producto: ")
                opcionreg = input("Entrada o Salida del Producto: ") 
                cantidadnew = input("Cantidad: ")
                                  
                data=  id_product + ' ' +opcionreg+ ' ' + cantidadnew
                msg_len = len(service) + len(data)
                msg = f"{msg_len:05d}{service}{data}"
                print(msg)
                # Send message
                sock.sendall(msg.encode())

                # Receive response
                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                print(f"Received: {response_data}")
                          
            elif opcion == "8":

                break
            else:
                print("Opción no válida. Intente de nuevo.")
    elif role == 'Guardia':
        while True:
            #PARA ESTE PUNTO TENDREMOS LAS VARIABLES DE SESION EN email,password,name,role
            print("BIENVENIDO " + name  + " ERES USUARIO TIPO: " +role)
            print("Seleccione una opcion:")
            print("1.Registrar entrada o salida")

            opcion = input("Ingrese la opción deseada: ")

            if opcion == "1":
                
                service = "userc"
                #namenew = input("Ingrese nombre del trabajador: ")
                users = GetUsers()
                columnas_users = ['ID USUARIO','NOMBRE USUARIO','EMAIL','ROLE']
                print(tabulate(users,headers=columnas_users,tablefmt='grid'))
                current_id = input("Ingrese ID del usuario a registrar: ")
                state_input = input("Ingrese un 1 para entrada y 0 para salida: ")

                # Verificar la entrada del usuario y asignar el valor adecuado a la variable state
                if state_input == '1':
                    state = 'Entrada'
                elif state_input == '0':
                    state = 'Salida'
                else:
                    print("Entrada no válida. Debe ingresar 1 para entrada o 0 para salida.")
                
                current_fecha = input("ingrese fecha en formato YYYY-MM-DD: ")
                current_hora = input("ingrese la hora en formato HH-MM-SS: ")

                msg = 'rgacc1' + ' ' +current_id + ' '+ state + ' ' + current_fecha + ' ' + current_hora
                len_msg = len(msg)
                msg_final = f"{len_msg:05d}{msg}"
                logging.info('sending {!r}'.format(msg_final))
                sock.sendall(msg_final.encode())



                # Send message
                

                # Receive response
                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                
                if response_data[:2] == "OK":
                    print("Registrado con éxito.")
                elif response_data[:2] == "NK":
                    print("Error.")
                else:
                    print("Error al registrar porfavor intentelo denuevo.")
                



finally:
    print('Closing socket')
    sock.close()
