import React, {Component} from 'react';
import DataProvider from "../DataProvider";
import Table from "../Table";
import Notification from "../Notification";

class Feed extends Component {
    constructor(props) {
        super(props);

        this.state = {
            notificationText: "",
            notificationType: "success",
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();

        let data = JSON.stringify({
          "user": this.props.userID,
          "content": this.post.value,
          "urls": null,
          "is_flagged": false,
          "by_admin": false
        });

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", (event) => {
          if (event.target.readyState === 4) {
            console.log(this.responseText);

            this.setState({
                notificationText: "Created Post: " + this.post.value
            });

            this.post.value = '';
          }
        });

        xhr.open("POST", "/api/post/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("cache-control", "no-cache");
        xhr.setRequestHeader("Authorization", "Token " + this.props.token);

        xhr.send(data);

    }

    render() {
        return (
            <div>
                <h1 className="title">Feed</h1>

                <Notification text={this.state.notificationText} type={this.state.notificationType} />

                <form onSubmit={this.handleSubmit}>
                    <div className="field">
                        <p className="control">
                            <textarea className="textarea" placeholder="Write your post here."
                                   ref={(input) => this.post = input}/>
                        </p>
                    </div>
                    <div className="field">
                        <p className="control">
                            <input type="submit" value="Post" className="button is-success"/>
                        </p>
                    </div>
                </form>

                <DataProvider postNotification={this.state.notificationText} endpoint="/api/post/" token={this.props.token} render={data => <Table data={data}/>}/>
            </div>
        );
    }
}

export default Feed;
