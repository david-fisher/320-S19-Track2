import React, {Component} from 'react';
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import {BrowserRouter as Router, Route, Link, NavLink} from 'react-router-dom';

const Home = () => (
    <div>
        Homepage.
    </div>
)

const Feed = () => (
    <div>
        <DataProvider endpoint="api/post/" render={data => <Table data={data}/>}/>
    </div>
)

class App extends Component {
    render() {
        return (
            <Router>
                <div className="App">
                    <nav className="navbar" role="navigation" aria-label="main navigation">
                        <div className="navbar-brand">
                            <Link className="navbar-item" href="/">
                                Members Only
                            </Link>

                            <a role="button" className="navbar-burger burger" aria-label="menu" aria-expanded="false"
                               data-target="navbarBasicExample">
                                <span aria-hidden="true"></span>
                                <span aria-hidden="true"></span>
                                <span aria-hidden="true"></span>
                            </a>
                        </div>

                        <div id="navbarBasicExample" className="navbar-menu">
                            <div className="navbar-start">
                                <NavLink to="/" className="navbar-item">
                                    Home
                                </NavLink>

                                <NavLink to="/feed" className="navbar-item">
                                    Feed
                                </NavLink>

                                <a href="/api" className="navbar-item">
                                    API Documentation
                                </a>
                            </div>

                            <div className="navbar-end">
                                <div className="navbar-item">
                                    <div className="buttons">
                                        <a className="button is-primary">
                                            <strong>Sign up</strong>
                                        </a>
                                        <a className="button is-light">
                                            Log in
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </nav>

                    <div className="container">
                        <Route exact path="/" component={Home}/>
                        <Route exact path="/feed" component={Feed}/>
                    </div>

                </div>
            </Router>
        );
    }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App/>, wrapper) : null;
