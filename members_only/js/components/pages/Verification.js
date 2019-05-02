import React, { Component } from "react";
import Notification from "../Notification";
import { Route, Redirect } from "react-router";

class Verification extends Component {
  constructor(props) {
    super(props);

    this.state = {
      notificationText: "",
      notificationType: "success",
      verified: false
    };


    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    let data = JSON.stringify({
      amount: this.amount.value
    });

    let xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", event => {
      if (event.target.readyState === 4) {

        var jsonResponse = JSON.parse(xhr.responseText);

        if(jsonResponse.success){
          
          this.setState({
            notificationText: xhr.response.message,
            notificationType: "success",
            verified: true
          });

        }else{
          this.setState({
            notificationText: "Incorrect Amount.",
            notificationType: "danger",
            verified: false
          });
        }
      }
    });

    xhr.open("PUT", "/api/user/verify/");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");
    xhr.setRequestHeader("Authorization", "Token " + this.props.token);

    xhr.send(data);
  }

  render() {
    return this.state.verified ? (
      <Redirect to={"/feed"} />
    ) : (
      <form onSubmit={this.handleSubmit}>
        <div className="columns">
          <div className="column is-offset-one-quarter is-half">
            <h1 className="title" style={header}>
              Verification
            </h1>

            <Notification
              text={this.state.notificationText}
              type={this.state.notificationType}
            />

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="number"
                  placeholder="Amount charged in cents"
                  ref={input => (this.amount = input)}
                />
              </p>
            </div>

            <div className="field" style={{ marginTop: "20px" }}>
              <p className="control">
                <input
                  type="submit"
                  value="Verify"
                  className="button is-success"
                />
              </p>
            </div>
          </div>
        </div>
      </form>
    );
  }
}

const header = {
  marginTop: "40px",
  fontVariant: "small-caps",
  fontSize: "40px"
};

export default Verification;

