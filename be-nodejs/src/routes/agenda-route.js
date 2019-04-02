"use strict";

const express = require("express");
const router = express.Router();

const controller = require("../controllers/agenda-controller");

// router.post("/", controller.post);
router.get("/contatos", controller.get);
router.post("/contatos", controller.post);


module.exports = router;


// exports.get = (req, res) => {
//     res.send({ id: 1, nome: "Elton" });
// };
