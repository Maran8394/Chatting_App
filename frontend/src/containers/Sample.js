import Axios from "axios";
import React from "react";
import { HOST_URL } from "../settings";
import Contact from "../components/Contact";

class Sample extends React.Component{
    state = {
        friend:{}
    }

    

    render(){
        Axios.get(`${HOST_URL}/chat/profile/${this.props.name}`)
        .then(res =>{
            this.setState({friend:res.data})
        })
        return(
            <Contact
                  name={this.state.friend.username}
                  picURL={HOST_URL + this.state.friend.profile_pic}
                  status={this.state.friend.status}
                  chatURL={this.props.chatURL}
                />
        )
    }
}
export default Sample;