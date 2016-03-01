""" qdotweb -- a Flask wraper for PyVISA instrument communication """

# this is the main code for qdotweb
# it is basically a flask wrapper for the PyVISA package
# use the flask development server to launch/test

from flask import Flask, render_template, request
from datetime import datetime
import visa
import json
import socket
from collections import OrderedDict
import sys

if socket.gethostname().find('.')>=0:
    hostname=socket.gethostname()
else:
    hostname=socket.gethostbyaddr(socket.gethostname())[0]
hostname = hostname.split('.')[0]

app = Flask(__name__)


### basic instrument information ###

rm = visa.ResourceManager()
instruments = {}

def format_resources_table(reslist):
    """ put instruments list into HTML table """
    table = '<table border="1" cellpadding="5" cellspacing="5">'
    table += '<caption>List of available resources:</caption>'
    table += '<tr> <th> </th> <th>Address</th> </tr>'
    for i, res in enumerate(reslist):
        table += '<tr> <td>{0:d}</td> <td>{1}</td> </tr>'.format(i, res)
    table += '</table>'
    return table

@app.route("/")
def main():
    global hostname
    global rm
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resources = rm.list_resources()
    resource_table = format_resources_table(resources)
    return render_template('index.html', hostname = hostname, 
                           resource_table = resource_table, current_time = current_time)
                           
def check_idn(resources):
    """ get the *IDN? response from any instruments that have it """
    ids = []
    errors = []
    for addr in resources:
        id = ''
        error = ''
        try:
            ctrl = rm.open_resource(addr)
            ctrl.timeout = 500
            id = ctrl.query('*IND?')
            ctrl.close()
        except Exception as e:
            error = str(e)
        ids.append(id)
        errors.append(error)
    return errors, ids
    
@app.route("/instruments")
def available_instruments():
    global rm
    
    resources = []
    resources_idn = []
    errors = []
    run_error = ''
    try:
        resources = [resource for resource in rm.list_resources()]
        errors, resources_idn = check_idn(resources)
    except Exception as e:
        run_error = str(e)
    errors.append(run_error)
    resources.append('url')
    resources_idn.append('')
    output = OrderedDict([('address', resources), ('IDN', resources_idn), ('errors', errors)])
    return json.dumps(output)
    
@app.route("/connected_instruments")
def list_connected_instruments():
    global instruments
    instruments_address = list(instruments.keys())
    output = OrderedDict([('instruments', instruments_address)])
    return json.dumps(output)
    
### control of individual instruments ###

# rules: urls should always return something. 
#        if an error occurs, leave data blank, catch the error, return some information
#        additional arguments can be added with POST keywords
#        use the same output format for all interaction with instruments

@app.route("/connect", methods=['POST', 'GET'])
def connect_instrument():
    """ create a visa resource for the instrument and store it in the 
        instruments/instruments_address arrays """
    global rm
    global instruments

    data = ''
    errors = ''
    address = ''
    if request.method == 'POST':
        post = request.form
        if 'address' in post:
            address = post['address']
        else:  
            raise ValueError('You did not send an address')
        try:
            if address in instruments:
                pass
            else:
                instruments[address] = rm.open_resource(address)
        except Exception as e:
            errors = str(e)
        data = 'CONNECTED'
    else:
        raise ValueError('please POST the address to connect')
    output = OrderedDict([('address', address), ('command', 'connect'), ('data', data), ('errors', errors)])
    return json.dumps(output)

def instrument_write(address, command):
    """ write to instrument """
    global instruments
    instruments[address].write(command)

@app.route("/write", methods=['POST', 'GET'])
def write():
    data = ''
    errors = ''
    address = ''
    command = ''
    try:
        if request.method == 'POST':
            post = request.form
            if post['address']:
                address = post['address']
            else:  
                raise ValueError('You did not send an address')
            if post['command']:
                command=request.form['command']
            else:  
                raise ValueError('You did not send a command')
        else:
            raise ValueError('Please POST an address and command')
        data = instrument_write(address, command)
        data = 'done'
    except Exception as e:
        errors = str(e)
    output = OrderedDict([('address', address), ('command', command), ('data', data), ('errors', errors)])
    return json.dumps(output)

def instrument_read(address):
    """ read from instrument """
    global instruments
    data = instruments[address].read(command)
    return data

@app.route("/read", methods=['POST', 'GET'])
def read():
    data = ''
    errors = ''
    address = ''
    command = ''
    try:
        if request.method == 'POST':
            post = request.form
            if post['address']:
                address = post['address']
            else:  
                raise ValueError('You did not send an address')
        else:
            raise ValueError('Please POST an address')
        data = instrument_read(address)
    except Exception as e:
        errors = str(e)
    output = OrderedDict([('address', address), ('command', command), ('data', data), ('errors', errors)])
    return json.dumps(output)

def instrument_query(address, command):
    """ query instrument """
    global instruments
    data = instruments[address].query(command)
    return data
    
@app.route("/query", methods=['POST', 'GET'])
def query():
    data = ''
    errors = ''
    address = ''
    command = ''
    try:
        if request.method == 'POST':
            post = request.form
            if post['address']:
                address = post['address']
            else:  
                raise ValueError('You did not send an address')
            if post['command']:
                command=request.form['command']
            else:  
                raise ValueError('You did not send a command')
        else:
            raise ValueError('Please POST an address and command')
        data = instrument_query(address, command)
    except Exception as e:
        errors = str(e)
    output = OrderedDict([('address', address), ('command', command), ('data', data), ('errors', errors)])
    return json.dumps(output)

@app.route("/close", methods=['POST', 'GET'])
def close_instrument():
    global instruments

    data = ''
    errors = ''
    address = ''
    if request.method == 'POST':
        post = request.form
        if 'address' in post:
            address = post['address']
        else:  
            raise ValueError('You did not send an address')
        try:
            if address not in instruments:
                pass
            else:
                del instruments[address]
        except Exception as e:
            errors = str(e)
        data = 'CLOSED'
    else:
        raise ValueError('please POST the address to close')
    output = OrderedDict([('address', address), ('command', 'close'), ('data', data), ('errors', errors)])
    return json.dumps(output)


### run with Flask development server ###
    
if __name__ == "__main__":
    app.run()