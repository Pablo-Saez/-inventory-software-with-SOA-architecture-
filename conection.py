import psycopg2
import socket
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    # Establece la conexión con la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname="inventario",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    logging.info("Conexión a la base de datos exitosa.")

    cursor = conn.cursor()

    def read_init_sql(file_path):
        with open(file_path, "r") as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script)

    # def CreateUser(Rut, Name, Last_name, Role):
    #     cursor.execute("""
    #         INSERT INTO usuario (rut, nombre, apellido, cargo)
    #         VALUES (%s, %s, %s, %s)
    #     """, (Rut, Name, Last_name, Role))

    #     row_count = cursor.rowcount
    #     print(row_count)
    #     conn.commit()
    #     if row_count > 0:
    #         logging.info("Usuario creado con éxito.")
    #         return row_count
    
    def CreateProduct(name,description,is_fragile,require_cold_chain,quantity):
        cursor.execute("""
            INSERT INTO producto (name, description, is_fragile, require_cold_chain,quantity)
            VALUES (%s, %s, %s, %s,%s)
        """, (name, description,is_fragile,require_cold_chain,quantity))
        row_count = cursor.rowcount
        print(row_count)
        conn.commit()
        if row_count > 0:
            logging.info("Usuario creado con éxito.")
            return row_count

    def CreateUser(name,role,email,password):
        cursor.execute("""
            INSERT INTO user (name, role, email, password)
            VALUES (%s, %s, %s, %s)
        """, (name, role,email,password))
        row_count = cursor.rowcount
        print(row_count)
        conn.commit()
        if row_count > 0:
            logging.info("Usuario creado con éxito.")
            return row_count



    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 5000)
    logging.info('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Resto de tu código de socket y operaciones de base de datos aquí
        message = b'00010sinitdatos'
        logging.info('sending {!r}'.format(message))
        sock.sendall(message)

        while True:
            logging.info("Waiting for transaction BBDD")
            amount_received = 0
            amount_expected = int(sock.recv(5))
            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)
                logging.info('received {!r}'.format(data))
                logging.info("Processing sql...")
                try:
                    data = data.decode().split()
                    print(data)
                    cadena = data[0]
                    opcion = cadena[5:]
                    print(opcion)
                    if opcion == '1':
                        Rut = data[1]
                        Name = data[2]
                        Last_name = data[3]
                        role = data[4]
                        print(Rut)

                        logging.info('Ingresando...')
                        priv = CreateUser(Rut, Name, Last_name, role)
                        logging.info(priv)
                        message = '00015datoscreateuser {}'.format(priv).encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)
                    
                    
                    elif opcion == '2':
                        
                        Name = data[1]
                        description = data[2]
                        is_fragile = data[3]
                        require_cold_chain = data[4]
                        quantity = data[5]
                        print(Name)
                        logging.info('Ingresando producto')
                        priv = CreateProduct(Name,description,is_fragile, require_cold_chain,quantity)
                        logging.info(priv)
                        message = '00018datoscreateproduct'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)

                    elif opcion == '3':
                        
                        Name = data[1]
                        role = data[2]
                        email = data[3]
                        password = data[4]
                        print(Name)
                        logging.info('Creando Usuario')
                        priv = CreateProduct(Name,role,email, password)
                        logging.info(priv)
                        message = '00015datoscreateuser'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)

                except Exception as e:
                    logging.error(f'Error: {e}')
                    logging.info('-------------------------------')

    finally:
        logging.info('closing socket')
        sock.close()

    

except psycopg2.Error as e:
    logging.error(f"No se pudo conectar a la base de datos. Error: {e}")
