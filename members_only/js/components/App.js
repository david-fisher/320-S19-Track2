import React, {Component} from 'react';
import ReactDOM from "react-dom";
import {BrowserRouter as Router, Route, Link, NavLink} from 'react-router-dom';
import Login from "./pages/Login";
import Navbar from "./Navbar";
import Feed from "./pages/Feed";
import Home from "./pages/Home";
import Cookies from "universal-cookie";
import Logout from "./pages/Logout";
import Invite from "./pages/Invite";
import Setup from "./pages/Setup";


class App extends Component {
    constructor(props) {
        super(props);

        const cookies = new Cookies();
        let token = cookies.get('user_token');

        if (token == null) {
            this.state = {
                token: null,
                logged_in: false,
            }
        } else {
            this.state = {
                token: token,
                logged_in: true,
            }
        }
    }

    updateToken(token) {
        if (token == null) {
            this.setState({
                token: null,
                logged_in: false,
            });
        } else {
            fetch('/api/user/current_user/', {
                headers: new Headers({'Authorization': 'Token ' + token}),
            })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }

                return response.json();
            })
            .then(data => this.setState({user_id: data.id, token: token, logged_in: true}));
        }
    }

    render() {
        return this.state.logged_in ? (
            <Router>
                <div className="App">
                    <Navbar loggedIn={this.state.logged_in}/>

                    <div className="section">
                        <div className="container">
                            <Route exact path="/" component={Home}/>
                            <Route exact path="/user/invite"
                                   render={
                                       (props) => <Invite {...props} token={this.state.token}/>
                                   }/>
                            <Route exact path="/feed"
                                   render={
                                       (props) => <Feed {...props} userID={this.state.user_id} token={this.state.token}/>
                                   }/>
                            <Route exact path="/user/logout"
                                   render={
                                       (props) => <Logout {...props} updateToken={this.updateToken.bind(this)}/>
                                   }/>
                            <Route exact path="/user/login"
                                   render={
                                       (props) => <Login {...props} updateToken={this.updateToken.bind(this)}/>
                                   }/>
                        </div>
                    </div>

                </div>
            </Router>
        ) : (
            <Router>
                <div className="App">
                    <Navbar loggedIn={this.state.logged_in}/>

                    <div className="section">
                        <div className="container">
                            <Route exact path="/" component={Home}/>
                            <Route exact path="/user/login"
                                   render={
                                       (props) => <Login {...props} updateToken={this.updateToken.bind(this)}/>
                                   }/>
                            <Route exact path="/user/setup" component={Setup}/>
                        </div>
                    </div>

                </div>
            </Router>
        );
    }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App/>, wrapper) : null;
