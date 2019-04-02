import { Table, Button } from "reactstrap";
import React, { Component } from "react";
import { Link } from "react-router-dom";

class ContatosTableVisualization extends Component {
  render() {
    const { contatos, onModify, onDelete } = this.props;
    return (
      <Table responsive hover>
        <thead>
          <tr>
            <th>id</th>
            <th>Nome</th>
            <th>Grupo</th>
            <th>e-mail</th>
            <th>Numero</th>
            <th>Modificar</th>
            <th>Deletar</th>
          </tr>
        </thead>
        <tbody>
          {contatos.map(contato => {
            let contatoLink = `/operacional/agenda/${contato.id}`;
            return (
              <tr key={contato.id.toString()}>
                <th scope="row">
                  <Link to={contatoLink}>{contato.id}</Link>
                </th>
                <td>
                  <Link to={contatoLink}>{contato.name}</Link>
                </td>
                <td>{contato.grupo}</td>
                <td>{contato.email}</td>
                <td>{contato.msisdn}</td>
                <td>
                  <Button
                    onClick={() => onModify(contato)}
                    color="warning"
                  >
                    Modificar
                  </Button>
                </td>
                <td>
                  <Button
                    onClick={() => onDelete(contato)}
                    color="danger"
                  >
                    <strong>Deletar</strong>
                  </Button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    );
  }
}

export default ContatosTableVisualization;
