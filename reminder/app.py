from flask import Flask, abort, jsonify, make_response, request

app = Flask(__name__)

reminders = [
    {
        'id': 1,
        'title': u'Buy Groceries',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'done': True
    }
]


@app.route('/api/v1/reminders', methods=['GET'])
def get_reminders():
    return jsonify({'reminders': reminders})


@app.route('/api/v1/reminders/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id: int):
    reminder = __get_reminder_by_id(reminder_id)

    if(len(reminder) == 0):
        abort(404)

    return jsonify({'reminder': reminder[0]})


@app.route('/api/v1/reminders', methods=['POST'])
def create_reminder():
    if not request.json or not 'title' in request.json:
        abort(400)

    reminder = {
        'id': reminders[-1]['id'] + 1,
        'title': request.json['title'],
        'done': False
    }

    reminders.append(reminder)

    return jsonify({'reminder': reminder}), 201


@app.route('/api/v1/reminders', methods=['PUT'])
def update_reminder():
    if not request.json or not 'id' in request.json or not 'title' in request.json:
        abort(400)

    reminder = __get_reminder_by_id(request.json['id'])

    if len(reminder) == 0:
        abort(400)

    reminder[0]['title'] = request.json.get('title', reminder[0]['title'])
    reminder[0]['done'] = request.json.get('done', reminder[0]['done'])

    return jsonify({'reminder': reminder[0]})


def __get_reminder_by_id(id: int):
    reminder = [reminder for reminder in reminders if reminder['id'] == id]

    return reminder


@app.route('/api/v1/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id: int):
    reminder = [
        reminder for reminder in reminders if reminder['id'] == reminder_id]

    if len(reminder) == 0:
        abort(404)

    reminders.remove(reminder[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
