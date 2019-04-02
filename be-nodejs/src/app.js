"use strict";
// const ejs = require('ejs');
const express = require("express"); // app
const bodyParser = require('body-parser');
var cors = require("cors");

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended:false}));
//const router = express.Router();


// use it before all route definitions
app.use(cors({ origin: "http://localhost:3000" }));

// Carrega as rotas
const indexRoute = require("./routes/index-route");
const productRoute = require("./routes/product-route");
const developerRoute = require("./routes/developer-route");
const formEnvioSmsRoute = require("./routes/form-envio-sms-route");
const agendaRoute = require("./routes/agenda-route");

// Link com as rotas
app.use("/", indexRoute);
app.use("/products", productRoute);
app.use("/developers", developerRoute);
app.use("/form-envio-sms",formEnvioSmsRoute);
app.use("/agenda",agendaRoute);


module.exports = app;
