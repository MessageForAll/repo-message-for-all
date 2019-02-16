"use strict";

const express = require("express");
const router = express.Router();
const fs = require("fs");

router.post("/", (req, res, next) => {
  res.status(200).send("Arquivo Salvo!");
  console.log(req.body);
  fs.writeFile("teste.txt", req.body.jsonDataFormEnvioDeSms.fraseologia, e => {
    if (e) {
      return e;
    }
  });
});

module.exports = router;
