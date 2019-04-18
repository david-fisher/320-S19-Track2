import React, {Component} from 'react';
import {Link, NavLink} from "react-router-dom";

class Navbar extends Component {
    render() {
        return this.props.loggedIn ? (
            <nav className="navbar" role="navigation" aria-label="main navigation">
                <div className="navbar-brand">
                    <Link to="/" className="navbar-item">
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

                        <NavLink to="/user/invite" className="navbar-item">
                            Invite
                        </NavLink>

                        <a href="/api" className="navbar-item">
                            API Documentation
                        </a>
                    </div>

                    <div className="navbar-end">
                        <div className="navbar-item">
                            <div className="buttons">
                                <Link to="/user/logout" className="button is-light">
                                    Log out
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        ) : (
            <nav className="navbar" role="navigation" aria-label="main navigation">
                <div className="navbar-brand">
                    <Link to="/" className="navbar-item">
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

                        <a href="/api" className="navbar-item">
                            API Documentation
                        </a>
                    </div>

                    <div className="navbar-end">
                        <div className="navbar-item">
                            <div className="buttons">
                                <Link to="/user/login" className="button is-light">
                                    Log In
                                </Link>
                            </div>
                        </div>
                        <div className="navbar-item">
                            <div className="buttons">
                                <Link to="/user/setup" className="button is-light">
                                    Sign Up
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        );
    }
}

export default Navbar;
