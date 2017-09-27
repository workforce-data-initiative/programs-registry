from app import db
from flask import current_app
import jwt
from datetime import datetime, timedelta


class Organization(db.Model):
    """This class defines an organization table."""

    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    year_incorporated = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Program(db.Model):
    """This class defines the program table."""

    __tablename__ = 'program'

    program_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    services = db.Column(db.String(256))
    language = db.Column(db.String(20), default="English")
    costs = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modifed = db.Column(db.DateTime,
                             default=db.func.current_timestamp(),
                             onupdate=db.func.current_timestamp())


    def __init__(self, name, location, services, costs):
        """Initialize the program with its fields."""
        self.name = name
        self.location = location
        self.services = services
        self.costs = costs

    @staticmethod
    def get_all(program_id):
        """This method gets all the programs in the registry."""
        return Program.query.all()

    def save(self):
        """Save a program when creating or updating one."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a given program."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of the program model instance."""
        return "<Program: {} - {}>".format(self.id, self.name)
