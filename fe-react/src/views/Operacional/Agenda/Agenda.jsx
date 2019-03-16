import React, { Component } from "react";
import { Row, Col } from "reactstrap";
import ContatoInput from "./ContatoInput";
import ContatosTable from "./ContatosTable";
import contatosBase from "./ContatosBase";

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
    contatos: {
      checked: contatosBase.map(() => {
        return false;
      })
    }
  };

  handleCheckboxHeader = e => {
    let listTrue = this.state.contatos.checked.map(() => {
      return true;
    });
    let listFalse = this.state.contatos.checked.map(() => {
      return false;
    });

    if (e.target.checked) {
      this.setState({ checkboxHeader: true, contatos: { checked: listTrue } });
    } else {
      this.setState({
        checkboxHeader: false,
        contatos: { checked: listFalse }
      });
    }
  };
  handleChangeRowBody = contatoId => {
    let list = this.state.contatos.checked;
    list[contatoId] = !list[contatoId];
    this.setState({ contatos: { checked: list } });
    // this.handleCheckboxRowBody(contatoId);

    let isFalse = list.reduce((acc, i) => {
      return acc && i;
    }, true);
    if (!isFalse) {
      this.setState({ checkboxHeader: false }); // Se houve 1 elemento false em list, mudo o this.state.checkboxHeader para false!!
    } else {
      this.setState({ checkboxHeader: true });
    }
  };

  handleCheckboxRowBody = contatoId => {
    return this.state.contatos.checked[contatoId];
  };

  handleInputBodyId = contatoId => {
    return `checkbox-body-${contatoId}`;
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
            <ContatoInput />
          </Col>
        </Row>
        <Row>
          <Col>
            <ContatosTable
              contatos={contatosBase}
              onChange={contatoId => this.handleChangeRowBody(contatoId)}
              checked={contatoId => this.handleCheckboxRowBody(contatoId)}
              inputId={contatoId => this.handleInputBodyId(contatoId)}
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
            </ContatosTable>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Agenda;
