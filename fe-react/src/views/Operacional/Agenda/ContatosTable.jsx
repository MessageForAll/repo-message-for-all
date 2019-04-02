import React, { Component } from "react";
import { Table } from "reactstrap";
import { Link } from "react-router-dom";

class ContatosTable extends Component {
  render() {
    const {onChange, checked, inputId, children } = this.props;
    return (
      <Table responsive hover>
        <thead>
          <tr>{children}</tr>
        </thead>
        <tbody>
          {/* {console.log(this.props.checked(1))} */}
          {this.props.contatos.map((contato, index) => (
            <ContatoRow
              key={index}
              contato={contato}
              onChange={() => onChange(contato.id)}
              checked={() => checked(contato.id)}
              inputId={() => inputId(contato.id)}
            />
          ))}
        </tbody>
      </Table>
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
