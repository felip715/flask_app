from crypt import methods
from validar import validar_mail
from flask import Flask, jsonify, request
from config import config
from dotenv import load_dotenv
from function_jwt import write_token, validate_token
from conex_postgresql import conect_bbdd


app = Flask(__name__)  # este archivo es el principal de la aplicacion


@app.route('/listar', methods=['GET'])
def listar():
    try:
        # conectar a la base de datos
        connection = conect_bbdd()
        # utilizar cursor
        cursor = connection.cursor()
        # crear la consulta
        sql = 'SELECT * FROM users'
        # ejecutar la consulta
        cursor.execute(sql)
        # mostrar resultados
        registro = cursor.fetchall()
        # TODO: Cerrar conexion si o si. El error salta porque abris la conexion en la configuracion. Hace una funcion para conectarte y llama esa funcion cada vez que la necesites. En config.py si crea variables con los datos que necesitas para conectarte.
        cursor.close()
        connection.close()
        datos = []
        for fila in registro:
            dato = {'dni': fila[0], 'name': fila[1], 'surname': fila[2], 'sex': fila[3], 'born': fila[4], 'phone': fila[5],
                    'address': fila[6], 'email': fila[7], 'pass': fila[10]}
            datos.append(dato)
        return jsonify({'Info': datos, 'message': "information displayed"})
    except Exception as ex:
        response = jsonify({"message": "Error"})
        response.status_code = 404
        return response


@app.route('/listar/<dni>', methods=['GET'])
def leer(dni):
    try:
        connection = conect_bbdd()
        cursor = connection.cursor()
        sql = "SELECT * FROM users WHERE dni = '{0}'".format(dni)
        cursor.execute(sql)
        registro = cursor.fetchone()
        # TODO: Cerrar conexion
        cursor.close()
        connection.close()
        if registro != None:
            dato = {'dni': registro[0], 'name': registro[1], 'surname': registro[2], 'sex': registro[3],
                    'born': registro[4], 'phone': registro[5], 'address': registro[6], 'email': registro[7], 'pass': registro[10]}
            return jsonify({'Info': dato, 'message': "Information listed"})
        else:
            print("DNI not found")
            return jsonify({'menssage': "DNI not found"})
    except Exception as ex:
        response = jsonify({"message": "Error"})
        response.status_code = 404
        return response


@app.route('/register', methods=['POST'])
def registrar_datos():
    if request.json != None:
        try:
            # TODO: SI no envias nada en la request se rompe, hace control de errores antes de generar la query.
            connection = conect_bbdd()
            cursor = connection.cursor()
            sql = """INSERT INTO users (dni, name, surname, sex, born, phone, address, email, pass) VALUES 
            ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(request.json['dni'],
                                                                              request.json['name'], request.json[
                                                                                  'surname'], request.json['sex'],
                                                                              request.json['born'], request.json['phone'], request.json['address'], request.json['email'], request.json['pass'])
            val_mail = validar_mail("'{0}'".format(request.json['email']))
            if val_mail:
                cursor.execute(sql)
                connection.commit()  # confirma la accion de insercion
                # TODO: Cerra la conexión.
                cursor.close()
                connection.close()
                # TODO: Retornar algo más significatico, ej: {'status': 200, 'token': write_token(data=request.get_json()), 'message': 'Registro exitoso'}
                return {'status' : 200, 'token' : write_token(data=request.get_json()), 'message': 'Register Successful'}
            else:
                return jsonify({"message": "Incorrect email format"})
        except Exception as ex:
            print(ex)
            response = jsonify({"message": "Error"})
            response.status_code = 404
            return response
            
    else:
        print('Error, Missing data in json')
        return jsonify({'message': "Error, Missing data in json"})



@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    try:
        email = data['email']
    except Exception as e:
        # TODO: Controlar errores.
        print("the following data is missing")
        print(e)
        return jsonify({"message": "You must enter an Email"})

    try:
        pass_user = data['pass']
    except Exception as e:
        # TODO: Controlar errores.
        print("the following data is missing")
        print(e)
        return jsonify({"message": "You must insert a password"})

    sql = "SELECT pass FROM users WHERE email = '{0}'".format(email)
    
    try:
        connection = conect_bbdd()
        cursor = connection.cursor()
        cursor.execute(sql)
        password = cursor.fetchone()
        cursor.close()
        connection.close()
        if password != None:
            passw = password[0]
            if pass_user == passw:
                print('The password is correct')
                return {'status' : 200, 'token': write_token(data), 'message': 'Login Successful'}
            else:
                print('The password is not correct')
                response = jsonify({"message": "Password is not correct"})
                response.status_code = 404
                return response
        else:
            return jsonify({"message": "The mails does not exist"})
    except Exception as e:
        print(e)
        response = jsonify({"message": "Error"})
        response.status_code = 404
        return response


@app.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    a=validate_token(token, output=True)
    print(a)
    return jsonify({'token': a, 'status': 200, 'message': 'Token verified'})

if __name__ == '__main__':
    load_dotenv()
    app.config.from_object(config['development'])
    app.run()