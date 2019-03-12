import React, { Component } from "react";
import { Link } from "react-router-dom";
import {
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  Col,
  Row,
  Table,
  Form,
  FormGroup,
  Label,
  Input,
  Button
} from "reactstrap";

import clientesData from "./ClientesData";

class ClienteTable extends Component {
  state = {};
  render() {
    return (
      <CardBody>
        <Table responsive hover>
          <thead>
            <tr>
              <th scope="col">
                <input
                  type="checkbox"
                  name="checkbox-header"
                  id="checkbox-header"
                  onChange={this.props.onChange}
                  checked={this.props.checked}
                />
              </th>

              <th scope="col">{this.props.headers[0]}</th>
              <th scope="col">{this.props.headers[1]}</th>
              <th scope="col">{this.props.headers[2]}</th>
              <th scope="col">{this.props.headers[3]}</th>
              <th scope="col">{this.props.headers[4]}</th>
            </tr>
          </thead>
          <tbody>
            

            <ClienteRow
              cliente={this.props.att.cliente}
              onChange={this.props.att.onChange}
              checked={this.props.att.checked}
              inputId={this.props.att.inputId}
              key={this.props.cliente.id}
            />
          </tbody>
        </Table>
      </CardBody>
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
          id={props.inputId}
          checked={props.checked}
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

export default ClienteTable;
