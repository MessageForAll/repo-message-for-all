import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Badge, Card, CardBody, CardHeader, Col, Row, Table } from "reactstrap";

import clientesData from "./ClientesData";

function ClienteRow(props) {
  const cliente = props.cliente;
  const clienteLink = `/operacional/clientes/${cliente.id}`;

  // const getBadge = status => {
  //   return status === "Active"
  //     ? "success"
  //     : status === "Inactive"
  //     ? "secondary"
  //     : status === "Pending"
  //     ? "warning"
  //     : status === "Banned"
  //     ? "danger"
  //     : "primary";
  // };

  return (
    <tr key={cliente.id.toString()}>
      <th scope="row">
        <Link to={clienteLink}>{cliente.id}</Link>
      </th>
      <td>
        <Link to={clienteLink}>{cliente.name}</Link>
      </td>
      <td>{cliente.grupo}</td>
      <td>{cliente.email}</td>
      {/* <td>
        <Link to={clienteLink}>
          <Badge color={getBadge(cliente.status)}>{cliente.status}</Badge>
        </Link>
      </td> */}
      <td>{cliente.msisdn}</td>
    </tr>
  );
}

class Clientes extends Component {
  render() {
    const clienteList = clientesData.filter(cliente => cliente.id < 10);

    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={6}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify" /> clientes{" "}
                <small className="text-muted">example</small>
              </CardHeader>
              <CardBody>
                <Table responsive hover>
                  <thead>
                    <tr>
                      <th scope="col">id</th>
                      <th scope="col">Nome</th>
                      <th scope="col">Grupo de Contatos</th>
                      <th scope="col">e-mail</th>
                      <th scope="col">Numero</th>
                    </tr>
                  </thead>
                  <tbody>
                    {clienteList.map((cliente, index) => (
                      <ClienteRow key={index} cliente={cliente} />
                    ))}
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Clientes;
