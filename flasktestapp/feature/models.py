# -*- coding: utf-8 -*-
"""User models."""

from flasktestapp.database import Column, Model, SurrogatePK, db, reference_col, relationship

from sqlalchemy.ext.orderinglist import ordering_list


class Client(SurrogatePK, Model):
    """A client"""
    __tablename__ = 'clients'
    name = Column(db.String(255), unique=True, nullable=False)
    users = relationship('User',
                         secondary='client_users')


class ClientUser(SurrogatePK, Model):
    __tablename__ = 'client_users'
    client_id = reference_col('clients', nullable=False)
    client = relationship('Client', backref='client_users')

    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='clients')

    def __repr__(self):
        return '<ClientUser({},{}>'.format(self.client_id, self.user_id)


class Project(SurrogatePK, Model):
    """A project for a client"""
    __tablename__ = 'projects'
    name = Column(db.String(255), unique=True, nullable=False)
    client_id = reference_col('clients', nullable=False)
    client = relationship('Client', backref='projects')

    features = relationship('Feature',
                            backref='project',
                            # secondary='features',
                            primaryjoin='projects.c.id == features.c.project_id',
                            order_by='features.c.client_priority',
                            collection_class=ordering_list('client_priority'))

    # def __init__(self, **kwargs):
    #     """Create instance"""
    #     db.Model.__init__(self, name=kwargs['name'],
    #                       client_id=kwargs['client_id'])

    def __repr__(self):
        return '<Project({}, {})>'.format(self.name, self.client_id)


class ProductArea(SurrogatePK, Model):
    """A product area"""
    __tablename__ = 'product_areas'
    name = Column(db.String(255), unique=True, nullable=False)

    DEFAULT_PRODUCT_AREAS = ['Policies', 'Billing', 'Claims', 'Reports']

    def __init__(self, **kwargs):
        """Create instance"""
        db.Model.__init__(self, name=kwargs['name'])


class Feature(SurrogatePK, Model):
    """A feature for a Project"""
    __tablename__ = 'features'
    __table_args__ = (db.UniqueConstraint('project_id', 'client_priority'),
                      {})

    name = Column(db.String(255), unique=True, nullable=False)
    description = Column(db.Text(), nullable=True)

    client_priority = Column(db.Integer(), nullable=True)

    target_date = Column(db.DateTime, nullable=True)

    ticket_url = Column(db.Text(), nullable=True)

    project_id = reference_col('projects', nullable=False)
    # project = relationship('Project',
    #                        backref='features',
    #                        )

    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='features')

    product_area_id = reference_col('product_areas', nullable=True)
    product_area = relationship('ProductArea', backref='features')

    @property  # TODO: sqlalchemy property ref
    def title(self):
        return self.name

    def __repr__(self):
        return '<Feature({}, {})>'.format(self.name, self.project_id)
