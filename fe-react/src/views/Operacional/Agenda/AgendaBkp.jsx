import React, { Component } from "react";
import { Row, Col, Card, CardBody, CardHeader } from "reactstrap";
import ContatoInput from "./ContatoInput";
import ContatosTableSelection from "./ContatosTableSelection";
import contatosBase from "./ContatosBase";
import ContatosTableVisualization from "./ContatosTableVisualization";

class Agenda extends Component {
  constructor(props) {
    super(props);
  }

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
      rows: contatosBase,
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

  onModifyClick = contato => {
    let c = { ...contato };
    console.table("onModifyClick", c);
  };

  onDeleteClick = contato => {
    console.log("onDeleteClick", contato);

    let newRows = this.state.contatos.rows.filter(row => row.id !== contato.id);
    let newChecked = newRows.map(() => false);
    this.setState({
      contatos: {
        rows: newRows,
        checked: newChecked
      }
    });
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
            <Card>
              <CardHeader>
                <strong>CONTATOS v1</strong>
              </CardHeader>
              <CardBody>
                <ContatosTableSelection
                  contatos={this.state.contatos.rows}
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
                </ContatosTableSelection>
              </CardBody>
            </Card>
          </Col>
        </Row>

        <Row>
          <Col>
            <Card>
              <CardHeader>
                <strong>CONTATOS v2</strong>
              </CardHeader>
              <CardBody>
                <ContatosTableVisualization
                  contatos={this.state.contatos.rows}
                  onModifyClick={contato => this.onModifyClick(contato)}
                  onDeleteClick={contato => this.onDeleteClick(contato)}
                />
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Agenda;
