import React, { Component } from 'react';
import Table from "../Table";
import Notification from "../Notification";
import './frontend_style.css'

class Profile extends Component {
    constructor(props) {
        super(props);

        this.state = {
            profile: {}
        };
        
        this.getInfo = this.getInfo.bind(this);
        this.getInfo();
    }

    getInfo() {
        let xhr = new XMLHttpRequest();

        xhr.open("GET", "/api/user/current_user/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.addEventListener("readystatechange", (event) => {
          if (event.target.readyState === 4) {
              let obj = JSON.parse(event.target.response);
              let d = (new Date(obj.date_create)).toString();
              obj.date_create = d.split(" ").slice(0, 4).join(" ");
              obj.blocked_members = obj.blocked_members.length;
              this.setState({ profile: obj });
              console.log(this.state);
            }
        });
        
        xhr.send();
    }
    
    render() {
        return (
            <div>
                <h1 className="title" style={profileHeader}>{this.state.profile.first_name} {this.state.profile.last_name}</h1>

                <img src="http://www.personalbrandingblog.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png" />
                
                <h3><b>Email:</b> {this.state.profile.email}</h3>
                <h3><b>Username:</b> {this.state.profile.username}</h3>
                <h3><b>Points:</b> {this.state.profile.points}</h3>
                <h3><b>Birthday:</b> {this.state.profile.birthday}</h3>
                <h3><b>Number of Blocked Members:</b> {this.state.profile.blocked_members}</h3>
                <h3><b>Invited By:</b> {this.state.profile.invited_by}</h3>
                <h3><b>Date Joined:</b> {this.state.profile.date_create}</h3>
            </div>
        );
    }
}

const profileHeader = {
    marginTop: '40px',
    fontVariant: 'small-caps',
    fontSize: '40px'
};

export default Profile;
