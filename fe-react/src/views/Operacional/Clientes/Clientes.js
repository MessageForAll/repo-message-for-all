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

class Clientes extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tableSize: 12,
      checkboxHeader: false,
      checkboxBody: false,
      clientes: {
        checked: clientesData.map(() => {
          return false;
        })
      }
    };
  }

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

  handleCheckboxBody = clienteId => {
    let list = this.state.clientes.checked;
    list[clienteId] = !list[clienteId];
    this.setState({ clientes: { checked: list } });

    let isFalse = list.reduce((acc, i) => {
      return acc && i;
    }, true);
    if (!isFalse) {
      this.setState({ checkboxHeader: false }); // Se houve 1 elemento false em list, mudo o this.state.checkboxHeader para false!!
    } else {
      this.setState({ checkboxHeader: true });
    }
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
    const clienteList = clientesData.filter(cliente => cliente.id < 10); ///////////////////

    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={this.state.tableSize}>
            <Card>
              <CardHeader>
                <strong>INCLUSAO DE CLIENTES NA AGENDA</strong>
              </CardHeader>
              <CardBody>
                <Form action="" method="post" inline>
                  <FormGroup className="pr-1">
                    <Label htmlFor="exampleInputName2" className="pr-1">
                      Name
                    </Label>
                    <Input
                      type="text"
                      id="exampleInputName2"
                      placeholder="Jane Doe"
                      required
                    />
                  </FormGroup>
                  <FormGroup className="pr-1">
                    <Label htmlFor="exampleInputEmail2" className="pr-1">
                      Email
                    </Label>
                    <Input
                      type="email"
                      id="exampleInputEmail2"
                      placeholder="jane.doe@example.com"
                      required
                    />
                  </FormGroup>
                </Form>
              </CardBody>
              <CardFooter>
                <Button type="submit" size="sm" color="primary">
                  <i className="fa fa-dot-circle-o" /> Salvar Contato
                </Button>
                <Button type="reset" size="sm" color="danger">
                  <i className="fa fa-ban" /> Reset
                </Button>
              </CardFooter>
            </Card>
          </Col>
        </Row>

        <Row>
          <Col xl={this.state.tableSize}>
            <Card>
              <CardHeader>
                <strong>AGENDA</strong>
                {/* <small className="text-muted">example</small> */}
              </CardHeader>
              <CardBody>
                <Table responsive hover>
                  <thead>
                    <tr>
                      <th scope="col">
                        <input
                          type="checkbox"
                          name="checkbox-header"
                          id="checkbox-header"
                          onChange={e => this.handleCheckboxHeader(e)}
                          checked={this.state.checkboxHeader}
                        />
                      </th>
                      <th scope="col">id</th>
                      <th scope="col">Nome</th>
                      <th scope="col">Grupo de Contatos</th>
                      <th scope="col">e-mail</th>
                      <th scope="col">Numero</th>
                    </tr>
                  </thead>
                  <tbody>
                    {clienteList.map((cliente, index) => (
                      <ClienteRow
                        key={index}
                        cliente={cliente}
                        onChange={()=> this.handleCheckboxBody(cliente.id)}
                        checked={this.state.clientes.checked[cliente.id]} ///////// this.state.clientes.id[id] | this.state.clientes.checked[id]
                        inputId={this.handleInputBodyId(cliente.id)}
                      />
                    ))}
                  </tbody>
                </Table>
              </CardBody>
              <CardFooter>
                <Button
                  type="submit"
                  size="sm"
                  color="info"
                  id="deleteRow"
                  name="deleteRow"
                  onClick={e => this.handleDeleteClient(e)}
                >
                  <i className="fa fa-ban" /> Deletar
                </Button>
                <strong> </strong>
                <Button
                  type="submit"
                  size="sm"
                  color="info"
                  id="changeRow"
                  name="changeRowRow"
                  onClick={e => this.handleChangeClient(e)}
                >
                  <i className="fa fa-dot-circle-o" /> Modificar
                </Button>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
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

export default Clientes;
