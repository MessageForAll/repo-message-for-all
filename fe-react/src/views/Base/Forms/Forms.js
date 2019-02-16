import React, { Component } from "react";
import { post } from "axios";
import Swal from "sweetalert2";
import {
  // Badge,
  Button,
  // ButtonDropdown,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Col,
  // Collapse,
  // DropdownItem,
  // DropdownMenu,
  // DropdownToggle,
  // Fade,
  Form,
  FormGroup,
  // FormText,
  // FormFeedback,
  Input,
  // InputGroup,
  // InputGroupAddon,
  // InputGroupText,
  Label,
  Row
} from "reactstrap";

class Forms extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.toggleFade = this.toggleFade.bind(this);
    this.state = {
      collapse: true,
      fadeIn: true,
      timeout: 300,
      selectedFile: null,
      loaded: 0,
      textoParaMarketing: "",
      responseFromApi: {},
      clientId: 0,
      clientName: "Padaria do Manel",
      fileInputState: false
    };
    this.baseState = this.state;
  }

  toggle() {
    this.setState({ collapse: !this.state.collapse });
  }

  toggleFade() {
    this.setState(prevState => {
      return { fadeIn: !prevState };
    });
  }

  handleTextoParaMarketing = e => {
    this.setState({ textoParaMarketing: e.target.value });
  };

  handleInputFile = e => {
    this.setState({ selectedFile: e.target.files[0] });
  };

  handlePlaceHolderTextArea = () => {
    return this.state.valuePlaceHolderTextArea === ""
      ? "Digite um texto aqui para envio de SMS..."
      : this.state.textoParaMarketing;
  };

  handleSubmitForm = () => {
    if (this.state.selectedFile) {
      let reader = new FileReader();
      reader.readAsText(this.state.selectedFile);
      reader.onload = e => {
        let fraseologia = this.state.textoParaMarketing;
        let clientId = this.state.clientId;
        let clientName = this.state.clientName;
        let vMsisdnList = e.target.result
          .split("\n")
          .filter(msisdn => msisdn !== "");

        //------> envio de um objeto
        let jsonData = {
          clientId: clientId,
          clientName: clientName,
          fraseologia: fraseologia,
          msisdnList: vMsisdnList
        };

        //------> Metodo do indiano com axios!!!
        const url = "http://localhost:3001/form-envio-de-sms";
        const formData = { jsonDataFormEnvioDeSms: jsonData };
        return post(url, formData)
          .then(response => {
            this.setState({ responseFromApi: response.data });
            console.log(this.state.responseFromApi);
          })
          .then(() => {
            Swal.fire({
              position: "center",
              type: "success",
              title: "SMS Broadcast Enviado!",
              showConfirmButton: false,
              timer: 1500
            });
          }).then(()=>{
            this.handleResetForm();
          })
      };
    } else {
      Swal.fire({
        type: "error",
        title: "Oops...",
        text: "Faltou informar um arquivo!"
      });
    }
  };

  handleResetForm = () => {
    this.setState(this.baseState);
  };

  render() {
    return (
      <div className="animated fadeIn">
        <Row>
          <Col xs="12" md="12">
            <Card>
              <CardHeader>
                <strong>Envio De SMS Broadcast</strong>
              </CardHeader>
              <CardBody>
                <Form
                  action=""
                  method="post"
                  encType="multipart/form-data"
                  className="form-horizontal"
                >
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="textarea-input">
                        Texto Para Marketing
                      </Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input
                        type="textarea"
                        name="textarea-input"
                        id="textarea-input"
                        rows="9"
                        placeholder="Digite um texto aqui para envio de SMS..."
                        value={this.state.textoParaMarketing}
                        onChange={e => this.handleTextoParaMarketing(e)} ////////////////////////////////// handleTextoParaMarketing
                      />
                    </Col>
                  </FormGroup>

                  <FormGroup row>
                    <Col md="3">
                      <Label>Selecao De Destinos</Label>
                    </Col>
                    <Col md="9">
                      <FormGroup check className="radio">
                        <Input
                          className="form-check-input"
                          type="radio"
                          id="radio1"
                          name="radios"
                          value="option1"
                          onChange={e => this.handleSelecaoDestino(e)}
                        />
                        <Label
                          check
                          className="form-check-label"
                          htmlFor="radio1"
                        >
                          Da Agenda
                        </Label>
                      </FormGroup>
                      <FormGroup check className="radio">
                        <Input
                          className="form-check-input"
                          type="radio"
                          id="radio2"
                          name="radios"
                          value="option2"
                          onChange={e => this.handleSelecaoDestino(e)}
                        />
                        <Label
                          check
                          className="form-check-label"
                          htmlFor="radio2"
                        >
                          Do Arquivo
                        </Label>
                      </FormGroup>
                      <FormGroup check className="radio">
                        <Input
                          className="form-check-input"
                          type="radio"
                          id="radio3"
                          name="radios"
                          value="option3"
                          onChange={e => this.handleSelecaoDestino(e)}
                        />
                        <Label
                          check
                          className="form-check-label"
                          htmlFor="radio3"
                        >
                          Individual R$0,20
                        </Label>
                      </FormGroup>
                    </Col>
                  </FormGroup>

                  <FormGroup
                    row
                    style={this.handleVisibility(this.state.fileInputState)}
                  >
                    <Col md="3">
                      <Label htmlFor="file-input">
                        Listagem de Numeros de Destino
                      </Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input
                        type="file"
                        id="file-input"
                        name="file-input"
                        onChange={e => this.handleInputFile(e)} ////////////////////////////// onChange
                      />
                    </Col>
                  </FormGroup>
                </Form>
              </CardBody>
              <CardFooter>
                <Button
                  type="submit"
                  size="sm"
                  color="primary"
                  onClick={this.handleSubmitForm}
                >
                  <i className="fa fa-dot-circle-o" /> Submit
                </Button>
                <Button
                  type="reset"
                  size="sm"
                  color="danger"
                  onClick={e => this.handleResetForm(e)}
                >
                  <i className="fa fa-ban" /> Reset
                </Button>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }

  handleSelecaoDestino = e => {
    switch (e.target.value) {
      case "option1":
        console.log("Da Agenda");
        this.setState({ fileInputState: false });
        this.handleVisibility(this.state.fileInputState);
        break;
      case "option2":
        console.log("Do Arquivo");
        this.setState({ fileInputState: true });
        this.handleVisibility(this.state.fileInputState);
        break;
      case "option3":
        console.log("Individual");
        this.setState({ fileInputState: false });
        this.handleVisibility(this.state.fileInputState);
        break;
      default:
        console.log("Nao foi encontrado um valor.");
    }
  };

  handleVisibility = on => {
    return on ? {} : { visibility: "hidden" };
  };
}

export default Forms;
