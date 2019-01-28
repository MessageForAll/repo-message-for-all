import unittest
import json
import importlib

from app.main.model.inbound_message import InboundMessage

class TestInboundMessage(unittest.TestCase):
    def test_check_is_instance(self):
        request_json = '{"request": {"session": "002", "transcript":"hola", "confidence":0.9, "datetime_inicio":"2018-09-21-16:25:48", "datetime_final":"201809201733", "msisdn-reclamado":"2199999999" } }'
        request = json.loads(request_json)

        inbound = InboundMessage(request=request)
        print(inbound.user_message)
        self.assertIsInstance(inbound, InboundMessage)


if __name__ == "__main__":
    unittest.main()