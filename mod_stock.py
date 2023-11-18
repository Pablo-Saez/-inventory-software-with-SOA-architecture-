import psycopg2
import socket
import sys
import logging

def bdCall(msg):
    print("desde modifcar stock, este es el msg " + msg)

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
    message = b'00010sinitmdstk' #mdstk = modificar stock
    logging.info('sending {!r}'.format(message))
    sock.sendall(message)

    while True:
        logging.info("Waiting for transactions modificar stock")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        print(amount_expected)
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            logging.info('received {!r}'.format(data))
            logging.info("Calling the db for creation...")
            try:
                print(data)
                data = data.decode().split()
                Id = data[0]
                Id = Id[5:]
                Stock = data[1]
                print(Id)
                # Prepare data to be sent in a format that connection.py understands
                formatted_data = f"6 {Id} {Stock}"
                msg_len = len(formatted_data) + 5  # 5 for "datos"
                msg = f"{msg_len:05d}datos{formatted_data}"
                sock.sendall(msg.encode())
                logging.info(f'Sending this msg to the db: {msg}')

                response_len_str = sock.recv(5).decode()
                response_len = int(response_len_str)
                response_service = sock.recv(5).decode()
                response_data = sock.recv(response_len - 5).decode()
                            
                logging.info(f'Database response: {response_data}')
                #logging.info(priv)

                message = '00015mdstkmodifstock'.encode()
                logging.info('sending {!r}'.format(message))                    
                sock.sendall(message)
            except Exception as e:
                logging.error(f'Error: {e}')
                logging.info('-------------------------------')

finally:
    logging.info('closing socket')
    sock.close()