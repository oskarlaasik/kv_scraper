from src import db


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    floors_in_building = db.Column(db.Integer)
    build_year = db.Column(db.Integer)
    condition = db.Column(db.String(256))
    form_of_ownership = db.Column(db.String(256))
    energy_efficiency = db.Column(db.String(64))
    utilities_summer = db.Column(db.Integer)
    utilities_winter = db.Column(db.Integer)
    square_meters = db.Column(db.Float)
    square_meter_price = db.Column(db.Integer)
    price = db.Column(db.Integer)
    address = db.Column(db.String(256))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.id'))
    kv_id = db.Column(db.Integer)

    def __init__(self, num_rooms, floor, floors_in_building, build_year, condition, form_of_ownership,
                 energy_efficiency, utilities_summer, utilities_winter, square_meters, square_meter_price, price,
                 longitude, latitude, address, broker_id, kv_id):
        self.num_rooms = num_rooms
        self.floor = floor
        self.floors_in_building = floors_in_building
        self.build_year = build_year
        self.condition = condition
        self.form_of_ownership = form_of_ownership
        self.energy_efficiency = energy_efficiency
        self.utilities_summer = utilities_summer
        self.utilities_winter = utilities_winter
        self.square_meters = square_meters
        self.square_meter_price = square_meter_price
        self.price = price
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.broker_id = broker_id
        self.kv_id = kv_id

    @staticmethod
    def create(num_rooms, floor, floors_in_building, build_year, condition, form_of_ownership, energy_efficiency,
               utilities_summer, utilities_winter, square_meters, square_meter_price, price, address, longitude,
               latitude, broker_id, kv_id):  # create new apartment
        new_apartment = Apartment(num_rooms, floor, floors_in_building, build_year, condition, form_of_ownership,
                                  energy_efficiency, utilities_summer, utilities_winter, square_meters,
                                  square_meter_price, price, longitude, latitude, address, broker_id, kv_id)
        db.session.add(new_apartment)
        db.session.commit()


class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    company = db.Column(db.String(256))
    apartment = db.relationship('Apartment')

    def __init__(self, name, company):
        self.name = name
        self.company = company

    @staticmethod
    def create(name, company):  # create new broker
        new_broker = Broker(name, company)
        db.session.add(new_broker)
        db.session.commit()
