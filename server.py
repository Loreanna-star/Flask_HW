from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from db import Session
from models import Advert
from schema import CreateAdvert, PatchAdvert, validate
from errors import HttpError, error_handler


app = Flask('app')

def get_advert(advert_id: int, session: Session):
    advert = session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, 'advert not found')
    return advert

class AdvertsView(MethodView):

    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            return jsonify({'id': advert.id, 'username': advert.username, 'title': advert.title, 'content': advert.content, 'creation_time': advert.creation_time.isoformat()})
        
    def post(self):
        json_data = request.json
        json_data = validate(CreateAdvert, json_data)
        with Session() as session:
            advert = Advert(**json_data)
            session.add(advert)
            try:                
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'Title already exists')
            return jsonify({'id': advert.id})
                

    def patch(self, advert_id: int):
        json_data = validate(PatchAdvert, request.json)
        with Session() as session:
            advert = get_advert(advert_id, session)
            for field, value in json_data.items():
                setattr(advert, field, value)
            session.add(advert)
            session.commit()
            return jsonify({'status': 'patched'})


    def delete(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            session.delete(advert)
            session.commit()
            return jsonify({'status': 'advert deleted'})


app.add_url_rule('/advert/<int:advert_id>/', view_func=AdvertsView.as_view('advert'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advert/', view_func=AdvertsView.as_view('advert_create'), methods=['POST'])

app.errorhandler(HttpError)(error_handler)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

