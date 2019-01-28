import React, { Component } from "react";
// const fs = require("fs");

class Example extends Component {
  state = {
    fileData: ""
  };

  handleSubmit = e => {
    e.preventDefault();
    var data = e.target.comment.value;
    console.log(data);
    // fs.writeFileSync("tst.txt", data, err => {
    //   if (err) throw err;
    // });

    // fs.write("txt.txt", this.state.fileData, err => {
    //   if (err) throw err;
    // });
  };

  render() {
    return (
      <form onSubmit={e => this.handleSubmit(e)}>
        <input name="comment" type="file" />
        <button type="submit">Submit </button>
      </form>
    );
  }
}

export default Example;
