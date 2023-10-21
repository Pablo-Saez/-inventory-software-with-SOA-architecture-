import psycopg2
import socket
import sys
import logging

def bdCall(msg):
    print("desde crear usuario, este es el msg " + msg)

    sock.sendall(msg.encode())

    # Recibir respuesta
    response_len_str = sock.recv(5).decode()
    response_len = int(response_len_str)
    response_service = sock.recv(5).decode()
    response_data = sock.recv(response_len - 5).decode()

    #print(f"Recibido: {response_data}")
    return response_data

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 5000)
logging.info('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)


try:
    # Resto de tu código de socket y operaciones de base de datos aquí
    message = b'00011sinitcruser' #cruser = create user
    logging.info('sending {!r}'.format(message))
    sock.sendall(message)

    while True:
        logging.info("Waiting for transactions create user")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            logging.info('received {!r}'.format(data))
            logging.info("Calling the db for creation...")
            try:
                data = data.decode().split()

                cadena = data[0]
                name = cadena[5:]
                role = data[1]
                email = data[2]
                password= data[3]

                
                service = "datos"
                cadena_completa = '3'+' '+ name + ' ' + role + ' ' + email + ' ' + password
                msg_len = len(cadena_completa) + len(service)
                msg = f"{msg_len:05d}{service}{cadena_completa}"
                print("desde crear user, este es el msg " + msg)
                
                # sock.sendall(msg.encode())
                
                # # Receive response
                # response_len_str = sock.recv(5).decode()
                # response_len = int(response_len_str)
                # response_service = sock.recv(5).decode()
                # response_data = sock.recv(response_len - 5).decode()
                response_data = bdCall(msg)
                print(response_data)
                # print(f"Received: {response_data}")
                #logging.info('Ingresando...')
                
                #logging.info(priv)
                message = '00015datoscreateuser'.encode()
                logging.info('sending {!r}'.format(message))                    
                sock.sendall(message)
            except Exception as e:
                logging.error(f'Error: {e}')
                logging.info('-------------------------------')

finally:
    logging.info('closing socket')
    sock.close()
