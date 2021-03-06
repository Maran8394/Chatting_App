import React from "react";
import { Spin, Icon } from "antd";
import { connect } from "react-redux";
import * as actions from "../store/actions/auth";
import * as navActions from "../store/actions/nav";
import * as messageActions from "../store/actions/message";
import UserProfile from "./User_profile";
import { HOST_URL } from "../settings";
import axios from 'axios';
import "babel-polyfill";
import Sample from "./Sample";


const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin />;

class Sidepanel extends React.Component {
  state = {
    loginForm: true,
    user:{},
    friend : {},
    
  };

  

  waitForAuthDetails() {
    const component = this;
    setTimeout(function() {
      if (
        component.props.token !== null &&
        component.props.token !== undefined
      ) {
        component.props.getUserChats(
          component.props.username,
          component.props.token
        );
        return;
      } else {
        console.log("waiting for authentication details...");
        component.waitForAuthDetails();
      }
    }, 100);
  }

  


  componentDidMount() {
    this.waitForAuthDetails();
  
    axios.get(`${HOST_URL}/chat/profile/${localStorage.getItem('username')}`)
    .then(res => {
      const user = res.data;
      this.setState({ user });
    })

  }

  openAddChatPopup() {
    this.props.addChat();
  }



  changeForm = () => {
    this.setState({ loginForm: !this.state.loginForm });
  };

  authenticate = e => {
    e.preventDefault();
    if (this.state.loginForm) {
      this.props.login(e.target.username.value, e.target.password.value);
    } else {
      this.props.signup(
        e.target.username.value,
        e.target.email.value,
        e.target.password.value,
        e.target.password2.value
      );
    }
  };


  render() {

    let activeChats = this.props.chats.map(c => {
            var arr = c.participants;
            var indexOf_user = arr.indexOf(this.props.username);
            arr.splice(indexOf_user,1);
            if(this.props.isAuthenticated){
              return (          
                <Sample
                key={c.id}
                  name={arr}
                  picURL="http://emilcarlsson.se/assets/louislitt.png"
                  status="online"
                  chatURL={`/${c.id}`}
                  />
              );
  }
    });
    return (
      <div id="sidepanel">
        <div id="profile">
          <div className="wrap">
            {this.props.isAuthenticated?(
            <UserProfile name={this.state.user.username}
            profile_pic = {this.state.user.profile_pic}
            status = {this.state.user.status}
             />)
            :(<UserProfile
              profile_pic={"/media/profile_pics/dummyImage.jpg"}
              status={"offline"} />)}
            <div id="expanded">
              {this.props.loading ? (
                <Spin indicator={antIcon} />
              ) : this.props.isAuthenticated ? (
                <button onClick={() => this.props.logout()} className="authBtn">
                  <span>Logout</span>
                </button>
              ) : (
                <div>
                  <form method="POST" onSubmit={this.authenticate}>
                    {this.state.loginForm ? (
                      <div>
                        <input
                          name="username"
                          type="text"
                          placeholder="username"
                        />
                        <input
                          name="password"
                          type="password"
                          placeholder="password"
                        />
                      </div>
                    ) : (
                      <div>
                        <input
                          name="username"
                          type="text"
                          placeholder="username"
                        />
                        <input name="email" type="email" placeholder="email" />
                        <input
                          name="password"
                          type="password"
                          placeholder="password"
                        />
                        <input
                          name="password2"
                          type="password"
                          placeholder="password confirm"
                        />
                      </div>
                    )}

                    <button type="submit">Authenticate</button>
                  </form>

                  <button onClick={this.changeForm}>Switch</button>
                </div>
              )}
            </div>
          </div>
        </div>
        {/* <div id="search">
          <label htmlFor="">
            <i className="fa fa-search" aria-hidden="true" />
          </label>
           <input type="text" placeholder="Search Chats..." /> 
        </div> */}
        <div id="contacts">
          <ul>{activeChats}</ul>
        </div>
        <div id="bottom-bar">
          <button id="addChat" onClick={() => this.openAddChatPopup()}>
            <i className="fa fa-user-plus fa-fw" aria-hidden="true" />
            <span>Create chat</span>
          </button>
          <button id="settings">
            <i className="fa fa-cog fa-fw" aria-hidden="true" />
            <span>Settings</span>
          </button>
          
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    isAuthenticated: state.auth.token !== null,
    loading: state.auth.loading,
    token: state.auth.token,
    username: state.auth.username,
    chats: state.message.chats
  };
};

const mapDispatchToProps = dispatch => {
  return {
    login: (userName, password) =>
      dispatch(actions.authLogin(userName, password)),
    logout: () => dispatch(actions.logout()),
    signup: (username, email, password1, password2) =>
      dispatch(actions.authSignup(username, email, password1, password2)),
    addChat: () => dispatch(navActions.openAddChatPopup()),
    getUserChats: (username, token) =>
      dispatch(messageActions.getUserChats(username, token))
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Sidepanel);