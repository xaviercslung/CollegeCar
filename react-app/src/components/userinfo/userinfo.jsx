import React, {Component, Fragment} from 'react';

import tempImg from './tempuser.png';
import birds from './birds.JPG';
import './userinfo.css'
import nik from './nik.JPG';
import withAuth from '../withAuth';
import {withRouter} from 'react-router';

//https://www.w3schools.com/cssref/css_selectors.asp

class UserInfo extends Component{

    render(){
        return(
            <Fragment>
                <div className="row">
                    <div class="content-profile-page">
                        <div class="profile-user-page card">
                            <div class="img-user-profile">
                                <img class="img-fluid profile-bgHome" src={birds} />
                                <img class="img-fluid avatar" src={nik} alt="allan"/>
                            </div>
                            <button className="btn">Add Friend</button>
                            <div class="user-profile-data">
                                <h1>Nik Burmeister</h1>
                                <p>"Put a Quote that you like here"</p>
                            </div> 
                            <div class="description-profile">Give a little description of yourself</div>
                            <ul class="data-user">
                                <li><a><strong>2.0</strong><span>GPA</span></a></li>
                                <li><a><strong>69</strong><span>Failed Classes</span></a></li>
                                <li style={{"border-right": "0.1em solid transparent" }}><a><strong>100</strong><span>Keepin it Real Score</span></a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div className="row justify-content-center">
                    <div className="user-activity">
                            <div className="col" align="center">
                                <a class="" data-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">
                                    User Information
                                    <p><i class="fa fa-angle-double-up" style={{"-moz-transform": "scale(3.5,-1.4)"}}></i></p>
                                </a>
                            </div>
                        <div class="collapse user-details" id="collapseExample">
                            <div class="card card-body">
                                <hr></hr>
                                <p>
                                    <b>Name:</b> Nik Burmeister
                                </p>
                                <hr></hr>
                                <p>
                                    <b>Username:</b> FiftyFifty
                                </p>
                                <hr></hr>
                                <p>
                                    <b>Age:</b> 23
                                </p>
                                <hr></hr>
                                <p>
                                    <b>Joined:</b> 7/5/2019
                                </p>
                                <hr></hr>
                                <p>
                                    <b>Email:</b> fakeemail@fakesite.com
                                </p>
                                <hr></hr>
                                <p>
                                    <b>Educational Attainment:</b>
                                </p>
                             </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="user-activity">
                        <h2>User activity</h2>
                        
                            <div className="card shadow margined rss-card">
                                <div className="container-fluid row" style={{ "height": "100%" }}>
                                    <div className="col d-flex align-items-center justify-content-center image-col">
                                        <img class="img-fluid rounded-circle comment-img" src={nik} alt="nik" />
                                    </div>
                                    <div className="col contentBar cutLink">
                                        "UW-Madison is in Madison, WI. It is cold AF for about 8 out of the 12 months. However, July and August are quite pleasant."
                                    </div>
                                </div>
                            </div>
                        
                    </div>
                </div>
            </Fragment>
            
            
        );
    }

}

export default UserInfo;