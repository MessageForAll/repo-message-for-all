"use strict";

const express = require("express");
const router = express.Router();

const controller = require("../controllers/developer-controller");

router.post("/", controller.post);
//router.get('/', controller.get);
//router.put('/:developerId', controller.put);
//router.delete('/', controller.delete);

module.exports = router;
