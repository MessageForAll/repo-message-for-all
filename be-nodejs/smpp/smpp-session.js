"use strict";
var smpp = require("smppnew");
const inputData = {
  URL: "smpp://10.125.124.24:17600",
  YOUR_SYSTEM_ID: "oemtstipa",
  YOUR_PASSWORD: "oemrtz",
  DESTINATION_NUMBER: "5521994309366",
  SHORT_MESSAGE_TEXT: "Hello!"
};
var session = smpp.connect(inputData.URL);

session.bind_transceiver(
  {
    system_id: inputData.YOUR_SYSTEM_ID,
    password: inputData.YOUR_PASSWORD
  },
  function(pdu) {
    if (pdu.command_status == 0) {
      // Successfully bound
      session.submit_sm(
        {
          destination_addr: inputData.DESTINATION_NUMBER,
          short_message: inputData.SHORT_MESSAGE_TEXT
        },
        function(pdu) {
          if (pdu.command_status == 0) {
            // Message successfully sent
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

