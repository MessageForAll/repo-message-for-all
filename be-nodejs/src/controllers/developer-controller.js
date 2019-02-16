"use strict";
const fs = require("fs");

exports.post = (req, res, next) => {
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
  res.send(req.body);
  console.log("oi");
  fs.writeFile("upload.txt", req.body.file, e => {
    if (e) {
      return e;
    }
  });
};

// exports.get = (req, res, next) => {
//   res.status(201).send(req.body);
// };

exports.put = (req, res, next) => {
  //put
  const developerId = req.params.developerId;
  var developerInformations = getDeveloperById(developerId);
  console.log("oi");
  res
    .setHeader("Access-Control-Allow-Origin", "*")
    .status(200)
    .send({
      devInfo: developerInformations,
      body: req.body // app.use(bodyParser .....)
    });
};

exports.delete = (req, res, next) => {
  //post
  res.status(200).send(req.body);
};

// ------ Funcoes ------- //
function getDeveloperById(id) {
  if (developersBase()[id]) {
    return developersBase()[id];
  } else {
    return {
      name: "undefined",
      idade: "undefined",
      profissao: "undefined"
    };
  }
}

function developersBase() {
  return {
    elton: {
      name: "Elton Braz",
      idade: 32,
      profissao: "engenheiro"
    },
    daniele: {
      name: "Daniele Melo",
      idade: 31,
      profissao: "enge"
    }
  };
}
