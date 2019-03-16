import React, { Component } from "react";
import { Card, CardBody, CardHeader, Table } from "reactstrap";
import { Link } from "react-router-dom";

class ContatosTable extends Component {
  render() {
    return (
      <Card>
        <CardHeader>
          <strong>CONTATOS</strong>
        </CardHeader>
        <CardBody>
          <Table responsive hover>
            <thead>
              <tr>{this.props.children}</tr>
            </thead>
            <tbody>
              {/* {console.log(this.props.checked(1))} */}
              {this.props.contatos.map((contato, index) => (
                <ContatoRow
                  key={index}
                  contato={contato}
                  onChange={() => this.props.onChange(contato.id)}
                  checked={() => this.props.checked(contato.id)}
                  inputId={() => this.props.inputId(contato.id)}
                />
              ))}
            </tbody>
          </Table>
        </CardBody>
      </Card>
    );
  }
}

function ContatoRow(props) {
  const contato = props.contato;
  const contatoLink = `/operacional/agenda/${contato.id}`;

  return (
    <tr key={contato.id.toString()}>
      <th>
        <input
          type="checkbox"
          name="checkbox-body"
          id={props.inputId(contato.id)}
          checked={props.checked(contato.id)}
          onChange={props.onChange}
        />
      </th>
      <th scope="row">
        <Link to={contatoLink}>{contato.id}</Link>
      </th>
      <td>
        <Link to={contatoLink}>{contato.name}</Link>
      </td>
      <td>{contato.grupo}</td>
      <td>{contato.email}</td>
      <td>{contato.msisdn}</td>
    </tr>
  );
}

export default ContatosTable;
