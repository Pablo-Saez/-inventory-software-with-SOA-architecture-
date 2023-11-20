import psycopg2
import socket
import sys
import logging
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    conn = psycopg2.connect(
        dbname="powmhjrm",  # Actualiza el nombre de la base de datos
        user="powmhjrm",  # Actualiza el usuario
        password="VNJkgl6HTbKcJKfqjzyy6n9EO2FZjbIV",  # Actualiza la contraseña
        host="suleiman.db.elephantsql.com",  # Actualiza el host
        port="5432"  # El puerto generalmente es el mismo, pero confirma en tu dashboard
    )
    logging.info("Conexión a la base de datos exitosa.")

    cursor = conn.cursor()
    #dbname = os.getenv("DB_NAME")
    #user = os.getenv("DB_USER")
    #password = os.getenv("DB_PASSWORD")
    #host = os.getenv("DB_HOST")
    #port = os.getenv("DB_PORT")

    # Establecer la conexión con la base de datos PostgreSQL utilizando las variables de entorno
    
    '''conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )'''

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
    def CreateProduct(Nombre, Caracteristicas, Dias_caducidad, Temperatura_Optima, Stock):
        cursor.execute("""
            INSERT INTO Producto (Nombre, Caracteristicas, Dias_caducidad, Temperatura_Optima, Stock)
            VALUES (%s, %s, %s, %s, %s)
        """, (Nombre, Caracteristicas, Dias_caducidad, Temperatura_Optima, Stock))
        conn.commit()

        row_count = cursor.rowcount
        if row_count > 0:
            logging.info("Producto creado con éxito.")
            return row_count
    def Login(email, password):
        cursor.execute("""
            SELECT * FROM usuario
            WHERE correo = %s AND contrasena = %s
        """, (email, password))
        result = cursor.fetchall()
        print(result)
        if result:
            # Si hay coincidencias, significa que la cuenta existe
            return result
        else:
            # Si no hay coincidencias, la cuenta no existe
            return None
    def GetProducts():
        cursor.execute("""
            SELECT * FROM producto
            ORDER BY ID_PRODUCTO ASC
            """)
        result = cursor.fetchall()
        
        return result
    def GetEntrada_Salida():
        cursor.execute("""
            SELECT * FROM entrada_salida_bodega
            """)
        result = cursor.fetchall()
        return result

    def ModStock(Id, Stock):
            cursor.execute("""
                UPDATE producto
                SET Stock = %s
                where ID_PRODUCTO = %s
            """, ( Stock, Id))
            row_count = cursor.rowcount
            
            conn.commit()
            if row_count > 0:
                logging.info("Stock Modificado con éxito.")
                return row_count
    def GetReportes():
        cursor.execute("""
            SELECT * FROM reporte_supervision
            """)
        result = cursor.fetchall()
        return result
    
    def RegisterProduct(Id,operacion,cantidad):
        if operacion == "Entrada":
            cursor.execute("""
            UPDATE producto
            SET Stock = Stock + %s
            where ID_PRODUCTO = %s
            """, ( cantidad, Id))
            row_count = cursor.rowcount
            
            conn.commit()
            if row_count > 0:
                logging.info("Registro de stock realizado con éxito.")
                return row_count
        
        elif operacion == "Salida":
            print("salidaaaa")
            cursor.execute("""
            UPDATE producto
            SET Stock = Stock - %s
            where ID_PRODUCTO = %s
            """, ( cantidad, Id))
            row_count = cursor.rowcount
            
            conn.commit()
            if row_count > 0:
                logging.info("Registro de stock realizado con éxito.")
                return row_count
        else:
            return

    def GetUsers():
        cursor.execute("""
            SELECT * FROM usuario
            """)
        result = cursor.fetchall()
        return result
    
    def RecordInOut(id_user,state,date,time):
        cursor.execute("""
            INSERT INTO entrada_salida_bodega (id_usuario, procedimiento, fecha, hora)
            VALUES (%s, %s, %s, %s)
        """, (id_user,state,date,time))
        row_count = cursor.rowcount
        
        conn.commit()
        if row_count > 0:
            logging.info("movimiento registrado con éxito.")
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
                    elif opcion == '4':
                        email = data[1]
                        password = data[2]
                        print("desde el connection:")
                        print(email)
                        print(password)
                        data_login=Login(email,password)
                        nombre = data_login[0][1]
                        tipo = data_login[0][4]
                        response = nombre + ' ' + tipo
                        response_len = len(nombre) + len(tipo)
                        #HAY UN PROBLEMA AQUI. CUANDO ENVIO LA RESPUESTA DEVUELTA
                        #AL LOGIN SE ENVIA UN PROPIO MENSAJE A LA BD REPITIENDO EL PROCESO
                        message = f"{response_len:05d}datos{response}"
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message.encode())
                    elif opcion == '5':

                        param = data[1]
                        print(param)
                        if param == 'products':
                            products = GetProducts()
                            msg = 'datos'

                            # Iterar sobre cada producto en la respuesta de la base de datos
                            for product in products:
                                # Extraer el ID, nombre y stock de cada producto
                                id_producto, nombre, _, _, _, stock = product

                                # Imprimir la información
                                msg += f" {id_producto} {nombre} {stock}"
                            len_msg = len(msg)
                            cadena_final = f"{len_msg:05d}{msg}"
                            logging.info('sending {!r}'.format(cadena_final))
                            sock.sendall(cadena_final.encode())
                        elif param == 'in_out':
                            print("entrada y salida de bodega")
                            in_outs = GetEntrada_Salida()
                            print(in_outs)
                            msg = 'datos'
                            for in_out in in_outs:
                                # Extraer el ID, nombre y stock de cada producto
                                id, id_usuario, procedimiento, fecha, hora = in_out

                                # Imprimir la información
                                msg += f" {id} {id_usuario} {procedimiento} {fecha} {hora}"
                            len_msg = len(msg)
                            cadena_final = f"{len_msg:05d}{msg}"
                            logging.info('sending {!r}'.format(cadena_final))
                            sock.sendall(cadena_final.encode())
                        elif param == 'reports':
                            print("entregar reportes de la bd")
                            reports = GetReportes()
                            msg = 'datos'
                            for report in reports:
                                # Extraer el ID, nombre y stock de cada producto
                                id, id_usuario, descripcion, fecha, hora = report

                                # Imprimir la información
                                msg += f"|{id}|{id_usuario}|{descripcion}|{fecha}|{hora}"
                            len_msg = len(msg)
                            cadena_final = f"{len_msg:05d}{msg}"
                            logging.info('sending {!r}'.format(cadena_final))
                            sock.sendall(cadena_final.encode())

                    elif opcion == '6':
                        
                        Id = data[1]
                        Stock = data[2]

                        logging.info('Modificando Stock')
                        priv = ModStock(Id,Stock)
                        
                        message = '00015datosmodifstock'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)
                    

                    elif opcion=='8':
                        users = GetUsers()
                        msg = 'datos'
                        for user in users:
                                # Extraer el ID, nombre y stock de cada producto
                                id_usuario, nombre, correo,_,tipo = user

                                # Imprimir la información
                                msg += f" {id_usuario} {nombre} {correo} {tipo}"
                        len_msg = len(msg)
                        cadena_final = f"{len_msg:05d}{msg}"
                        logging.info('sending {!r}'.format(cadena_final))
                        sock.sendall(cadena_final.encode())
                    elif opcion=='9':
                        id_user = data[1]
                        state = data[2]
                        date = data[3]
                        time = data[4]
                        func = RecordInOut(id_user,state,date,time)
                        logging.info(func)
                        message = '00013datosregistro'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)

                        


                        
                    elif opcion == '7':
                        Id = data[1]
                        operacion = data[2]
                        cantidad = data[3]

                        logging.info('Registrando Movimiento de producto')
                        priv = RegisterProduct(Id,operacion,cantidad)
                        
                        message = '00015datosregdeprodc'.encode()
                        logging.info('sending {!r}'.format(message))
                        sock.sendall(message)   
                    elif opcion == '8':
                        msg = 'datos'

                        logging.info('Monitor productos en expiracion')
                        priv = RegisterProduct(Id,operacion,cantidad)
                        
                        message = '00015rvprxp'.encode()
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