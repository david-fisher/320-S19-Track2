import React, { Component } from "react";
import StripeCheckout from "react-stripe-checkout";
import Notification from "../Notification";
import { Route, Redirect } from "react-router";

class Setup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      notificationText: "",
      notificationType: "success",
      setupComplete: false
    };
    this.onToken = (token, addresses) => (this.token = token.id);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    if (this.password.value != this.confirm_password.value) {
      this.setState({
        notificationText: "Your passwords don't match.",
        notificationType: "danger"
      });

      event.preventDefault();
      return;
    }

    if (this.access_code.value == "") {
      this.setState({
        notificationText: "Access code is blank.",
        notificationType: "danger"
      });

      event.preventDefault();
      return;
    }

    if (this.email.value == "") {
      this.setState({
        notificationText: "Email is blank.",
        notificationType: "danger"
      });

      event.preventDefault();
      return;
    }

    if (this.token == null) {
      this.setState({
        notificationText: "Payment Incomplete.",
        notificationType: "danger"
      });

      event.preventDefault();
      return;
    }

    let data = JSON.stringify({
      first_name: this.first_name.value,
      last_name: this.last_name.value,
      email: this.email.value,
      password: this.password.value,
      address: this.address.value,
      reset_code: this.access_code.value,
      stripe_card: this.token // Changed to just send the id, it's the only information the backend is setup to handle at the moment
    });

    let xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", event => {
      if (event.target.readyState === 4) {
        this.setState({
          setupComplete: true
        });
      }
    });

    xhr.open("POST", "/api/user/setup/");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(data);
  }

  render() {
    return this.state.setupComplete ? (
      <Redirect to={"/user/login"} />
    ) : (
      <form onSubmit={this.handleSubmit}>
        <div className="columns">
          <div className="column is-offset-one-quarter is-half">
            <h1 className="title" style={header}>
              Setup User
            </h1>

            <Notification
              text={this.state.notificationText}
              type={this.state.notificationType}
            />

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="text"
                  placeholder="First Name"
                  ref={input => (this.first_name = input)}
                />
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="text"
                  placeholder="Last Name"
                  ref={input => (this.last_name = input)}
                />
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="email"
                  placeholder="Email"
                  ref={input => (this.email = input)}
                />
                <span className="icon is-small is-left">
                  <i className="fas fa-envelope" />
                </span>
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="text"
                  placeholder="Access Code"
                  ref={input => (this.access_code = input)}
                />
                <span className="icon is-small is-left">
                  <i className="fas fa-key" />
                </span>
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left has-icons-right">
                <input
                  className="input"
                  type="text"
                  placeholder="Address"
                  ref={input => (this.address = input)}
                />
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left">
                <input
                  className="input"
                  type="password"
                  placeholder="Password"
                  ref={input => (this.password = input)}
                />
                <span className="icon is-small is-left">
                  <i className="fas fa-lock" />
                </span>
              </p>
            </div>

            <div className="field">
              <p className="control has-icons-left">
                <input
                  className="input"
                  type="password"
                  placeholder="Confirm Password"
                  ref={input => (this.confirm_password = input)}
                />
                <span className="icon is-small is-left">
                  <i className="fas fa-lock" />
                </span>
              </p>
            </div>

            <StripeCheckout
              stripeKey="pk_test_K6KdPJVX535SygtsR9joQpuQ"
              token={this.onToken}
            />

            <div className="field" style={{ marginTop: "20px" }}>
              <p className="control">
                <input
                  type="submit"
                  value="Finish Setup"
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

export default Setup;
