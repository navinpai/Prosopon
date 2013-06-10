import json

import flask
import requests

from personademo.visitorcollection import VisitorCollection

app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'R5e2oVAMxG4FLIo1Riz01sfIwjEeDEd1m2z1ugSh'
visitors = VisitorCollection()

@app.route('/')
def index():
    global visitors

    me = visitors.get_me()
    me.refresh()
    visitors.prune()

    return flask.render_template('index.html',
            me=me,
            visitors=visitors.all())

@app.route('/signin', methods=['POST'])
def signin():
    global visitors

    me = visitors.get_me()
    me.refresh()

    payload = flask.request.stream.read(2048)
    data = json.loads(payload)
    if data.keys() != ['assertion']:
        return flask.jsonify(
                message='POST payload contained unexpected keys.',
                status='error')
    data['audience'] = 'localhost:5000'
    response = requests.post('https://verifier.login.persona.org/verify',
            data=data, verify=True)
    if response.ok:
        verificationdata = json.loads(response.content)
        me.identify(verificationdata['email'])
        return flask.jsonify(
                identifier=verificationdata['email'],
                status='success')
    else:
        return flask.jsonify(
                message='Received invalid response from Persona verifier.',
                status='error')

    flask.abort(500)

@app.route('/signout', methods=['POST'])
def signout():
    global visitors

    me = visitors.get_me()
    me.deidentify()

    return flask.jsonify(status='success')

@app.route('/visitors')
def slashvisitors():
    global visitors

    visitors.prune()
    return flask.jsonify(
            me=flask.session.get('visitorid'),
            visitors=visitors.all(asjson=True))

if __name__ == '__main__':
    app.run()
