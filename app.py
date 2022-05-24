import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect, jsonify
from bson.objectid import ObjectId

app = Flask(__name__)

# On se connecte avec pymongo à notre BDD MongoDB Atlas
client = MongoClient("mongodb+srv://adm:ADMpass123@initial.e0fas.mongodb.net/initial?retryWrites=true&w=majority")
db = client["initial"]
sal = db.salary


# Affiche la liste de tous les utilisateurs et ajout / suppression d'utilisateur


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        status = request.form['status']
        position_title = request.form['position_title']
        pay_basis = request.form['pay_basis']
        salary = request.form['salary']
        year = request.form['year']
        gender = request.form['gender']
        sal.insert_one({'last_name': last_name, 'first_name': first_name, 'status': status,
                        'position_title': position_title, 'pay_basis': pay_basis, 'salary': salary,
                        'year': year, 'gender': gender})
        return redirect(url_for('index'))

    all_doc = sal.find()
    return render_template('index.html', sal=all_doc)

# Recherche par variable et valeur associée


@app.route('/search/<variable>/<value>/', methods=('GET', 'POST'))
def search(variable, value):
    return jsonify(list(sal.find({variable: value}, {"_id": 0, "index": 0, "level_0": 0})))


# Retourne la liste sous format json des n salaires les plus faibles


@app.route('/findmin/<int:n>/', methods=('GET', 'POST'))
def findnls(n):
    return jsonify(list(sal.find({}, {"_id": 0, "index": 0, "level_0": 0},
                                 sort=[('salary', pymongo.ASCENDING)], limit=n)))


# Retourne la liste sous format json des n salaires les plus hauts


@app.route('/findmax/<int:n>/', methods=('GET', 'POST'))
def findnmx(n):
    return jsonify(list(sal.find({}, {"_id": 0, "index": 0, "level_0": 0},
                                 sort=[('salary', pymongo.DESCENDING)], limit=n)))


@app.route("/replace_by_id/<idx>/<last_name>/<first_name>/<year>/<status>/<pay_basis>/<position_title>/<salary"
           ">/<gender>/")
def replace_one(idx, last_name, first_name, year, status, pay_basis, position_title, salary, gender):
    sal.replace_one({'_id': ObjectId(idx)}, {'last_name': last_name,
                                             'first_name': first_name,
                                             'year': year,
                                             'status': status,
                                             'pay_basis': pay_basis,
                                             'position_title': position_title,
                                             'salary': salary,
                                             'gender': gender})
    return jsonify("Replace sur le doc " + idx + " ok.")


@app.route("/replace/<variable>/<valeur>/<last_name>/<first_name>/<year>/<status>/<pay_basis>/<position_title"
           ">/<salary>/<gender>/")
def replace_by_var(variable, valeur, last_name, first_name, year, status, pay_basis, position_title, salary, gender):
    sal.replace_one({variable: valeur}, {'last_name': last_name,
                                         'first_name': first_name,
                                         'year': year,
                                         'status': status,
                                         'pay_basis': pay_basis,
                                         'position_title': position_title,
                                         'salary': salary,
                                         'gender': gender})
    return jsonify("Replace sur le doc ayant la variable " + variable + " set avec la valeur " + valeur + " ok.")


@app.route("/update/<idx>/<variable>/<valeur>/")
def update_one(idx, variable, valeur):
    sal.update_one({'_id': ObjectId(idx)}, {'$set': {variable: valeur}})
    return jsonify("Update sur le doc " + idx + " de la variable " + variable + " par la valeur " + valeur + " ok.")


@app.post('/<id>/delete/')
def delete(id):
    sal.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
