import React, {Component} from "react";
import PropTypes from "prop-types";

class DataProvider extends Component {
    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        render: PropTypes.func.isRequired,
        token: PropTypes.string.isRequired
    };

    state = {
        data: [],
        loaded: false,
        placeholder: "Loading...",
        time: Date.now()
    };

    loadData() {
        fetch(this.props.endpoint, {
            headers: new Headers({'Authorization': 'Token ' + this.props.token}),
        })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }

                return response.json();
            })
            .then(data => this.setState({data: data, loaded: true}));
    }

    componentWillMount() {
        this.loadData();
    }

    componentDidUpdate(prevProps) {
      if (this.props.postNotification !== prevProps.postNotification) {
        this.loadData();
      }
    }

    render() {
        const {data, loaded, placeholder} = this.state;
        console.log(data);
        return loaded ? this.props.render(data.results) : <p>{placeholder}</p>;
    }
}

export default DataProvider;