import React, { Component } from "react";
import { Card, CardBody, CardHeader, Table } from "reactstrap";
import { Link } from "react-router-dom";

class AgendaTable extends Component {
  render() {
    return (
      <Card>
        <CardHeader>
          <strong>AGENDA</strong>
        </CardHeader>
        <CardBody>
          <Table responsive hover>
            <thead>
              <tr>{this.props.children}</tr>
            </thead>
            <tbody>
              {/* {console.log(this.props.checked(1))} */}
              {this.props.clientes.map((cliente, index) => (
                <ClienteRow
                  key={index}
                  cliente={cliente}
                  onChange={() => this.props.onChange(cliente.id)}
                  checked={() => this.props.checked(cliente.id)}
                  inputId={() => this.props.inputId(cliente.id)}
                />
              ))}
            </tbody>
          </Table>
        </CardBody>
      </Card>
    );
  }
}

function ClienteRow(props) {
  const cliente = props.cliente;
  const clienteLink = `/operacional/clientes/${cliente.id}`;

  return (
    <tr key={cliente.id.toString()}>
      <th>
        <input
          type="checkbox"
          name="checkbox-body"
          id={props.inputId(cliente.id)}
          checked={props.checked(cliente.id)}
          onChange={props.onChange}
        />
      </th>
      <th scope="row">
        <Link to={clienteLink}>{cliente.id}</Link>
      </th>
      <td>
        <Link to={clienteLink}>{cliente.name}</Link>
      </td>
      <td>{cliente.grupo}</td>
      <td>{cliente.email}</td>
      <td>{cliente.msisdn}</td>
    </tr>
  );
}

export default AgendaTable;
