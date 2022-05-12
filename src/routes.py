from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import func

from src import db
from src.models import Apartment, Broker

api_bp = Blueprint('api', __name__)


def parse_page_size(query_parameters):
    page_num = query_parameters.get('page_num')
    page_size = query_parameters.get('page_size')
    if page_num:
        try:
            page_num = int(page_num)
        except Exception as e:
            return jsonify(error=400, text=str(e))
    else:
        page_num = 1

    if page_size:
        try:
            page_size = int(page_size)
        except Exception as e:
            return jsonify(error=400, text=str(e))
    else:
        page_size = 100
    return page_num, page_size


@api_bp.route('/api')
def api():
    return render_template('documentation.html')


@api_bp.route('/api/apartments/all')
def apartments():
    page_num, page_size = parse_page_size(request.args)

    results = Apartment.query.paginate(page_num, page_size).items
    results = [{'num_rooms': i.num_rooms,
                'price': i.price,
                'address': i.address,
                'floor': i.floor,
                'floors_in_building': i.floors_in_building,
                'build_year': i.build_year,
                'condition': i.condition,
                'energy_efficiency': i.energy_efficiency,
                'utilities_summer': i.utilities_summer,
                'utilities_winter': i.utilities_winter,
                'square_meters': i.square_meters,
                'longitude': i.longitude,
                'latitude': i.latitude,
                'broker_id': i.broker_id,
                'kv_id': i.kv_id,
                'form_of_ownership': i.form_of_ownership}
               for i in results]

    return jsonify(results)


@api_bp.route('/api/brokers/all')
def brokers():
    page_num, page_size = parse_page_size(request.args)

    results = Broker.query.paginate(page_num, page_size).items
    results = [{'name': i.name, 'company': i.company} for i in results]

    return jsonify(results)


@api_bp.route('/api/brokers/all/arrange')
def brokers_arrange():
    query_parameters = request.args
    arrange = query_parameters.get('arrange')
    if not arrange and arrange != 'asc' and arrange != 'desc':
        return jsonify(error=400, text='arrange variable not specified')

    page_num, page_size = parse_page_size(request.args)

    avg_meter_price = func.avg(Apartment.square_meter_price)
    result = db.session.query(avg_meter_price, Broker.id, Broker.name, Broker.company).filter(
        Apartment.broker_id == Broker.id).group_by(Broker.id)

    if arrange == 'desc':
        result = result.order_by(avg_meter_price.desc())
    else:
        result = result.order_by(avg_meter_price.asc())
    results = result.paginate(page_num, page_size).items
    results = [{'average_square_meter_price': i[0], 'name': i[2], 'company': i[1]} for i in results]

    return jsonify(results)
