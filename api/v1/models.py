# -*- coding: utf-8 -*-

from app.app import db


class QueryObject(object):
    def save(self):
        """Save program registry table object."""
        
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete program registry table object."""
        
        db.session.delete(self)
        db.session.commit()


class Organization(db.Model, QueryObject):
    """This class defines an organization table."""

    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    year_incorporated = db.Column(db.DateTime, nullable=True)

    programs = db.relationship("Program", backref="organization", 
                               lazy=True, passive_deletes=True)
    locations = db.relationship("Location", backref="organization", 
                                lazy=True,passive_deletes=True)
    services = db.relationship("Service", backref="organization", 
                               lazy=True, passive_deletes=True)

    def __init__(self, name, description, email=None, url=None,
                 year_incorporated=None):
        self.name = name
        self.description = description
        self.email = email
        self.url = url
        self.year_incorporated = year_incorporated 

    def __repr__(self):
        """Return a representation of the model instance."""
        
        return "<Organization: {}, {}>".format(self.id, self.name)


class Program(db.Model, QueryObject):
    """This class defines the program table."""

    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)
    cip = db.Column(db.Integer, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id,
                                                          ondelete='CASCADE'))
    name = db.Column(db.String(100), nullable=False)
    alternate_name = db.Column(db.String(100), nullable=True)
    on_etpl = db.Column(db.String(10), default='N/A', nullable=False)
    
    services = db.relationship("Service", backref="program", 
                               lazy=True, passive_deletes=True)

    def __init__(self, cip, name, organization_id, alternate_name=None, on_etpl=0):
        """Initialize the program with its fields."""
        
        self.cip = cip
        self.organization_id = organization_id
        self.name = name
        self.alternate_name = alternate_name
        self.on_etpl = on_etpl 

    def __repr__(self):
        """Return a representation of the program model instance."""
        
        return "<Program: {}, {}, {}>".format(self.id, self.cip, self.name)


service_location = db.Table('service_location', 
                            db.Column('service_id', db.Integer, db.ForeignKey('service.id')),
                            db.Column('location_id', db.Integer, db.ForeignKey('location.id')) )


class Service(db.Model, QueryObject):
    """This class represents a service table."""

    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id,
                                                          ondelete='CASCADE'))
    program_id = db.Column(db.Integer,
                           db.ForeignKey(Program.id, ondelete='CASCADE'),
                           nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(10), nullable=True)
    fees = db.Column(db.String(10), nullable=True)
    
    def __init__(self, name, organization_id, program_id=None, status=None,
                 fees=None, email=None, url=None):
        """Initialize the service with its fields."""
        self.name = name
        self.organization_id = organization_id
        self.program_id = program_id
        self.email = email
        self.status = status
        self.fees = fees
        self.url = url

    def __repr__(self):
        """Return a representation of the service model instance."""
        
        return "<Service: {}, {}>".format(self.id, self.name)


class Location(db.Model, QueryObject):
    """This class defines a location model."""

    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id,
                                                          ondelete="CASCADE"))
    alternate_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    transportation = db.Column(db.String(256), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    address = db.relationship("PhysicalAddress", backref="location", lazy=True,
                              uselist=False, passive_deletes=True)
    services = db.relationship("Service", secondary=service_location, lazy='subquery',
                               backref=db.backref("locations", lazy=True))
    
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

    def __repr__(self):
        """Return a representation of the model instance."""
        
        return "<Location: {}, {}>".format(self.id, self.name)


class PhysicalAddress(db.Model, QueryObject):
    """This class defines a representation of the physical address model."""

    __tablename__ = "physical_address"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id,
                                                      ondelete='CASCADE'))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False)  # 2-letter country code
    
    def __repr__(self):
        """Return a representation of the model instance."""
        
        return "<Address: {}, {}, {} {}, {}".format(self.address, self.city, self.state,
                                                    self.postal_code, self.country)