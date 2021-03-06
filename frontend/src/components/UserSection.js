import React, { Component } from "react";
import axios from 'axios';
import $ from 'jquery';
import { Redirect } from 'react-router-dom'

class UserSection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editClicked: false,
      settingsClicked: false,
      viewClicked: false,
      exitClicked: false
    }

    this.onEditClick = this.onEditClick.bind(this);
    this.onSettingsClick = this.onSettingsClick.bind(this);
    this.onViewClick = this.onViewClick.bind(this);
    this.onExitClick = this.onExitClick.bind(this);
    this.handleLogOut = this.handleLogOut.bind(this)
  }

    total_reach(instagram_followers, twitter_followers, youtube_followers){return instagram_followers + twitter_followers + youtube_followers}

    handleLogOut(){

      this.setState({
        username: '',
        password: '',
        login: false,
        signUpSubmit: false,
        forgottenPassword: false,
        resetPasswordSubmitted: false,
        data: {},
        loggedInAs: '',
        activation_token: '',
        activation_user: '',
        reset_token: '',
        reset_uid: '',
        reroute: false,
        signup_load: ''
      })
    }

    onEditClick(){
      this.setState({
        editClicked: true
      })
    }

    onSettingsClick(){
      this.setState({
        settingsClicked: true
      })
    }

    onViewClick(){
      this.setState({
        viewClicked: true
      })
    }

    onExitClick(){
      this.setState({
        exitClicked: true
      })
    }

render(){
  const imageStyle = {backgroundImage: `url(${this.props.data.picture})`}
  var commaNumber = require('comma-number')

    if (this.state.editClicked === true){
     return <Redirect to='/editprofile' data={this.props.data} loggedInAs={this.state.username} login= {true}/>
    }

   if (this.state.settingsClicked === true){
    return <Redirect to='/settings' data={this.props.data} loggedInAs={this.state.username} login= {true}/>
    }

    if (this.state.viewClicked === true){
     return <Redirect to='/profile' data={this.props.data} loggedInAs={this.state.username} login= {true}/>
    }

    if (this.state.exitClicked === true){
     return <Redirect to='/' data={this.props.data} loggedInAs={this.state.username} logout={this.handleLogOut} login= {true}/>
   }
   // TODO: Logout (lines 85-7) is redirecting to Search resuts, NOT logging out




    if (this.props.loggedInAs === ""){
      return <div className="center"> Oops! You need to log in </div>
    }


    else{
      return (

/* USER PROFILE CARD (Start) */
        <div class="user-content">

        <div class="user-card">
        {/* DISPLAY USER PROFILE */}
        <div class="firstinfo">  <img style={imageStyle}></img>
        <div class="userprofileinfo">

          {/* USER NAME  */}
          <h3>{this.props.data.name}</h3>

          {/* USER INFO */}
          <h3>Reach: {commaNumber(this.total_reach(this.props.data.instagram_followers, this.props.data.twitter_followers, this.props.data.youtube_followers))}</h3>
          <p class="bio">Bio: {this.props.data.bio}</p>
          <span> 🌏 Location: {this.props.data.location}</span><br></br>
          <span> 👍🏻 Likes: {this.props.data.likes}</span><br></br>
          <span> 👎🏻 Dislikes: {this.props.data.greetings}</span><br></br>
          <span> 💚 Matches: 3</span>
        </div>
        </div>
        </div>

        {/* USER TOOLBAR  */}
        <div class="badgescard">
          <span class="devicons devicons-django"><input type='image' src="/images/app_images/editicon.svg" width="40" height="40" onClick={this.onEditClick}></input></span>

          <span class="devicons devicons-python"><input type='image' src="/images/app_images/viewicon.svg" width="40" height="40" onClick={this.onViewClick}></input></span>

          <span class="devicons devicons-codepen"><input type='image' src="/images/app_images/settingicon.svg" width="40" height="40" onClick={this.onSettingsClick}></input></span>

          <span class="devicons devicons-codepen"><input type='image' src="/images/app_images/exiticon.svg" width="40" height="40" onClick={this.onExitClick}></input></span>
          {/* TODO: The last of these <spans> above needs to log user out, i.e onExitClick needs amending */}
        </div>
        </div>
// {/* USER PROFILE CARD (End) */}









          /* <div class="usericons">
            <ul>
              <li className="userbutton">
                <input type='image' src="/images/app_images/editicon.svg" width="40" height="40" onClick={this.onEditClick}></input>
              </li>
              <li className="userbutton">
                <input type='image' src="/images/app_images/viewicon.svg" width="40" height="40" onClick={this.onViewClick}></input>
              </li>
              <li className="userbutton">
                <input type='image' src="/images/app_images/settingicon.svg" width="40" height="40" onClick={this.onSettingsClick}></input>
           */








  )
}


}

}

export default UserSection;
