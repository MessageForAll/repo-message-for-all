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
    res.status(200).send("Arquivo Salvo!");
    console.log(req.body);
    const {clientId,clientName, fraseologia} = req.body.jsonDataFormEnvioDeSms;
    fs.writeFile("formEnvioSmsOfClientId_"+clientId.toString()+".txt",fraseologia, e => {
        if (e) {
            return e;
        }
    });
};
