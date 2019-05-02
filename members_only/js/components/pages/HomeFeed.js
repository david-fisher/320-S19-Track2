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
        return (
            <div>
                <h1 className="title" style={feedHeader}>Feed</h1>

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

                <DataProvider {...this.props} postNotification={this.state.notificationText} endpoint="/api/post/" callerType="HomeFeed" token={this.props.token} render={
                    data => this.state.data
                } />

                <div className="w3-container w3-card w3-white w3-round w3-margin">
                    <span style={{ 'margin-top': '10px' }} className="w3-right w3-opacity">1 min ago</span>
                    <div style={{ 'display': 'flex', 'align-items': 'flex-start'}}>
                        <h4 style={{ 'border-radius': '25px', 'background-color': 'steelblue', 'color': 'white', 'padding-left': '15px', 'padding-top': '5px', 'padding-bottom': '5px', 'padding-right': '15px', 'margin-top': '10px' }} >John Doeeeeeeeeeeeee</h4>
                    </div>
                    <p style={{ 'margin-left': '25px', 'margin-top': '5px', 'padding-left': '5px' }}>DAE fortnite burger?</p>
                    <hr class="w3-clear"></hr>

                    <form>
                        <textarea type="text" style={{ 'resize': "none", 'width': "75%" }} className="w3-border w3-padding" placeholder="Leave a comment!"></textarea>
                        <br></br>
                        <button style={{ 'color': 'white', 'background-color': 'DarkSlateGray', 'margin-left': "0px", 'margin-top': "10px", 'margin-bottom': "30px" }} type="submit" className="w3-button w3-theme-d2 w3-margin-bottom"><i style={{'color':'white'}} className="fa fa-comment"></i> Comment</button>
                    </form>
                </div>


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
