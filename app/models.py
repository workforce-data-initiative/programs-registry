from app import db
from flask import current_app
import jwt
from datetime import datetime, timedelta


class Organization(db.Model):
    """This class defines an organization table."""

    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    year_incorporated = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, description, email=None, url=None,
                 year_incorporated=None):
        self.name = name
        self.description = description
        self.email = email
        self.url = url
        self.year_incorporated = year_incorporated

    def save(self):
        """Save an organization when creating or updating one."""
        db.session.add(self)
        db.session.commit()

    def get_all():
        """Return all the organizations."""
        return Organization.query.all()

    def __repr__(self):
        """Return a representation of the model instance."""
        return "{}: {}".format(self.id, self.name)


class Program(db.Model):
    """This class defines the program table."""

    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id))
    name = db.Column(db.String(100), nullable=False)
    alternate_name = db.Column(db.String(100), nullable=True)

    def __init__(self, name, organization_id, alternate_name=None):
        """Initialize the program with its fields."""
        self.organization_id = organization_id
        self.name = name
        self.alternate_name = alternate_name

    @staticmethod
    def get_all():
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


class Service(db.Model):
    """This class represents a service table."""

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id))
    program_id = db.Column(db.Integer, db.ForeignKey(Program.id))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(10), nullable=True)
    fees = db.Column(db.String(10), nullable=True)

    def __init__(self, name, organization_id, program_id=None, status=None,
                 fees=None):
        """Initialize the service with its fields."""
        self.name = name
        self.organization_id = organization_id
        self.program_id = program_id
        self.status = status
        self.fees = fees

    @staticmethod
    def get_all(organization_id):
        """This method gets all the services for a given organization."""
        return Service.query.filter_by(organization_id=organization_id)

    def save(self):
        """Save a program when creating or updating one."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a given program."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return a representation of the service model instance."""
        return "<Service: {} - {}>".format(self.id, self.name)


class Location(db.Model):
    """This class defines a location model."""

    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id))
    alternate_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable = True)
    transportation = db.Column(db.String(256), nullable=True)
    latitude = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Integer, nullable=True)

    def __init__(self, name, organization_id, alternate_name=None,
                 description=None, transportation=None, latitude=None,
                 longitude=None):
        """Initialize location object with its fields."""
        self.name = name
        self.organization_id = organization_id
        self.alternate_name = alternate_name
        self.description = description
        self.transportation = transportation
        self.latitude = latitude
        self.longitude = longitude

    def save(self):
        """Save a location when creating a new one."""
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_all(organization_id):
        """Return all the locations for a given organization."""
        return Location.query.filter_by(organization_id=organization_id)

    def __repr__(self):
        """Return a representation of the model instance."""
        return "{}: {}".format(self.id, self.name)


class ServiceLocation(db.Model):
    """This class defines a representation of the service at location table."""

    __tablename__ = "service_location"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey(Service.id))
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, service_id, location_id, description=None):
        """Initialize location object with its fields."""
        self.service_id = service_id
        self.location_id = location_id

    @staticmethod
    def get_all(service_id):
        """Get all the location ids for a given service."""
        return ServiceLocation.query.filter_by(service_id=service_id)

    def __repr__(self):
        """Return a representation of the model instance."""
        return "{}".format(self.id)



class PhysicalAddress(db.Model):
    """This class defines a representation of the physical address model."""

    __tablename__ = "physical_address"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False) # Two-letter country code

    def save(self):
        """Save the instance of the physical address."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(location_id):
        """Get the physical address given the location."""
        return PhysicalAddress.query.filter_by(location_id=location_id)

    def __repr__(self):
        """Return a representation of the model instance."""
        return "{}: {}, {} {}".format(self.id, self.address, self.city,
                                      self.postal_code)




