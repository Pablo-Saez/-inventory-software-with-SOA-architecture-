import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
sock.connect(server_address)

try:
    # Prepare message
    service = "crprd"
    print("CREAR PRODUCTO")
    # nombre = input("Ingrese el nombre: ")
    # caracteristicas = input("Ingrese la descripción: ")
    # fecha_vencimiento = input("Ingrese la fecha en formato yyyy-mm-dd, (en caso de no tener aprete enter)")
    # temperatura_optima = input("Indique la temperatura optima del producto: ")
    # stock = input("Ingrese la cantidad del producto: ")

    nombre = 'papas_fritas'
    caracteristicas = 'papas_que_esta_fritas'
    fecha_vencimiento = "2023-12-31"
    temperatura_optima = '3'
    stock = '500'    
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

finally:
    print('closing socket')
    sock.close()
