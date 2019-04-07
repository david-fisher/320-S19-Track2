import React, {Component} from 'react';
import { Route, Redirect} from 'react-router'
import Cookies from 'universal-cookie';

class Login extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            logged_in: false
        }
    }

    handleSubmit(event) {
        let data = JSON.stringify({
            "username": this.email.value,
            "password": this.password.value,
        });

        let xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", (event) => {
          if (event.target.readyState === 4) {
              let response_data = JSON.parse(event.target.responseText);

              const cookies = new Cookies();
              cookies.set('user_token', response_data.token, {path: "/"});

              this.setState({
                  logged_in: true
              })

              this.props.updateToken(response_data.token);
          }
        });

        xhr.open("POST", "/api-token-auth/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("cache-control", "no-cache");

        xhr.send(data);

        event.preventDefault();
    }

    render() {
        return this.state.logged_in ?
            (
                <Redirect to="/"/>
            )
            : (
            <form onSubmit={this.handleSubmit}>
                <div className="columns">
                    <div className="column is-offset-one-quarter is-half">
                        <h1 className="title">Login</h1>

                        <div className="field">
                            <p className="control has-icons-left has-icons-right">
                                <input className="input" type="email" placeholder="Email"
                                       ref={(input) => this.email = input}/>
                                <span className="icon is-small is-left">
                          <i className="fas fa-envelope"></i>
                        </span>
                            </p>
                        </div>
                        <div className="field">
                            <p className="control has-icons-left">
                                <input className="input" type="password" placeholder="Password"
                                       ref={(input) => this.password = input}/>
                                <span className="icon is-small is-left">
                          <i className="fas fa-lock"></i>
                        </span>
                            </p>
                        </div>
                        <div className="field">
                            <p className="control">
                                <input type="submit" value="Login" className="button is-success"/>
                            </p>
                        </div>
                    </div>
                </div>
            </form>
        );
    }
}

export default Login;
