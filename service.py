import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send data
    message = b'00010sinitresta'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    amount_received = 0
    amount_expected = int(sock.recv(5))
    while amount_received < amount_expected:
        data = sock.recv(amount_expected - amount_received)
        amount_received += len(data)
        print('received {!r}'.format(data))

    while True:
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            print('received {!r}'.format(data))

        print("Processing ...")
        received_str = data.decode()
        service = received_str[:5]
        numbers_str = received_str[5:].split()

        # if service == 'sumar' and len(numbers_str) == 2:
        #     sum_result = int(numbers_str[0]) + int(numbers_str[1])
        #     resp_data = f"OK{numbers_str[0]} + {numbers_str[1]} = {sum_result}"
        if service == 'resta' and len(numbers_str) == 2:
            sum_result = int(numbers_str[0]) - int(numbers_str[1])
            resp_data = f"OK{numbers_str[0]} - {numbers_str[1]} = {sum_result}"
        else:
            resp_data = "NKInvalid input"

        resp = '{:05d}'.format(len(service) + len(resp_data)) + service + resp_data
        print("Send answer (if needed)")
        print('sending {}'.format(resp))
        sock.sendall(bytes(resp, 'utf-8'))

finally:
    print('closing socket')
    sock.close()