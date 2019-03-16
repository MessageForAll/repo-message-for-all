import React, { Component } from "react";
import { Card, CardBody, CardHeader, Col, Row, Table } from "reactstrap";

import clientesData from "./ContatosBase";

class Contato extends Component {
  render() {
    const cliente = clientesData.find(
      cliente => cliente.id.toString() === this.props.match.params.id
    );

    const clienteDetails = cliente
      ? Object.entries(cliente)
      : [
          [
            "id",
            <span>
              <i className="text-muted icon-ban" /> Not found
            </span>
          ]
        ];

    return (
      <div className="animated fadeIn">
        <Row>
          <Col lg={6}>
            <Card>
              <CardHeader>
                <strong>
                  <i className="icon-info pr-1" />Contato id:{" "}
                  {this.props.match.params.id}
                </strong>
              </CardHeader>
              <CardBody>
                <Table responsive striped hover>
                  <tbody>
                    {clienteDetails.map(([key, value]) => {
                      return (
                        <tr key={key}>
                          <td>{`${key}:`}</td>
                          <td>
                            <strong>{value}</strong>
                          </td>
                        </tr>
                      );
                    })}
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

export default Contato;
