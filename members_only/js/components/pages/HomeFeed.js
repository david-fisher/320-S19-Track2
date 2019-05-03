import React, { Component } from 'react';
import DataProvider from "../DataProvider";
import Table from "../Table";
import Notification from "../Notification";
import './frontend_style.css'

class HomeFeed extends Component {
    constructor(props) {
        super(props);

        this.state = {
            notificationText: "",
            notificationType: "success",
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    state = {
        data: {
            "user": null,
            "content": null,
            "urls": null,
            "is_flagged": false,
            "by_admin": false
        }
    };

    curFirstname = "";
    curLastname = "";

    handleSubmit(event) {
        event.preventDefault();

        this.state.data = JSON.stringify({
          "user": this.props.userID,
          "content": this.post.value,
          "urls": null,
          "is_flagged": false,
          "by_admin": false
        });
        this.curFirstname = this.props.firstName;
        this.curLastname = this.props.lastName;

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
        //console.log(this.props.userID);

        xhr.open("POST", "/api/post/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("cache-control", "no-cache");
        xhr.setRequestHeader("Authorization", "Token " + this.props.token);

        xhr.send(this.state.data);

    }

    //currentPage = 1;
    //baseEndpoint = "/api/post/";

    //nextPage = () => {
    //    //this.currentPage += 1;
    //    //this.setState({});
    //    //this.forceUpdate();
    //    //return <DataProvider {...this.props} postNotification={this.state.notificationText} endpoint={this.baseEndpoint + "?page=" + this.currentPage} callerType="HomeFeed" token={this.props.token} render={
    //    //    data => this.state.data
    //    //} />
    //}

    render() {
        //console.log("rendering main");
        //let endpointString = "/api/post/?page=" + this.currentPage;
        //console.log("current page: main: " + this.currentPage);
        //let test = [1,2,3]
        return (
            <div>
                <h1 className="title" style={feedHeader}>Feed</h1>

                <Notification text={this.state.notificationText} type={this.state.notificationType} />

                <form onSubmit={this.handleSubmit}>
                    <div className="field">
                        <p className="control">
                            <textarea style={{ 'resize': "none"}} className="textarea" placeholder="Write your post here."
                                   ref={(input) => this.post = input}/>
                        </p>
                    </div>
                    <div className="field">
                        <p className="control">
                            <input type="submit" value="Post" className="button is-success"/>
                        </p>
                    </div>
                </form>

                <DataProvider {...this.props} postNotification={this.state.notificationText} endpoint="/api/post/" blockedMembers={this.props.blockedMembers} callerType="HomeFeed" token={this.props.token} render={
                    data => this.state.data
                } />

            </div>
        );
    }
}

const feedHeader = {
    marginTop: '40px',
    fontVariant: 'small-caps',
    fontSize: '40px'
};

export default HomeFeed;
