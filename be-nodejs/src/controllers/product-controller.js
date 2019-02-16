"use strict";

exports.post = (req, res, next) => {
  //post
  res.status(200).send("<h1>oi</h1>"); // created
};

exports.put = (req, res, next) => {
  //put
  const id = req.params.id;
  res.status(200).send({
    id: id,
    item: req.body // app.use(bodyParser .....)
  });
};

exports.delete = (req, res, next) => {
  //post
  res.status(200).send(req.body); // created
};
