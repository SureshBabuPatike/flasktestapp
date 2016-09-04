# -*- coding: utf-8 -*-
"""Model unit tests."""

import datetime as dt
import unittest
import pprint

import pytest

from flasktestapp.user.models import Role, User
from flasktestapp.feature.models import (
    Client,
    ClientUser,
    Project,
    ProductArea,
    Feature,
)

# from flasktestapp import factories
from flasktestapp.factories import (
    UserFactory,
    ClientFactory,
    # ClientUserFactory,
    ProjectFactory,
    ProductAreaFactory,
    FeatureFactory,
    load_factories,
)


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles


@pytest.mark.usefixtures('db')
class TestFactories(unittest.TestCase):
    def test_load_factories(self):
        data = load_factories()
        self.assertTrue(len(data))
        self.assertIn('users', data)
        self.assertIn('clients', data)
        self.assertIn('projects', data)
        self.assertIn('product_areas', data)
        self.assertIn('features', data)

    def test_one(self):
        data = load_factories()
        userA = UserFactory.create(username='userABC', password='password')
        userB = UserFactory.create(username='userBCD', password='password')
        client = ClientFactory.create(name='clientXYZ', users=[userA])
        client.users.append(userB)
        print(client)
        # product_areas = ProductAreaFactory.create_defaults()
        product_areas = data['product_areas']
        projectA = ProjectFactory.create(name="projectABC", client=client)
        featureA = FeatureFactory.create(name='featureABC',
                                         user=userA,
                                         project=projectA,
                                         product_area=product_areas[-1])
        print(featureA)

        data['users'].extend([userA, userB])
        data['clients'].extend([client])
        data['projects'].extend([projectA])
        data['features'].extend([featureA])

        data['users'].extend(UserFactory.create_batch(10))
        data['clients'].extend(ClientFactory.create_batch(10))
        data['product_areas'].extend(ProductAreaFactory.create_batch(10))

        # data['projects'].extend(ProjectFactory.create_batch(10))
        for project in data['projects'][:-1]:
            data['features'].extend(FeatureFactory.create_batch(2,
                                                                user=userA, # TODO
                                                                project=project))
        print(pprint.pformat(data.items()))
        raise Exception()
