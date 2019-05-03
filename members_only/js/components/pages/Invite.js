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

            var jsonResponse = JSON.parse(xhr.responseText);

            if(jsonResponse.success){
                this.setState({
                    notificationText: "Invite sent.",
                    notificationType: "success"
                });
            }else{
                this.setState({
                    notificationText: "Not enough points.",
                    notificationType: "danger",
                });
            }

          }
        });

        xhr.open("POST", "/api/user/");
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
                        <h1 className="title" style = {header}>Invite User</h1>

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

const header = {
    marginTop: '40px',
    fontVariant: 'small-caps',
    fontSize: '40px'
};

export default Invite;
