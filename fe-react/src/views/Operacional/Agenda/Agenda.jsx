import React, { Component } from "react";
import { Row, Col, Card, CardBody, CardHeader } from "reactstrap";
import axios from "axios";
import ContatoInput from "./ContatoInput";
import ContatosTableVisualization from "./ContatosTableVisualization";

const apiEndPoint = "http://localhost:3001/agenda/contatos";
// const objFake = {
//   id: 0,
//   name: "Zico",
//   email: "zico@hotmail.com",
//   msisdn: "5521994309366",
//   grupo: "Idolos do Flamengo",
//   rua: "Clarimundo de Melo",
//   numeroRua: "10",
//   bairro: "Quintino",
//   cidade: "Rio de Janeiro",
//   estado: "RJ",
//   pais: "Brasil"
// };

class Agenda extends Component {
  state = {
    contatos: [],
    contato: {
      id: 100,
      name: "",
      group: "",
      email: "",
      msisdn: "",
      address: {
        rua: "",
        numeroRua: "",
        bairro: "",
        cidade: "",
        estado: "",
        pais: ""
      }
    }
  };

  async componentDidMount() {
    const { data } = await axios.get(apiEndPoint);
    this.setState({ contatos: data.contatos });
  }

  onAdd = async () => {
    const resp = await axios.post(apiEndPoint, this.state.contato);
    const posts = [...resp.data, this.state.contato];
    // const { data } = await axios.post(apiEndPoint, objFake);
    // const posts = [data, ...this.state.contatos];
    // this.setState({ contatos: posts });

    console.log(posts);
  };

  onModify = contato => {
    let c = { ...contato };
    console.table("onModify", c);
  };

  onDelete = contato => {
    let newRows = this.state.contatos.filter(row => row.id !== contato.id);
    this.setState({ contatos: newRows });
  };

  onInputName = e => {
    e.preventDefault();
    let contato = { ...this.state.contato };
    contato.name = e.target.value;
    this.setState({ contato });
  };

  onInputGroup = e => {
    e.preventDefault();
    let contato = { ...this.state.contato };
    contato.group = e.target.value;
    this.setState({ contato });
  };

  onInputEmail = e => {
    e.preventDefault();
    let contato = { ...this.state.contato };
    contato.email = e.target.value;
    this.setState({ contato });
  };

  onInputMsisdn = e => {
    e.preventDefault();
    let contato = { ...this.state.contato };
    contato.msisdn = e.target.value;
    this.setState({ contato });
  };

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col>
            <ContatoInput
              onAdd={() => this.onAdd()}
              onInputName={e => this.onInputName(e)}
              onInputGroup={e => this.onInputGroup(e)}
              onInputEmail={e => this.onInputEmail(e)}
              onInputMsisdn={e => this.onInputMsisdn(e)}
            />
          </Col>
        </Row>

        <Row>
          <Col>
            <Card>
              <CardHeader>
                <strong>CONTATOS</strong>
              </CardHeader>
              <CardBody>
                <ContatosTableVisualization
                  contatos={this.state.contatos}
                  onModify={contato => this.onModify(contato)}
                  onDelete={contato => this.onDelete(contato)}
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
