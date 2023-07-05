from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
import pydantic

from db import Session
from models import Advert
from schema import CreateAdvert, PatchAdvert



app = Flask('app')

def validate(input_data: dict, validation_model):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())

class HttpError(Exception):
    def __init__(self, status_code: int, description: str | dict | list):

        self.status_code = status_code
        self.description = description

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code
    return response


def get_advert(advert_id: int, session: Session):
    advert = session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, 'advert not found')
    return advert

class AdvertsView(MethodView):

    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            return jsonify({'id': advert.id, 'username': advert.username, 'content': advert.content, 'creation_time': advert.creation_time.isoformat()})
        
    def post(self):
        json_data = request.json
        json_data = validate(json_data, CreateAdvert)
        with Session() as session:
            advert = Advert(**json_data)
            session.add(advert)
            try:                
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'Title already exists')
            return jsonify({'id': advert.id})
                

    def patch(self, advert_id: int):
        json_data = validate(request.json, PatchAdvert)
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

