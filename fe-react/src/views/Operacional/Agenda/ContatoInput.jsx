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
  state = {};
  render() {
    return (
      <Card>
        <CardHeader>
          <strong>INCLUSAO DE CONTATO NA AGENDA</strong>
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
    );
  }
}

export default ContatoInput;
