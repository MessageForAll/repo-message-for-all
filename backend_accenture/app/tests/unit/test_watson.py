import unittest

from app.main.service.nlu.watson import Watson

class TestWatson(unittest.TestCase):
    watson = Watson()

    def setUp(self):
        self.response =  {'intents': [{'intent': 'greet', 'confidence': 1}], 'entities': [], 'input': {'text': 'hola'}, 'output': {'generic': [{'response_type': 'text', 'text': 'Boa noite, sou a técnica virtual Mári. Com quem falo?'}], 'text': ['Boa noite, sou a técnica virtual Mári. Com quem falo?'], 'nodes_visited': ['Bem-vindo', 'node_11_1532701072565'], 'times': [{'max': '300', 'silence': '30', 'interval': '5'}], 'log_messages': []}, 'context': {'conversation_id': '002', 'timezone': 'America/Sao_Paulo', 'chamada_valida': '', 'time': '2018-10-18T22:32:18.545300', 'repetida': '', 'name': '', 'etapa': 'welcome', 'system': {'initialized': True, 'dialog_stack': [{'dialog_node': 'root'}], 'dialog_turn_counter': 1, 'dialog_request_counter': 1, '_node_output_map': {'node_11_1532701072565': {'0': [0, 0, 1]}}, 'branch_exited': True, 'branch_exited_reason': 'completed'}, 'rpt': 0, 'servico': 'internet', 'saudacao': 'Boa noite', 'evento_fixo': 'N', 'evento_velox': 'S', 'rpt_silencio': 0, 'rpt_improperio': 0, 'rpt_not_motivo': 0, 'hr_normalizacao': 'sete horas da noite', 'chamada_repetida': 'N', 'data_normalizacao': 'hoje', 'rpt_visitatecnica': 0}}
        class OutboundMessage(dict):
            intent = ''
            etapa = ''
            watson_confidence = ''
            watson_response = ''
            output_text = ''
            context = ''
            watson_times_response = ''
            intervalo_confianca = ''
            flag_anatel = ''
            registrar_atendimento = ''

        class Context(object):
            context_watson = {"context_test": "test"}

            def get_json(self):
                context_chamada_j = {}
                context_chamada_j["context_watson"] = str(self.context_watson)
                return context_chamada_j
        
        class InboundMessage(object):
            msisdn_reclamado = "test_watson"
            user_message = "hola"
            session_verbio = "test_watson"

        self.outbound_message  = OutboundMessage()
        self.context = Context()
        self.inbound_message = InboundMessage()

    def test_set_flag_anatel(self):
        self.outbound_message.etapa = "welcome"
        self.watson.set_flag_anatel(self.outbound_message, self.context)
        self.assertEqual(self.outbound_message.flag_anatel, "")
        self.outbound_message.etapa = ""
        self.outbound_message.intent = "AmeacarAnatel"
        self.watson.set_flag_anatel(self.outbound_message, self.context)
        self.assertEqual(self.outbound_message.flag_anatel, 'Y')

    def test_set_registrar_chamada(self):
        self.outbound_message.etapa = "welcome"
        self.watson.set_registrar_chamada(self.outbound_message, self.inbound_message, self.context)
        self.assertEqual(self.outbound_message.registrar_atendimento, '')
        self.outbound_message.etapa = "evento"
        self.watson.set_registrar_chamada(self.outbound_message, self.inbound_message, self.context)
        self.assertEqual(self.outbound_message.registrar_atendimento, 'Y')

    def test__create_outbound_message__(self):
        self.outbound_message = self.watson.__create_outbound_message__(self.response)
        self.assertEqual(self.outbound_message.intent, "greet")
        self.assertEqual(self.outbound_message.watson_confidence, 1)
        self.assertEqual(self.outbound_message.output_text, ["Boa noite, sou a técnica virtual Mári. Com quem falo?"])

    def test__change_answer_and_context__(self):
        answer = "answer test watson"
        response_changed = self.watson.__change_answer_and_context__(self.response, answer)
        self.assertEqual(response_changed["output"]["text"], ["Boa noite, sou a técnica virtual Mári. Com quem falo?", "answer test watson"])
        self.assertEqual(response_changed["context"], {'conversation_id': '002', 'timezone': 'America/Sao_Paulo', 'chamada_valida': '', 'time': '2018-10-18T22:32:18.545300', 'repetida': '', 'name': '', 'etapa': 'welcome', 'system': {'initialized': True, 'dialog_stack': [{'dialog_node': 'root'}], 'dialog_turn_counter': 1, 'dialog_request_counter': 1, '_node_output_map': {'node_11_1532701072565': {'0': [0, 0, 1]}}, 'branch_exited': True, 'branch_exited_reason': 'completed'}, 'rpt': 0, 'servico': 'internet', 'saudacao': 'Boa noite', 'evento_fixo': 'N', 'evento_velox': 'S', 'rpt_silencio': 0, 'rpt_improperio': 0, 'rpt_not_motivo': 0, 'hr_normalizacao': 'sete horas da noite', 'chamada_repetida': 'N', 'data_normalizacao': 'hoje', 'rpt_visitatecnica': 0})

    def test__check_intent_confidence__(self):
        etapa_anterior = ''
        response_changed = self.watson.__check_intent_confidence__(self.response, self.context, etapa_anterior)
        self.assertEqual(response_changed["intervalo_confianca"], 3)
        response = {'intents': [{'intent': 'greet', 'confidence': 0.5}], 'entities': [], 'input': {'text': 'hola'}, 'output': {'generic': [{'response_type': 'text', 'text': 'Boa noite, sou a técnica virtual Mári. Com quem falo?'}], 'text': ['Boa noite, sou a técnica virtual Mári. Com quem falo?'], 'nodes_visited': ['Bem-vindo', 'node_11_1532701072565'], 'times': [{'max': '300', 'silence': '30', 'interval': '5'}], 'log_messages': []}, 'context': {'conversation_id': '002', 'timezone': 'America/Sao_Paulo', 'chamada_valida': '', 'time': '2018-10-18T22:32:18.545300', 'repetida': '', 'name': '', 'etapa': 'welcome', 'system': {'initialized': True, 'dialog_stack': [{'dialog_node': 'root'}], 'dialog_turn_counter': 1, 'dialog_request_counter': 1, '_node_output_map': {'node_11_1532701072565': {'0': [0, 0, 1]}}, 'branch_exited': True, 'branch_exited_reason': 'completed'}, 'rpt': 0, 'servico': 'internet', 'saudacao': 'Boa noite', 'evento_fixo': 'N', 'evento_velox': 'S', 'rpt_silencio': 0, 'rpt_improperio': 0, 'rpt_not_motivo': 0, 'hr_normalizacao': 'sete horas da noite', 'chamada_repetida': 'N', 'data_normalizacao': 'hoje', 'rpt_visitatecnica': 0}}
        response_changed = self.watson.__check_intent_confidence__(response, self.context, etapa_anterior)
        self.assertEqual(response_changed["intervalo_confianca"], 2)
        response = {'intents': [{'intent': 'greet', 'confidence': 0.3}], 'entities': [], 'input': {'text': 'hola'}, 'output': {'generic': [{'response_type': 'text', 'text': 'Boa noite, sou a técnica virtual Mári. Com quem falo?'}], 'text': ['Boa noite, sou a técnica virtual Mári. Com quem falo?'], 'nodes_visited': ['Bem-vindo', 'node_11_1532701072565'], 'times': [{'max': '300', 'silence': '30', 'interval': '5'}], 'log_messages': []}, 'context': {'conversation_id': '002', 'timezone': 'America/Sao_Paulo', 'chamada_valida': '', 'time': '2018-10-18T22:32:18.545300', 'repetida': '', 'name': '', 'etapa': 'welcome', 'system': {'initialized': True, 'dialog_stack': [{'dialog_node': 'root'}], 'dialog_turn_counter': 1, 'dialog_request_counter': 1, '_node_output_map': {'node_11_1532701072565': {'0': [0, 0, 1]}}, 'branch_exited': True, 'branch_exited_reason': 'completed'}, 'rpt': 0, 'servico': 'internet', 'saudacao': 'Boa noite', 'evento_fixo': 'N', 'evento_velox': 'S', 'rpt_silencio': 0, 'rpt_improperio': 0, 'rpt_not_motivo': 0, 'hr_normalizacao': 'sete horas da noite', 'chamada_repetida': 'N', 'data_normalizacao': 'hoje', 'rpt_visitatecnica': 0}}
        response_changed = self.watson.__check_intent_confidence__(response, self.context, etapa_anterior)
        self.assertEqual(response_changed["intervalo_confianca"], 1)
'''
    def test_execute_dialog(self):
        watson_output = self.watson.execute_dialog(self.inbound_message, self.context)
        self.assertEqual(watson_output.intent, "greet")'''







            