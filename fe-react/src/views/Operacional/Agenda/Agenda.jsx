import React, { Component } from "react";
import { Row, Col } from "reactstrap";
import AgendaInput from "./AgendaInput";
import AgendaTable from "./AgendaTable";
import clientesData from "./ClientesData";

class Agenda extends Component {
  state = {
    agendaTableHeaderColumns: [
      "id",
      "Nome",
      "Grupo de Contatos",
      "e-mail",
      "Numero"
    ],
    checkboxHeader: false,
    clientes: {
      checked: clientesData.map(() => {
        return false;
      })
    }
  };

  handleCheckboxHeader = e => {
    let listTrue = this.state.clientes.checked.map(() => {
      return true;
    });
    let listFalse = this.state.clientes.checked.map(() => {
      return false;
    });

    if (e.target.checked) {
      this.setState({ checkboxHeader: true, clientes: { checked: listTrue } });
    } else {
      this.setState({
        checkboxHeader: false,
        clientes: { checked: listFalse }
      });
    }
  };
  handleChangeRowBody = clienteId => {
    let list = this.state.clientes.checked;
    list[clienteId] = !list[clienteId];
    this.setState({ clientes: { checked: list } });
    // this.handleCheckboxRowBody(clienteId);

    let isFalse = list.reduce((acc, i) => {
      return acc && i;
    }, true);
    if (!isFalse) {
      this.setState({ checkboxHeader: false }); // Se houve 1 elemento false em list, mudo o this.state.checkboxHeader para false!!
    } else {
      this.setState({ checkboxHeader: true });
    }
  };

  handleCheckboxRowBody = clienteId => {
    return this.state.clientes.checked[clienteId];
  };

  handleInputBodyId = clienteId => {
    return `checkbox-body-${clienteId}`;
  };
  handleDeleteClient = e => {
    console.log(e.target.id);
    // this.handleInputFile(this.state.fileEventTarget, true);
    // this.setState(this.baseState);
  };
  handleChangeClient = e => {
    console.log(e.target.id);
    // this.handleInputFile(this.state.fileEventTarget, true);
    // this.setState(this.baseState);
  };

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col>
            <AgendaInput />
          </Col>
        </Row>
        <Row>
          <Col>
            <AgendaTable
              clientes={clientesData}
              onChange={clienteId => this.handleChangeRowBody(clienteId)}
              checked={clienteId => this.handleCheckboxRowBody(clienteId)}
              inputId={clienteId => this.handleInputBodyId(clienteId)}
            >
              {/* Header - Table */}
              <th scope="col">
                <input
                  type="checkbox"
                  name="checkbox-header"
                  id="checkbox-header"
                  onChange={e => this.handleCheckboxHeader(e)}
                  checked={this.state.checkboxHeader}
                />
              </th>
              {this.state.agendaTableHeaderColumns.map((column, index) => {
                return (
                  <th key={index} scope="col">
                    {column}
                  </th>
                );
              })}
            </AgendaTable>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Agenda;
