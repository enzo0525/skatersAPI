from flask import Flask, request, redirect, jsonify
from database import search_for_skater

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/api/v1/skateboarders/')

@app.route('/api/v1/skateboarders/', methods=['GET'])
def skateboarders():
    params = {
        'fName': request.args.get('fname', None),
        'lName': request.args.get('lname', None),
        'age': request.args.get('age', None),
        'dateOfBirth': request.args.get('dateofbirth', None),
        'gender': request.args.get('gender', None),
        'from': request.args.get('from', None),
        'sponsors': request.args.get('sponsors', None),
        'stance': request.args.get('stance', None),
        'globalRanking': request.args.get('globalranking', None),
        'earnings': request.args.get('earnings', None)
    }

    query = {
        key: {'$regex': f'^{value}$', '$options': 'i'} if key in ['fName', 'lName', 'gender', 'from', 'sponsors', 'stance'] else (int(value) if key in ['age', 'globalRanking', 'earnings'] else value)
        for key, value in params.items() if value
    }

    data = search_for_skater(query)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)