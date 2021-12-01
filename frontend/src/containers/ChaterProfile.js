import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import Hoc from "../hoc/hoc";
import Axios from "axios";
import { HOST_URL } from "../settings";



class Profile extends React.Component {
  state = {
    user:{}
  }
  
  render(props) {
    if (this.props.token === null) {
      return <Redirect to="/" />;
    }              
    Axios.get(`${HOST_URL}/chat/profile/${this.props.name}`)
        .then(res =>{
            this.setState({user:res.data})
        })
console.log(this.state)
    return (
      <div className="contact-profile">
        {this.props.username !== null ? (
          <Hoc>
            <img src={HOST_URL + this.state.user.profile_pic} alt="" />
            <p>{this.props.name}</p>
            <div className="social-media">
              <i className="fa fa-facebook" aria-hidden="true" />
              <i className="fa fa-twitter" aria-hidden="true" />
              <i className="fa fa-instagram" aria-hidden="true" />
            </div>
          </Hoc>
        ) : null} 
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    username: state.auth.username,
    token: state.auth.token
  };
};

export default connect(mapStateToProps)(Profile);