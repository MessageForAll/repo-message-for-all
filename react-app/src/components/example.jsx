import React, { Component } from "react";
import axios, { post } from "axios";
// const fs = require("fs");
import {
  Badge,
  Button,
  ButtonDropdown,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Col,
  Collapse,
  DropdownItem,
  DropdownMenu,
  DropdownToggle,
  Fade,
  Form,
  FormGroup,
  FormText,
  FormFeedback,
  Input,
  InputGroup,
  InputGroupAddon,
  InputGroupText,
  Label,
  Row
} from "reactstrap";

class Example extends Component {
  state = {
    fileData: ""
  };

  onFormSubmit = () => {

  };

  onChange = e => {
    let files = e.target.files;
    let reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onload = e => {
      console.log(e.target.result);
    };
  };

  // render() {
  //   return (
  //     <form onSubmit={e => this.onFormSubmit}>
  //       <input name="file" type="file" onChange={e => this.onChange(e)} />
  //       <button type="submit">Submit </button>
  //     </form>
  //   );
  // }

  render() {
    return (
      <div>
        <FormGroup row>
          <Col md="3">
            <Label htmlFor="textarea-input">Textarea</Label>
          </Col>
          <Col xs="12" md="9">
            <Input
              type="textarea"
              name="textarea-input"
              id="textarea-input"
              rows="9"
              placeholder="Content..."
            />
          </Col>
        </FormGroup>
      </div>
    );
  }
}

export default Example;
