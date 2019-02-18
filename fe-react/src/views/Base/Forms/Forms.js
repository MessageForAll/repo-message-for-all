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
      selectedFile: undefined,
      fileUploadName: "",
      loaded: 0,
      textoParaMarketing: "",
      responseFromApi: {},
      clientId: 6578,
      clientName: "Padaria do Manel",
      fileInputState: false,
      radioState: {
        agenda: false,
        arquivo: false,
        individual: false
      }
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
    e.preventDefault();
    this.setState({
      selectedFile: e.target.files[0],
      fileUploadName: e.target.files[0].name
    });

    try {
      console.log(e.target.files[0].name, "-------", this.state);
    } catch (error) {
      console.log(
        "ERROR!!!! e.target.files[0].name nao foi carregado!",
        e.target.value
      );
    }
  };

  handlePlaceHolderTextArea = () => {
    return this.state.valuePlaceHolderTextArea === ""
      ? "Digite um texto aqui para envio de SMS..."
      : this.state.textoParaMarketing;
  };

  handleVisibility = on => {
    return on ? {} : { visibility: "hidden" };
  }; //

  handleSelecaoDestino = e => {
    switch (e.target.value) {
      case "option1":
        console.log("Da Agenda", this.state);
        this.setState({
          fileInputState: false,
          radioState: {
            agenda: true,
            arquivo: false,
            individual: false
          }
        });
        this.handleVisibility(this.state.fileInputState);
        break;
      case "option2":
        console.log("Do Arquivo", this.state);
        this.setState({
          fileInputState: false,
          radioState: {
            agenda: false,
            arquivo: true,
            individual: false
          }
        });
        this.setState({ fileInputState: true });
        this.handleVisibility(this.state.fileInputState);
        break;
      case "option3":
        console.log("Individual", this.state);
        this.setState({
          fileInputState: false,
          radioState: {
            agenda: false,
            arquivo: false,
            individual: true
          }
        });
        this.setState({ fileInputState: false });
        this.handleVisibility(this.state.fileInputState);
        break;
      default:
        console.log("Nao foi encontrado um valor.");
    }
  };

  handleSubmitForm = e => {
    e.preventDefault();
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
          })
          .then(() => {
            console.log("submit", this.state);
          })
          .then(() => {
            this.handleResetForm();
            this.forceUpdate();
          });
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
    console.log("reset", this.state);
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
                  {/* {Bloco 1: Texto Para Marketing} */}
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
                        onChange={e => this.handleTextoParaMarketing(e)}
                      />
                    </Col>
                  </FormGroup>

                  {/* {Bloco 2: Selecao De Destinos} */}
                  <FormGroup row>
                    <Col md="3">
                      <Label>Selecao De Destinos</Label>
                    </Col>
                    <Col md="9">
                      {/* {Da Agenda} */}
                      <FormGroup check className="radio">
                        <Input
                          className="form-check-input"
                          type="radio"
                          id="radio1"
                          name="radios"
                          value="option1"
                          checked={this.state.radioState.agenda}
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

                      {/* {Do arquivo} */}
                      <FormGroup check className="radio">
                        <input
                          className="form-check-input"
                          type="radio"
                          id="radio2"
                          name="radios"
                          value="option2"
                          onChange={e => this.handleSelecaoDestino(e)}
                          checked={this.state.radioState.arquivo}
                        />
                        <Label
                          check
                          className="form-check-label"
                          htmlFor="radio2"
                        >
                          Do Arquivo
                        </Label>
                      </FormGroup>

                      {/* {Individual R$0,20} */}
                      <FormGroup check className="radio">
                        <Input
                          className="form-check-input"
                          type="radio"
                          id="radio3"
                          name="radios"
                          value="option3"
                          onChange={e => this.handleSelecaoDestino(e)}
                          checked={this.state.radioState.individual}
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

                  {/* {Bloco 3: Listagem De Numeros De Destinos} */}
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

              {/* {Bloco 4: Rodape Botoes Submit e Reset} */}
              <CardFooter>
                <Button
                  type="submit"
                  size="sm"
                  color="primary"
                  htmlFor="file-input"
                  onClick={e => {
                    this.handleSubmitForm(e);
                  }}
                >
                  <i className="fa fa-dot-circle-o" /> Submit
                </Button>

                <Button
                  type="reset"
                  size="sm"
                  color="danger"
                  htmlFor="file-input"
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
}

export default Forms;
