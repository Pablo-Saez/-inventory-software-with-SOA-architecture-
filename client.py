import socket

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
    # recibir_respuesta()

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
    while True:
        #PARA ESTE PUNTO TENDREMOS LAS VARIABLES DE SESION EN email,password,name,role
        print("BIENVENIDO " + name  + " ERES USUARIO TIPO: " +role)
        print("2. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            service = input("Ingrese el servicio: ")
            data = input("Ingrese los datos: ")
            enviar_mensaje(service, data)
            recibir_respuesta()
        elif opcion == "2":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

finally:
    print('Closing socket')
    sock.close()
