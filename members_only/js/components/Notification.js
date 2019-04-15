import React, {Component} from "react";

class Notification extends Component {
    render() {
        return this.props.text == "" ? ( <div/> ) : (
            <div className={"notification is-" + this.props.type}>
                <button className="delete"></button>
                {this.props.text}
            </div>
        );
    }
}

export default Notification;