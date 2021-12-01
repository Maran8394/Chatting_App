import React from 'react';
import { HOST_URL } from "../settings";
import axios from 'axios';


class UserProfile extends React.Component{

  state = {
    user :{}
  }

  

  render(){
    let s = document.getElementsByClassName("status")
    return (
      <div>
          <img
            id="profile-img"
            src={HOST_URL+this.props.profile_pic}
            className={this.props.status}
            alt="profile picture"
          />
          <p>{localStorage.getItem('username')}</p>
          <div id="status-options">
            <ul>
              <li id="status-online" className="active">
                <span className="status-circle" /> <p className="status">Online</p>
              </li>
              <li id="status-away">
                <span className="status-circle" /> <p className="status">Away</p>
              </li>
              <li id="status-busy">
                <span className="status-circle" /> <p className="status">Busy</p>
              </li>
              <li id="status-offline">
                <span className="status-circle" /> <p className="status">Offline</p>
              </li>
            </ul>
          </div>
      </div>
  )
  }
}
export default UserProfile
