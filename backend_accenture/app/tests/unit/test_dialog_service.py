import unittest
import json

from app.main.service.dialog_service import DialogService

class TestDialogService(unittest.TestCase):
    dialog = DialogService()

    def setUp(self):
        class OutboundMessage(object):
            output_text = ["Teste dialog service"]
            watson_times_response = ""
            conversation_id = "test_dialog_service"
            etapa = ''
            intent = ''
        
        class Context(object):
            context_watson = {"test": "dialog_service"}
            conversation_id = "test_dialog_service"

        class InboundMessage(object):
            user_message = 'Input dialog service test'
            session_verbio = "test_dialog_service"

        self.outbound_message = OutboundMessage()
        self.inbound_message = InboundMessage()
        self.context = Context()


    def test__build_answer__(self):
        answer = json.loads(self.dialog.__build_answer__(self.outbound_message)[0])
        print(answer)
        self.assertEqual(answer["answer"]["session"], "test_dialog_service")
        self.assertEqual(answer["answer"]["next"], "ask")

    def test__create_outbound_message__(self):
        utter = "New output text"
        outbound_message = self.dialog.__create_outbound_message__(utter, self.context)
        self.assertEqual(outbound_message.output_text, ["New output text"])
        self.assertEqual(outbound_message.context, {"test": "dialog_service"})

    def test__check_silence__(self):
        silence = self.dialog.__check_silence__(self.inbound_message, self.context)
        self.assertEqual(silence[0], False)
        self.assertEqual(silence[1], None)
        self.inbound_message.user_message = ''
        silence = self.dialog.__check_silence__(self.inbound_message, self.context)
        self.assertEqual(silence[0], True)








