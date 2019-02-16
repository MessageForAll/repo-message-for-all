# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:45:15 2018

@author: dlaivison
"""

import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts
import pandas as pd


logging.basicConfig(level = logging.DEBUG,
    format = "%(levelname)s %(filename)s:%(lineno)d %(message)s")

def send_message(dest,source, string):
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(string)

    logging.info('Sending SMS "%s" to %s' % (string, dest))
    for part in parts:
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_INTL,
            source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            source_addr='3802',
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr=dest,
            short_message=part,
            data_coding=encoding_flag,
            #esm_class=msg_type_flag,
            esm_class=smpplib.consts.SMPP_MSGMODE_FORWARD,
            registered_delivery=False,
    )
    logging.debug(pdu.sequence)


file_bind = pd.read_csv(r'bind_spec.txt')
b_system_ip   = file_bind.loc[0,'IP']
b_system_port = file_bind.loc[0,'PORT']
b_system_type = file_bind.loc[0,'SYSTEM_TYPE']
b_system_id   = file_bind.loc[0,'SYSTEM_ID']
b_system_password = file_bind.loc[0,'PASSWORD']


source_addr= input("Insira o numero de Origem:")
destinations= input("Insira o número de Destino:")
message = input("Insira a mensagem:")



client = smpplib.client.Client(b_system_ip, b_system_port)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

client.connect()
client.bind_transmitter(system_id=b_system_id, password=b_system_password)

#destinations = ('5521', '7839', '3807', '3811', '3806', '3805', '3804', '3809', '3812', '3815', '3814', '3803', '3813')

send_message(destinations,source_addr, message)

client.listen()
