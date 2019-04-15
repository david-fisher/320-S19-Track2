import React, {Component} from 'react';
import Notification from "../Notification";

class Invite extends Component {

    constructor(props) {
        super(props);

        this.state = {
            notificationText: "",
            notificationType: "success",
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        let data = JSON.stringify({
            "username": this.email.value,
            "email": this.email.value,
        });

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", (event) => {
          if (event.target.readyState === 4) {
            console.log(this.responseText);

            this.setState({
                notificationText: "Invite sent."
            });
          }
        });

        xhr.open("POST", "http://127.0.0.1:8000/api/user/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("cache-control", "no-cache");
        xhr.setRequestHeader("Authorization", "Token " + this.props.token);

        xhr.send(data);

        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <div className="columns">
                    <div className="column is-offset-one-quarter is-half">
                        <h1 className="title">Invite User</h1>

                        <Notification text={this.state.notificationText} type={this.state.notificationType} />

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
                            <p className="control">
                                <input type="submit" value="Invite" className="button is-success"/>
                            </p>
                        </div>
                    </div>
                </div>
            </form>
        );
    }
}

export default Invite;
