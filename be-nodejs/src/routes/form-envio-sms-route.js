"use strict";

const express = require("express");
const router = express.Router();

const controller = require("../controllers/form-envio-sms-controller");

router.post("/", controller.post);

module.exports = router;
