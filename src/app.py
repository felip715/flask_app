from crypt import methods
from validar import validar_mail
from flask import Flask, jsonify, request
from config import config, connection
from dotenv import load_dotenv
from function_jwt import write_token, validate_token


app=Flask(__name__)  #este archivo es el principal de la aplicacion

@app.route('/listar',methods=['GET'])
def listar():
    try:
        #utilizar cursor
        cursor=connection.cursor()
        #crear la consulta
        sql='SELECT * FROM users'
        #ejecutar la consulta
        cursor.execute(sql)
        #mostrar resultados
        registro=cursor.fetchall()
        #cerrar conexion
        #TODO: Cerrar conexion si o si. El error salta porque abris la conexion en la configuracion. Hace una funcion para conectarte y llama esa funcion cada vez que la necesites. En config.py si crea variables con los datos que necesitas para conectarte.
        #cursor.close()
        #connection.close()
        datos=[]
        for fila in registro:
            dato={'dni':fila[0],'name':fila[1],'surname':fila[2],'sex':fila[3],'born':fila[4],'phone':fila[5],
            'address':fila[6],'email':fila[7],'pass':fila[10]}
            datos.append(dato)
        return jsonify({'datos':datos, 'mensaje':"Datos listados"})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':"Error"})


@app.route('/listar/<dni>',methods=['GET'])
def leer(dni):
    try:
        cursor=connection.cursor()
        sql = "SELECT * FROM users WHERE dni = '{0}'".format(dni)
        cursor.execute(sql)
        registro=cursor.fetchone()
        #TODO: Cerrar conexion
        #cursor.close()
        #connection.close()
        if registro != None:
            dato={'dni':registro[0],'name':registro[1],'surname':registro[2],'sex':registro[3],
            'born':registro[4],'phone':registro[5],'address':registro[6],'email':registro[7],'pass':registro[10]}
            return jsonify({'datos':dato, 'mensaje':"Dato listado"})
        else:
            return jsonify({'mensaje':"Dato no encontrado"})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje':"Error"})


@app.route('/register',methods=['POST'])
def registrar_datos():
    try:
        #TODO: SI no envias nada en la request se rompe, hace control de errores antes de generar la query.

        cursor=connection.cursor()
        sql = """INSERT INTO users (dni, name, surname, sex, born, phone, address, email, pass) VALUES 
        ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(request.json['dni'],
        request.json['name'], request.json['surname'],request.json['sex'],
        request.json['born'],request.json['phone'],request.json['address'],request.json['email'],request.json['pass'])
        val_mail = validar_mail("'{0}'".format(request.json['email']))
        print(val_mail)
        if val_mail:
            cursor.execute(sql)
            connection.commit() #confirma la accion de insercion

            #TODO: Cerra la conexión.
            cursor.close()
            connection.close()
            return write_token(data=request.get_json()) #TODO: Retornar algo más significatico, ej: {'status': 200, 'token': write_token(data=request.get_json()), 'message': 'Registro exitoso'}
        else:
            return jsonify({"message" : "Incorrect email format"})
    except Exception as ex:  
        print("\nEl error es:")
        print(ex)
        return jsonify({'mensaje':"Error"}) #TODO: Fijate que en algunas partes pones mensaje y en otras message.

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    cursor=connection.cursor()
    try:
        email = data['email']
    except Exception as e:
        return jsonify({"message" : "Debe ingresar un email"})   #TODO: Controlar errores.

    try:
        pass_user = data['pass']
    except Exception as e:
        return jsonify({"message" : "Debe ingresar una contraseña"})   #TODO: Controlar errores.

    sql = "SELECT pass FROM users WHERE email = '{0}'".format(email)
    cursor.execute(sql)
    password=cursor.fetchone()
    passw = password[0]

    #TODO: Siempre cerrar la bbdd para que no queden hilos pendientes.
    cursor.close()
    connection.close()

    if passw != None:
        try:
            if pass_user == passw:
                print('La contraseña es correcta')
                return {'token' : write_token(data)}
            else:
                response = jsonify({"message": "Password is not correct"})
                response.status_code = 404
                return response
        except Exception as e:
            return jsonify({"message" : e})   #TODO: Controlar errores.
    else:
        return jsonify({"message" : "The mails does not exist"})

@app.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)


if __name__=='__main__':
    load_dotenv()
    app.config.from_object(config['development'])
    app.run()