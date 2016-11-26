from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello_world'

@app.route('/saysomething')
def something_else():
    return 'We are now saying something else'

@app.route('/passval/<new_val>')
def get_value(new_val):
    return 'You requested the '+ new_val + ' resource'

if __name__ == '__main__':
    app.debug = True
    app.run()
