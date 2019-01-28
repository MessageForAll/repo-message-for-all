import unittest

from app.main.service.verbio_response import VerbioResponse


class TestVerbioResponse(unittest.TestCase): 

    def setUp(self):
        self.v = VerbioResponse()
        class OutboundMessage(object):
            etapa = ''
            intent = 'a'
            registrar_atendimento = ''
            flag_anatel = ''
        self.outbound_message = OutboundMessage()
        self.date = '11/12/2011 11:12:00'
        self.number = '12'
        self.phone_number = '112'
        self.transcript = '<telefone>'
        self.audio_id = 'telefone'
        self.empty_protocolo = False
    def test_next_step(self):
        self.outbound_message.etapa = "transferir"
        self.assertEqual(self.v.next_step(self.outbound_message), 'transfer')
        self.outbound_message.etapa = "finalizar"
        self.assertEqual(self.v.next_step(self.outbound_message), 'hang-up')
        self.outbound_message.intent = 'SolicitarProtocolo'
        self.empty_protocolo = True
        self.outbound_message.etapa = ''
        self.assertEqual(self.v.next_step(self.outbound_message), 'transfer')
        self.outbound_message.intent = 'SaberPrazo'
        self.assertEqual(self.v.next_step(self.outbound_message), 'ask')

    def test_get_region(self):
        self.assertEqual(self.v.get_region('2198989898'), 'R1')
        self.assertEqual(self.v.get_region('718909890080'), 'R1')
        self.assertEqual(self.v.get_region('6199889798'), 'R2')
        self.assertEqual(self.v.get_region('5599887767'), 'R2')

    def test_transfer_sector(self):
        phone = '2125696969'
        self.outbound_message.intent = "CancelarLinhaOuProduto"
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '2222222222')
        self.outbound_message.intent = "QuestionarConta"
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '1111111111')
        self.outbound_message.intent = ""
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '3333333333')
        phone = '6199889798'
        self.outbound_message.intent = "CancelarLinhaOuProduto"
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '5555555555')
        self.outbound_message.intent = "QuestionarConta"
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '4444444444')
        self.outbound_message.intent = ""
        self.assertEqual(self.v.transfer_sector(self.outbound_message, phone), '6666666666')

    def test_replace_variables(self):
        self.assertEqual(self.v.replace_variables('telefone'), [{'type': 'recording', 'transcript': '11', 'id': 'ID_N_11'}, {'type': 'recording', 'transcript': '2', 'id': 'ID_N_2'}])

    def test_hours_audios(self):
        self.assertEqual(self.v.hours_audios(self.date), [{'type': 'recording', 'transcript': '11', 'id': 'ID_N_11'}, {'type': 'recording', 'transcript': '12', 'id': 'ID_N_12'}])

    def test_date_audios(self):
        self.assertEqual(self.v.date_audios(self.date), [{'type': 'recording', 'transcript': '11', 'id': 'ID_N_11'}, {'type': 'recording', 'transcript': 'de', 'id': 'ID_T_DE'}, {'type': 'recording', 'transcript': 'dezembro', 'id': 'ID_M_01'}, {'type': 'recording', 'transcript': 'de', 'id': 'ID_T_DE'}, {'type': 'recording', 'transcript': '2000', 'id': 'ID_N_2000'}, {'type': 'recording', 'transcript': 'e', 'id': 'ID_T_E'}, {'type': 'recording', 'transcript': '11', 'id': 'ID_N_11'}])

    def test_numbers_audios(self):
        self.assertEqual(self.v.numbers_audios(self.number), [{'type': 'recording', 'transcript': '1', 'id': 'ID_N_1'}, {'type': 'recording', 'transcript': '2', 'id': 'ID_N_2'}])

    def test_phone_audios(self):
        self.assertEqual(self.v.phone_audios(self.phone_number), [{'type': 'recording', 'transcript': '11', 'id': 'ID_N_11'}, {'type': 'recording', 'transcript': '2', 'id': 'ID_N_2'}])

    def test_replace_variables_transcript(self):
        self.assertEqual(self.v.replace_variables_transcript(self.transcript), '112')






if __name__ == "__main__":
    unittest.main()

        