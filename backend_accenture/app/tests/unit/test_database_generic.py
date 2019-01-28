import unittest

from app.main.model.database_generic import DatabaseGeneric

class TestDatabaseGeneric(unittest.TestCase):
     generic = DatabaseGeneric()

     def test_connect(self):
        colection = 'pav-mongo'
        self.assertTrue(self.generic.connect(colection))