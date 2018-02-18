# from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pavitra24@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class TinyWebDB(db.Model):
    tag = db.Column(db.String, primary_key=True, nullable=False)
    value = db.Column(db.String, nullable=False)
    # The 'date' column is needed for deleting older entries, so not really required
    # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/storeavalue', methods=['POST'])
def store_a_value():
    tag = request.args.get('tag', '')
    value = request.args.get('value')
    if tag:
        # Prevent Duplicate Key error by updating the existing tag
        existing_tag = TinyWebDB.query.filter_by(tag=tag).first()
        if existing_tag:
            existing_tag.value = value
        else:
            data = TinyWebDB(tag=tag, value=value)
            db.session.add(data)
            db.session.commit()
        return jsonify(['STORED', tag, value])
    return 'Enter a valid tag!'


@app.route('/getvalue', methods=['POST'])
def get_value():
    tag = request.args.get('tag', '')
    if tag:
        value = TinyWebDB.query.filter_by(tag=tag).first().value
        return jsonify(['VALUE', tag, value])


@app.route('/deleteentry')
def delete_entry():
    return 'Not implemented!'


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
