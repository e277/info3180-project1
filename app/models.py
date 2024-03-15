from . import db


class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    noOfRooms = db.Column(db.Integer)
    noOfBathrooms = db.Column(db.Integer)
    price = db.Column(db.Float())
    propertyType = db.Column(db.String(100))
    location = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    
    def __init__(self, title, description, noOfRooms, noOfBathrooms, price, propertyType, location, photo):
        self.title = title
        self.description = description
        self.noOfRooms = noOfRooms
        self.noOfBathrooms = noOfBathrooms
        self.price = price
        self.propertyType = propertyType
        self.location = location
        self.photo = photo