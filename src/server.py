#!/usr/bin/env python3

from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
import re
from datetime import datetime
from constants import DB_URI, EMAIL_REGEX

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
class books(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   title = db.Column(db.String(100))
   available = db.Column(db.Boolean)
   timestamp = db.Column(db.String(20))

   def __init__(self, title, available, timestamp):
      self.title = title
      self.available = available
      self.timestamp = timestamp

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, books):
            return {
                'id': obj.id,
                'title': obj.title,
                'available': str(obj.available),
                'timestamp': obj.timestamp
            }
        return super(MyJSONEncoder, self).default(obj)
app.json_encoder = MyJSONEncoder

@app.route('/request', methods=['GET', 'POST', 'DELETE'])
def get_requests():
    if (request.method == 'GET'):
        request_id = request.args.get('id')
        if (request_id is None):
            return jsonify(books.query.all())
        else:
            return jsonify(books.query.filter_by(id = request_id).all())
    if (request.method == 'POST'):
        email = request.json['email']
        if (re.search(EMAIL_REGEX, email)):
            title = request.json['title']
            requested_book = books.query.filter_by(title = title).first()
        else:
            return "Invalid email", 400
        if (requested_book is None):
            return "Book not found", 404
        else:
            response = jsonify(requested_book)
            requested_book.available = False
            requested_book.timestamp = datetime.now().isoformat()
            db.session.commit()
            return response
    if (request.method == 'DELETE'):
        request_id = request.args.get('id')
        if (request_id is None):
            return "Must specify an id to delete", 400
        else:
            request_to_delete = books.query.filter_by(id = request_id).first()
            request_to_delete.available = True
            request_to_delete.timestamp = None
            db.session.commit()
            return {}, 200

if __name__ == '__main__':
    db.create_all()

    titles = ['Gods of the Upper Air', 'Inherent Vice', 'The Count of Monte Cristo',
    'A Tale of Two Cities', 'Culture Warlords', 'East of Eden', 'Crime and Punishment',
    'Gravitys Rainbow', 'Naked Lunch', 'Pride and Prejudice']
    for title in titles:
        exists = books.query.filter_by(title = title).first()
        if (exists is None):
            db.session.add(books(title, True, None))

    db.session.commit()

    app.run(debug = True)
