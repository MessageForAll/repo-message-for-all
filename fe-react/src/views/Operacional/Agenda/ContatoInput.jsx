import React, { Component } from "react";

import {
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  Form,
  FormGroup,
  Label,
  Input,
  Button
} from "reactstrap";

class ContatoInput extends Component {
  render() {
    const {
      onInputName,
      onInputGroup,
      onInputEmail,
      onInputMsisdn,
      onAdd
    } = this.props;
    return (
      <Card>
        <CardHeader>
          <strong>INCLUSAO DE CONTATO NA AGENDA</strong>
        </CardHeader>
        <CardBody>
          <Card>
            <Form action="" method="post" inline>
              <FormGroup className="pr-1">
                <Label htmlFor="exampleInputName2" className="pr-1">
                  Name:
                </Label>
                <Input
                  type="text"
                  id="exampleInputName2"
                  placeholder="Jane Doe"
                  onChange={e => onInputName(e)}
                  required
                />
              </FormGroup>

              <FormGroup className="pr-1">
                <Label htmlFor="exampleInputName2" className="pr-1">
                  Grupo:
                </Label>
                <Input
                  type="text"
                  id="exampleInputName2"
                  placeholder="Jane Doe"
                  onChange={e => onInputGroup(e)}
                  required
                />
              </FormGroup>
              <FormGroup className="pr-1">
                <Label htmlFor="exampleInputEmail2" className="pr-1">
                  Email:
                </Label>
                <Input
                  type="email"
                  id="exampleInputEmail2"
                  placeholder="jane.doe@example.com"
                  onChange={e => onInputEmail(e)}
                />
              </FormGroup>
            </Form>
          </Card>
          <Card>
            <Form action="" method="post" inline>
              <FormGroup className="pr-1">
                <Label htmlFor="exampleInputName2" className="pr-1">
                  Telefone:
                </Label>
                <Input
                  type="text"
                  id="exampleInputName2"
                  placeholder="(xx) xxxxx-xxxx"
                  onChange={e => onInputMsisdn(e)}
                  required
                />
              </FormGroup>
            </Form>
          </Card>
        </CardBody>
        <CardFooter>
          <Button
            onClick={() => onAdd()}
            type="submit"
            size="sm"
            color="primary"
          >
            <i className="fa fa-dot-circle-o" /> Salvar Contato
          </Button>
          <Button type="reset" size="sm" color="danger">
            <i className="fa fa-ban" /> Reset
          </Button>
        </CardFooter>
      </Card>
    );
  }
}

export default ContatoInput;
