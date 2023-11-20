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
    message = b'00010sinitrvprxp' #rvprxp
    logging.info ('sending {!r}'.format (message))
    sock.sendall (message)
    while True:
        # Look for the response
        logging.info ("Waiting for transaction Register_acces")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len (data)
            logging.info('received {!r}'.format(data))
            logging.info ("Processing login...")
            data = data.decode().split()
            print(data)
            cadena = data[0]
            opcion = cadena[5:]
                    
            try:
                if opcion == '1':

                    msg = '8'
                    service = "datos"
                    msg_len = len(msg) + len(service)              
                    final_msg = f"{msg_len:05d}{service}{msg}"
                    # #message = '000{}datos {} {} {}'.format(largo,opcion,email,password).encode()
                    
                    logging.info ('sending to bbdd {!r}'.format (final_msg))
                    sock.sendall(final_msg.encode())

                    response_len_str = sock.recv(5).decode()
                    response_len = int(response_len_str)
                    response_service = sock.recv(5).decode()
                    response_data = sock.recv(response_len - 5).decode()
                    print(response_data)

                    
                    msg_response=  'rvprxp' + response_data [2:]
                
                    len_msg = len(msg_response)
                    final_msg_response = f"{len_msg:05d}{msg_response}"
                    print(final_msg)
                    final_msg_encode= final_msg_response.encode()
                    logging.info('sending {!r}'.format(final_msg_response))
                    sock.sendall(final_msg_encode)
                 
        
            except:
                pass
            logging.info('-------------------------------')

finally:
    logging.info ('closing socket')
    sock.close ()