import socket
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Create a TCP/IP socket
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
logging.info ('connecting to {} port {}'.format (*server_address))
sock.connect (server_address)
try:
    # Send data
    message = b'00010sinitbodga'  #bodga = bodega 
    logging.info ('sending {!r}'.format (message))
    sock.sendall (message)
    while True:
        # Look for the response
        logging.info ("Waiting for transaction bodega")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len (data)
            logging.info('received {!r}'.format(data))
            data = data.decode().split()
            print(data)
            cadena = data[0]
            opcion = cadena[5:]
            try:
                if opcion == '1': #productos
            
               
                    message = '00015datos5 products'
                    logging.info ('sending to bbdd {!r}'.format (message))
                    sock.sendall(message.encode())

                    response_len_str = sock.recv(5).decode()
                    response_len = int(response_len_str)
                    response_service = sock.recv(5).decode()
                    response_data = sock.recv(response_len - 5).decode()
                    print(f"Received: {response_data}")
                    
                    len_response_data = len(response_data)+5
                    cadena_final = f"{len_response_data:05d}bodga{response_data}"                
                    logging.info('sending {!r}'.format(cadena_final))
                    sock.sendall(cadena_final.encode())
                elif opcion == '2': #movimientos
                    message = '00013datos5 in_out'
                    logging.info ('sending to bbdd {!r}'.format (message))
                    sock.sendall(message.encode())

                    response_len_str = sock.recv(5).decode()
                    response_len = int(response_len_str)
                    response_service = sock.recv(5).decode()
                    response_data = sock.recv(response_len - 5).decode()
                    print(f"Received: {response_data}")

                    len_response_data = len(response_data)+5
                    cadena_final = f"{len_response_data:05d}bodga{response_data}"                
                    logging.info('sending {!r}'.format(cadena_final))
                    sock.sendall(cadena_final.encode())
                elif opcion=='3': #reportes
                    message = '00014datos5 reports'
                    logging.info ('sending to bbdd {!r}'.format (message))
                    sock.sendall(message.encode())

                    response_len_str = sock.recv(5).decode()
                    response_len = int(response_len_str)
                    response_service = sock.recv(5).decode()
                    response_data = sock.recv(response_len - 5).decode()
                    print(f"Received: {response_data}")

                    len_response_data = len(response_data)+5
                    cadena_final = f"{len_response_data:05d}bodga{response_data}"                
                    logging.info('sending {!r}'.format(cadena_final))
                    sock.sendall(cadena_final.encode())
                    




                
            except:
                pass
            logging.info('-------------------------------')

finally:
    logging.info ('closing socket')
    sock.close ()