import React, {Component} from "react";

class Notification extends Component {

    //tempText = ""
    shouldHide = false;

    constructor(props) {
        super(props);
        //this.tempText = props.text;
    }

    deleteNotification = () => {
        this.shouldHide = true;
        //this.tempText = "";
        //this.setState({});
        //this.forceUpdate();
    }

    render() {

        if (this.props.text == "" || this.shouldHide) {
            this.shouldHide = false;
            return (<div />)
        }

        return (
            <div className={"notification is-" + this.props.type}>
                <button onClick={this.deleteNotification} className="delete"></button>
                {this.props.text}
            </div>
        );
    }
}

export default Notification;