# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from __future__ import print_function
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from flasktestapp.database import db
from flasktestapp.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session
        force_flush = True


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True
    is_admin = False

    class Meta:
        """Factory configuration."""

        model = User


from flasktestapp.feature import models


class ClientFactory(BaseFactory):

    name = Sequence(lambda n: 'client{0}'.format(n))

    class Meta:
        model = models.Client


class ClientUserFactory(BaseFactory):
    class Meta:
        model = models.ClientUser


class ProjectFactory(BaseFactory):

    name = Sequence(lambda n: 'project {0}'.format(n))

    class Meta:
        model = models.Project


class ProductAreaFactory(BaseFactory):
    name = Sequence(lambda n: 'productArea{}'.format(n))

    class Meta:
        model = models.ProductArea

    @classmethod
    def create_defaults(cls):
        objs = []
        for name in models.ProductArea.DEFAULT_PRODUCT_AREAS:
            objs.append(cls(name=name))
        return objs


class FeatureFactory(BaseFactory):

    class Meta:
        model = models.Feature

    name = Sequence(lambda n: 'feature {}'.format(n))


def load_factories():
    admin = UserFactory.create(
        username='admin',
        password='password',
        is_admin=True)
    client = ClientFactory.create(name='clientABC', users=[admin])
    client.users.append(admin)  # TODO
    project = ProjectFactory.create(
        name='projectA',
        client_id=client.id)
    product_areas = ProductAreaFactory.create_defaults()
    feature = FeatureFactory.create(
        name='featureA',
        project_id=project.id,
        product_area_id=product_areas[0].id,
        user=admin)
    import collections
    data = collections.OrderedDict()
    data['users'] = [admin]
    data['clients'] = [client]
    data['projects'] = [project]
    data['product_areas'] = product_areas
    data['features'] = [feature]
    return data


if __name__ == "__main__":
    import sys
    try:
        data = load_factories()
        print(data)
        sys.exit(0)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
