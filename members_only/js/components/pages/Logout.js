import React, {Component} from 'react';
import { Route, Redirect} from 'react-router'
import Cookies from 'universal-cookie';

class Logout extends Component {
    constructor(props) {
        super(props);

        const cookies = new Cookies();
        let token = cookies.remove('user_token');

        this.props.updateToken(null);
    }

    render() {
        return (
                <Redirect to="/"/>
        );
    }
}

export default Logout;
