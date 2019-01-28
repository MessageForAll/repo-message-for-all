#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os
import os.path

class S(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))			
		arquivo = './registro/stc_%s.json' %str(self.headers['msisdn'])
		if os.path.isfile(arquivo):					
			with open(arquivo,'r', encoding='utf-8') as data_file:
				data = data_file.read()	  
		else:
			with open('./registro/mock_stc.json','r',encoding='utf8',errors="ignore") as data_file:
				data = data_file.read()	
		self._set_response()
		self.wfile.write(bytes(data,'utf-8'))

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",str(self.path), str(self.headers), post_data.decode('utf-8'))
		msisdn = json.loads(post_data.decode('utf-8'))			
		with open('./registro/stc_%s.json' %str(msisdn['Terminal_Reclamado']), "w+",encoding='utf8') as data_file:
			data_file.write(post_data.decode('utf-8'))							
		data = "{\"msg\": \"Gravado com Sucesso\"}"
		self._set_response()
		self.wfile.write(bytes(data,'utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=9100):
	logging.basicConfig(level=logging.INFO)
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	logging.info('Iniciado Servidor STC SAC na porta %s \n' %port)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	logging.info('Parando servidor STC SAC na porta %s ...\n' %port)

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()