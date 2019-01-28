import unittest

from app.main.model.event import Event

class TestEvent(unittest.TestCase):
    evento = Event()

    def setUp(self):
        self.cci_teste = '{"idOrdem": 3456, "idEventRec": 1, "eventNumber": "4733-09-2016", "forecastDate": "2016-09-13T00:47:48-03:00", "initialDate": "2016-09-12T18:47:48-03:00", "endDate": "31/07/2016", "requestDateREC": "2016-10-10T14:06:28-03:00","resultDateREC": "2016-10-10T14:06:28-03:00", "descrEventType": "EXISTE EVENTO DE INTERRUPCAO NAO PROGRAMADA","result": "OK", "msg": "Sucesso"}'

    def test_fill(self):
        self.evento.fill(self.cci_teste)
        self.assertEqual(self.evento.id_ordem, 3456)
        self.assertEqual(self.evento.descr_event_type, "EXISTE EVENTO DE INTERRUPCAO NAO PROGRAMADA")
        self.assertEqual(self.evento.event_number, "4733-09-2016")
