from flask import Flask, jsonify, g, request
from multiprocessing import Process
import sqlite3
import time
import random


DATABASE = '/app/clients.db'
delay = 30
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def delayed_insert(client_id, service_id):
    time.sleep(random.randint(0, delay))
    conn = sqlite3.connect(DATABASE)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM CLIENT_SERVICE"
                     " WHERE CLIENTS_CLIENT_ID = {clnt_id}"
                     " AND SERVICES_SERVICE_ID = {srv_id}".format(clnt_id=client_id, srv_id=service_id))
        db_services = curs.fetchall()

        if not db_services:
            curs.execute("INSERT INTO CLIENT_SERVICE(CLIENTS_CLIENT_ID, SERVICES_SERVICE_ID)"
                         "VALUES({clnt_id}, {srv_id})".format(clnt_id=client_id, srv_id=service_id))

            curs.execute("SELECT BALANCE FROM BALANCES"
                         " WHERE CLIENTS_CLIENT_ID = {clnt_id}".format(clnt_id=client_id))
            balance = curs.fetchall()[0][0]

            curs.execute("SELECT COST FROM SERVICES"
                         " WHERE SERVICE_ID = {srv_id}".format(srv_id=service_id))
            cost = curs.fetchall()[0][0]
            new_balance = balance - cost

            curs.execute("UPDATE BALANCES SET BALANCE = {new_balance}"
                         " WHERE CLIENTS_CLIENT_ID = {clnt_id}".format(new_balance=new_balance, clnt_id=client_id))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def root():
    return "It's alive!"


@app.route('/services')
def services_request():
    curs = get_db().cursor()
    curs.execute("SELECT * FROM SERVICES")
    db_services = curs.fetchall()
    services = {'count': 0, 'items': []}
    for service in db_services:
        services['count'] += 1
        services['items'].append({'id': service[0], 'name': service[1], 'cost': service[2]})
    return jsonify(services)


@app.route('/client/services', methods=['POST'])
def client_service_request():
    curs = get_db().cursor()
    data = request.get_json()
    services = {'count': 0, 'items': []}
    if 'client_id' in data:
        curs.execute("SELECT * FROM SERVICES AS S"
                     " INNER JOIN CLIENT_SERVICE AS CS ON S.SERVICE_ID = CS.SERVICES_SERVICE_ID"
                     " WHERE CLIENTS_CLIENT_ID = {0}".format(data['client_id']))
        db_services = curs.fetchall()
        for service in db_services:
            services['count'] += 1
            services['items'].append({'id': service[0], 'name': service[1], 'cost': service[2]})
        return jsonify(services)
    return "Request error", 400


@app.route('/client/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    if 'service_id' in data and 'client_id' in data:
        p = Process(target=delayed_insert, args=(data['client_id'], data['service_id']))
        p.daemon = True
        p.start()
        return "Processing", 202
    return "Request error", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
