import psycopg2
import socket
import sys
import logging
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    # Establece la conexión con la base de datos PostgreSQL
    #    conn = psycopg2.connect("postgres://powmhjrm:VNJkgl6HTbKcJKfqjzyy6n9EO2FZjbIV@suleiman.db.elephantsql.com/powmhjrm")

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    # Establecer la conexión con la base de datos PostgreSQL utilizando las variables de entorno
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    logging.info("Conexión a la base de datos exitosa.")

    cursor = conn.cursor()

    def read_init_sql(file_path):
        with open(file_path, "r") as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script)


    def CreateUser(Nombre, Correo, Contrasena, Tipo):
        cursor.execute("""
            INSERT INTO usuario ( nombre, correo, contrasena, tipo)
            VALUES ( %s, %s, %s, %s)
        """, ( Nombre, Correo, Contrasena, Tipo))
        row_count = cursor.rowcount
        
        conn.commit()
        if row_count > 0:
            logging.info("Usuario creado con éxito.")
            return row_count
    def CreateProduct(Nombre, Caracteristicas, Fecha_Vencimiento, Temperatura_Optima, Stock):
        cursor.execute("""
            INSERT INTO Producto (Nombre, Caracteristicas, Fecha_Vencimiento, Temperatura_Optima, Stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (Nombre, Caracteristicas, Fecha_Vencimiento, Temperatura_Optima, Stock))
        conn.commit()

        row_count = cursor.rowcount
        if row_count > 0:
            logging.info("Producto creado con éxito.")
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
                    #CREATE USER
                    if opcion == '1': 
  
                        logging.info('Ingresando ...')
                        priv = CreateUser(*data[1:6])
                        logging.info(priv)
                        message = '00015datoscreateuser {}'.format(priv).encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)
                    
                    #CREATE PRODUCT
                    elif opcion == '2':
                        
                        logging.info('Ingresando producto')
                        priv = CreateProduct(*data[1:6])
                        logging.info(priv)
                        message = '00018datoscreateproduct'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)
                    #CREATE 
                    elif opcion == '3':
                        #(ID_Usuario, Nombre, Correo, Contrasena, Tipo))
                        Name = data[1]
                        email = data[2]
                        password = data[3]
                        role = data[4]
                        print(Name)
                        logging.info('Creando Usuario')
                        priv = CreateUser(Name,email,password, role)
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