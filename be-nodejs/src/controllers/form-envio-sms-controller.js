"use strict";
const fs = require("fs");
var smpp = require("smppnew");

const smscCredential = {
  url: "smpp://10.125.124.24:17600",
  systemId: "oemtstipa",
  password: "oemrtz"
};

function smppConnection(smscCredential, destinationNumber, smsText) {
  console.log("Sending message to ", destinationNumber, " ...");
  var session = smpp.connect(smscCredential.url);
  session.bind_transceiver(
    {
      system_id: smscCredential.systemId,
      password: smscCredential.password
    },
    function(pdu) {
      if (pdu.command_status == 0) {
        // Successfully bound
        // retorna uma promisse aqui para controlar e aguardar o resultado???
        session.submit_sm(
          {
            destination_addr: destinationNumber,
            short_message: smsText
          },
          function(pdu) {
            if (pdu.command_status == 0) {
              // Message successfully sent
              // retorna uma promisse aqui para controlar e aguardar o resultado???

              console.log(pdu.message_id);
            } else {
              console.log(pdu.command_status);
            }
          }
        );
      } else {
        console.log(pdu.command_status);
      }
    }
  );
}

exports.post = (req, res) => {
  //---> Request
  const {
    clientId,
    clientName,
    fraseologia,
    msisdnList
  } = req.body.jsonDataFormEnvioDeSms;

  console.log(req.body);

  // msisdnList.map(destinationNumber => {
  //   smppConnection(smscCredential, destinationNumber, fraseologia);
  // });

  fs.writeFile(
    "temp/formEnvioSmsOfClientId_" + clientId.toString() + ".txt",
    fraseologia,
    e => {
      if (e) {
        return e;
      }
    }
  );

  // ---> Response
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, OPTIONS, PUT, PATCH, DELETE"
  );
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-Requested-With,content-type"
  );
  res.setHeader("Access-Control-Allow-Credentials", true);
  res.status(200).send("Arquivo Salvo!");
};


