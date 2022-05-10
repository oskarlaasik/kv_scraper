from src import db

#dict_keys(['Tube', 'Üldpind', 'Korrus/Korruseid', 'Ehitusaasta', 'Seisukord', 'Omandivorm', 'Katastrinumber', 'Energiamärgis', 'Kulud suvel/talvel', 'Kinnistu number', 'Korruseid'])
class Appartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    floors_in_building = db.Column(db.Integer)
    build_year = db.Column(db.Integer)
    condition = db.Column(db.String(256))
    form_of_ownership = db.Column(db.String(256))
    energy_efficiency = (db.String(8))
    utilities_summer = db.Column(db.Integer)
    utilities_winter = db.Column(db.Integer)
    square_meters = db.Column(db.Float)
    price = db.Column(db.Float)

    def __init__(self, num_rooms, floor, floors_in_building, build_year, condition,
                 form_of_ownership, energy_efficiency, utilities_summer, utilities_winter, square_meters, price):
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
        self.price = price

    @staticmethod
    def create(num_rooms, floor, floors_in_building, build_year, condition, form_of_ownership, energy_efficiency,
               utilities_in_summer, utilities_in_winter, square_meters, price):  # create new appartment
        new_appartment = Appartment(num_rooms, floor, floors_in_building, build_year, condition, form_of_ownership, energy_efficiency,
               utilities_in_summer, utilities_in_winter, square_meters, price)
        db.session.add(new_appartment)
        db.session.commit()

    @staticmethod
    def get_all():  # return list of user details
        return [{'product_id': i.id, 'name': i.name, 'stock': i.stock, 'price': i.price}
                for i in Appartment.query.order_by('id').all()]
