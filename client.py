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
            print("2.Obtener informacion de bodega")
            print("3. Modificar Stock")
            print("4. Salir")

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
                ####################FETCH MOVIMIENTOS
                print(tabulate(productos,headers=columnas_productos,tablefmt='grid'))

            elif opcion == "3":
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
                    
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

finally:
    print('Closing socket')
    sock.close()
