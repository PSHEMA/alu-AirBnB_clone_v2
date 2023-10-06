#!/usr/bin/python3
"""dbStorage Unittest"""

import unittest
import models
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class."""

    def setUp(self):
        """Set up test environment."""
        self.storage = models.storage

    def tearDown(self):
        """Remove storage file at the end of tests."""
        self.storage.close()

    def test_user(self):
        """Test saving and retrieving a User object."""
        user = User(name="Chyna", email="chyna1@gmail.com", password="Chyna12345")
        user.save()
        self.assertTrue(user.id in self.storage.all())
        self.assertEqual(user.name, "Chyna")

    def test_city(self):
        """Test saving and retrieving a City object."""
        state = State(name="California")
        state.save()
        city = City(name="Batch")
        city.state_id = state.id
        city.save()
        self.assertTrue(city.id in self.storage.all())
        self.assertEqual(city.name, "Batch")

    def test_state(self):
        """Test saving and retrieving a State object."""
        state = State(name="California1")
        state.save()
        self.assertTrue(state.id in self.storage.all())
        self.assertEqual(state.name, "California1")

    def test_place(self):
        """Test saving and retrieving a Place object."""
        state = State(name="California2")
        state.save()

        city = City(name="Batch2")
        city.state_id = state.id
        city.save()

        user = User(name="Chyna2", email="chyna2@gmail.com", password="Chyna12345")
        user.save()

        place = Place(name="Palace2", number_rooms=4)
        place.city_id = city.id
        place.user_id = user.id
        place.save()

        self.assertTrue(place.id in self.storage.all())
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.name, "Palace2")

    def test_amenity(self):
        """Test saving and retrieving an Amenity object."""
        amenity = Amenity(name="Startlink3")
        amenity.save()
        self.assertTrue(amenity.id in self.storage.all())
        self.assertEqual(amenity.name, "Startlink3")

    def test_review(self):
        """Test saving and retrieving a Review object."""
        state = State(name="California3")
        state.save()

        city = City(name="Batch3")
        city.state_id = state.id
        city.save()

        user = User(name="Chyna3", email="chyna3@gmail.com", password="Chyna12345")
        user.save()

        place = Place(name="Palace3", number_rooms=4)
        place.city_id = city.id
        place.user_id = user.id
        place.save()

        review = Review(text="no comment3", place_id=place.id, user_id=user.id)
        review.save()

        self.assertTrue(review.id in self.storage.all())
        self.assertEqual(review.text, "no comment3")

if __name__ == '__main__':
    unittest.main()
