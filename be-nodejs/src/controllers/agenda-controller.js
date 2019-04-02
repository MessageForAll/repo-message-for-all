"use strict";
const contatos = require("../baseTemp/contatos-base-temp");

exports.get = (req, res, next) => {
  res.send({ contatos });
};

exports.post = (req, res, next) => {
  //post
  res.status(200).send(contatos); // created
  console.log(req.body);
};
