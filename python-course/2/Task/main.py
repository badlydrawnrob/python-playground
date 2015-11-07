from flask import Flask, render_template, url_for, jsonify
from support import get_name, get_description


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def root():
    #Send out the index.html file (our main file)
    return render_template('index.html')


#The route below is so we can request the data about a room
@app.route('/room/<int:room_id>')
def get_room(room_id):

    #Print out the variable passed in
    print(room_id)

    #We need to feed back actual information
    #Not just the current generic data
    cur_room = {
        'name': get_name(room_id),
        'description': get_description(room_id),
        'image': url_for('static', filename='img/{}.jpg'.format(room_id))
    }

    #Return the above Python object but convert it to JSON first
    return jsonify(**cur_room)


# The following runs automatically when you run the file (in this case starting the server)
if __name__ == '__main__':
    #Setting debug to True shows us more information when an error is thrown
    app.debug = True
    app.run()
