import React, { Component } from "react";
import { Table } from "reactstrap";
import { Link } from "react-router-dom";

class ContatosTableSelection extends Component {
  render() {
    const {
      contatos, //contatos.rows e contatos.checked
      onChangeHeader,
      onCheckedHeader,
      onChangeBody,
      onCheckedBody,
      inputId
    } = this.props;
    return (
      <Table responsive hover>
        <thead>
          <tr>
            <th scope="col">
              {console.log(onCheckedHeader)}
              <input
                type="checkbox"
                name="checkbox-header"
                id="checkbox-header"
                onChange={e => onChangeHeader(e)}
                checked={onCheckedHeader}
              />
            </th>
            <th>id</th>
            <th>Nome</th>
            <th>Grupo</th>
            <th>e-mail</th>
            <th>Numero</th>
          </tr>
        </thead>
        <tbody>
          {contatos.rows.map((contato, index) => (
            <ContatoRow
              key={index}
              contato={contato}
              onChangeBody={() => onChangeBody(contato.id)}
              onCheckedBody={() => onCheckedBody(contato.id)}
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
          onChange={props.onChangeBody(contato.id)}
          checked={props.onCheckedBody(contato.id)}
          id={props.inputId(contato.id)}
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

export default ContatosTableSelection;
