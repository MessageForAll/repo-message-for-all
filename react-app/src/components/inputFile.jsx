import React, { Component } from "react";
import axios from "axios";
//import fs from "fs";
//const fs = require("fs");
const writeFileP = require("write-file-p");

class InputFile extends Component {
  state = { selectedFile: null, loaded: 0 };

  handleselectedFile = event => {
    this.setState({
      selectedFile: event.target.files[0],
      loaded: 0
    });
    var dir = "/c/Users/oi209294/projetos/startup-mobile-marketing/startup-app";
    console.log(dir);
    console.log(writeFileP);
    writeFileP(dir + "/output.txt", event.target.files[0], (err, data) => {
      console.log(err || data);
    });
  };

  handleUpload = () => {
    const data = new FormData();
    data.append("file", this.state.selectedFile, this.state.selectedFile.name);

    axios
      .post("/", data, {
        onUploadProgress: ProgressEvent => {
          this.setState({
            loaded: (ProgressEvent.loaded / ProgressEvent.total) * 100
          });
        }
      })
      .then(res => {
        console.log(res.statusText);
      });
  };

  // render() {
  //   return (
  //     <div className="App">
  //       <input
  //         type="file"
  //         name=""
  //         id="file"
  //         onChange={event => this.handleselectedFile(event)}
  //       />
  //       <button onClick={this.handleUpload}>Upload</button>
  //       <div> {Math.round(this.state.loaded, 2)} %</div>
  //     </div>
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

export default InputFile;
