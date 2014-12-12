#!/usr/bin/env python
from flask import Flask, Response, request, json,send_file
from subprocess import check_output
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/', methods=['GET'])
def api_root():
    return 'Domas linux build server!'


@app.route('/build', methods=['POST'])
def api_post():
    data = request.get_json(force=True)
    proName = data['ProName']
    scripts = data['BuildScripts']
    buildversion = data['BuildVersion']
    out = check_output([scripts], shell = True)
    print out
    return send_file('./%s/%s/release/%s' % (buildversion, proName ,proName+'.zip'), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
