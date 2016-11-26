#This code is a possible solution for the coding problem
@app.route('/room/<path:room_id>')
def get_room(room_id):
    img = 'img/' + room_id + '.jpg'
    cur_room = {
        'name': get_name(int(room_id)), 
        'description': get_description(int(room_id)),
        'image': img}
    return jsonify(**cur_room)