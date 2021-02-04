import json
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Miguel1989@localhost:3306/todolist' 
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/todos/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):
    if request.method == 'GET':
        todo = Todo.query.filter_by(username=username).first()
        if not todo:
            return jsonify({"msg":"user not found"})
        return jsonify(todo.serialize()),200
            
    if request.method == 'POST':
        #obtener el cuerpo completo del request
        body = request.get_json()
        #validar el tipo de dato que esta recibiendo sea lista
        if not type(body) == list:
            return jsonify({"msg":"error"}), 400
        #añadir un objeto por defecto
        body.append({"label":"sample task", "done": "false"})
        #generar una instancia de la clase Todo
        todo = Todo()
        #asignar el username
        todo.username = username
        #convertir el array de tareas en un string
        todo.tasks = json.dumps(body) 
        #guardar en la base de datos
        todo.save()
        
        return jsonify(    {
        "result": "ok"
    }), 200

        
        

        
        
    if request.method == 'PUT':
        body = request.get_json()
        todo = Todo.query.filter_by(username=username).first()
        if todo:
            todo.tasks= json.dumps(body)
            todo.update()
            return jsonify({"result": "a list with " + str(len(body))+ " todos was successfully saved" }), 200
        else:
            return jsonify({"msg": "User not found"}), 400

        
    
    
    
    if request.method == 'DELETE':
        todo = Todo.query.filter_by(username=username).first()
        if not todo:
            return jsonify({"msg":"user not found"}), 404
        todo.delete()

        return jsonify({'result': 'OK'}), 200

if __name__ == '__main__':
    manager.run()