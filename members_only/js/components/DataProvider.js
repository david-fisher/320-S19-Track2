import React, {Component} from "react";
import PropTypes from "prop-types";
import './pages/frontend_style.css'
import Notification from "./Notification";

class DataProvider extends Component {

    // temp variables to handle posts
    postIter = -1;
    tempUserCache = [];

    tempAllComments = [];
    commentPageIter = 1;
    tempIter = 0;

    currentPage = 1;

    constructor(props) {
        super(props);
    }

    static propTypes = {
        endpoint: PropTypes.string.isRequired,
        render: PropTypes.func.isRequired,
        token: PropTypes.string.isRequired,
        callerType: PropTypes.string.isRequired
    };

    state = {
        data: [],
        blocked_members: [],
        callerType: "hoi",
        loaded: false,
        placeholder: "Loading...",
        time: Date.now()
    };

    ass = () => {
        return "hi";
    }

    loadCommentPage = () => {
        fetch("/api/comment/?page=" + this.commentPageIter, {
            headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
        })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: "Something went wrong" });
                }

                return response.json();
            })
    }

    loadData() {
        if (this.props.callerType == "HomeFeed") {
            fetch(this.props.endpoint + "?page=" + this.currentPage, {
                headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
            })
                .then(response => {
                    if (response.status !== 200) {
                        return this.setState({ placeholder: "Something went wrong" });
                    }

                    return response.json();
                })
                .then(data => { if (this.tempUserCache.length <= 0) { this.getUsers(); } this.setState({ blocked_members: this.props.blockedMembers, data: data, loaded: true, callerType: this.props.callerType }) });


            let temp = fetch("/api/comment/?page=" + this.commentPageIter, {
                headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
            }).then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: "Something went wrong" });
                }

                return response.json();
                }).then(data => {
                    //console.log(data);
                    //console.log(data['count']);
                    let tempCommentNum = data['count'];
                    if (tempCommentNum === this.tempAllComments.length) {
                        return;
                    }

                    this.tempIter = 0;
                    this.tempAllComments = []; //wipe to reset

                    if (this.tempIter < tempCommentNum) { //go through every single comment
                        console.log("currently tempiter is " + this.tempIter + " and num to reach is " + tempCommentNum);
                        fetch("/api/comment/?page=" + this.commentPageIter, {
                            headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
                        }).then(response => {
                            if (response.status !== 200) {
                                return this.setState({ placeholder: "Something went wrong" });
                            }

                            return response.json();
                            }).then( innerData => {

                                for (let i = 0; i < innerData.results.length; i++) { //for every comment on that page
                                    console.log("found a comment, adding!");
                                    this.tempIter += 1;
                                    this.tempAllComments.push(innerData.results[i]);
                                }
                                this.commentPageIter += 1; //increment page and continue until count is filled.

                            });

                    }

                });

            //let temp = this.loadCommentPage();
            //temp.then(response => {
            //    console.log(response);
            //    console.log("^ :)");
            //});
            //let temp2 = this.ass();
            //console.log(temp);
            //console.log(temp2);
        //this.loadCommentPage().then( tempCommentPage => {
        //    let tempCommentNum = tempCommentPage['count'];
        //    if(tempCommentNum === this.tempAllComments.length) {
        //        return;
        //    }
        //    let tempIter = 0;
        //    this.tempAllComments = []; //wipe to reset
        //    while (tempIter < tempCommentNum) { //not sure how fucked waiting for fetches will be
        //        //let tempCommentPage3 = this.loadCommentPage();
        //        break;

        //        //    .then(response => {
        //        //    for (let i = 0; i < response.results.length; i++) { //for every comment on that page
        //        //        tempIter += 1;
        //        //        this.tempAllComments.push(response.results[i]);
        //        //    }
        //        //    this.commentPageIter += 1; //increment page and continue until count is filled.
        //        //});
        //        //let tempPageResults = this.loadCommentPage().results; //wait for it?
        //        //for (let i = 0; i < tempPageResults.length; i++) { //for every comment on that page
        //        //    tempIter += 1;
        //        //    this.tempAllComments.push(tempPageResults[i]);
        //        //}
        //        //this.commentPageIter += 1; //increment page and continue until count is filled.
        //    }
        //});

        } else {
            fetch(this.props.endpoint, {
                headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
            })
                .then(response => {
                    if (response.status !== 200) {
                        return this.setState({ placeholder: "Something went wrong" });
                    }

                    return response.json();
                })
                .then(data => { this.setState({ data: data, loaded: true, callerType: this.props.callerType }) });
        }
    }

    getUsers = () => {
        fetch('/api/user/', {
            headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
        })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: "Something went wrong" });
                }
                return response.json();
            })
            .then(
            data => {
                this.tempUserCache = data.results;
                this.setState({}); //empty refesh
            }
        );
                    
    }
        
    componentWillMount() {
        this.loadData();
    }

    componentDidUpdate(prevProps) {

      if (this.props.postNotification !== prevProps.postNotification) {
        this.loadData();
      }
    }


    renderPost = () => {
        const { data, blocked_members } = this.state;

        let postIter2 = this.postIter + 1;
        this.postIter += 1;

        if (postIter2 < 0 || postIter2 >= data.results.length) {
            return <p></p>
        }

        console.log(blocked_members);
        let tempUserId = data.results[postIter2]['user'];
        if (blocked_members != undefined) {
            for (let i = 0; i < blocked_members.length; i++) { //check for blocked members
                if (tempUserId === blocked_members[i]) {
                    return <div className="w3-container w3-card w3-white w3-round w3-margin">
                        ==== BLOCKED POST ====
                </div>
                }
            }
        }

        let emailCheck = (this.tempUserCache.length - data.results[postIter2]['user']);
        let tempEmail = "_loading_"; //placeholders while API loads /api/users/
        let tempName = "_loading_";
        if (emailCheck >= 0) { //email check is basically universal
            let relevantUser = this.tempUserCache[this.tempUserCache.length - data.results[postIter2]['user']];
            //^ gets the appropriate user data from api/users/ for the guy who made the post
            tempEmail = relevantUser['email'];
            tempName = relevantUser['first_name'] + " " + relevantUser['last_name'];
        }
        let tempCreated = data.results[postIter2]['date_created'];
        let timeArray = tempCreated.split('-').join(',').split('T').join(',').split(':').join(',').split(',');
        let tempContent = data.results[postIter2]['content'];
        //TODO: if content has #, make the text after it until a space is reached blue
        //if (tempContent.includes('#')) {
        //}



        //console.log(timeArray);

        //todo: add block user button. 

        return <div>
            <div className="w3-container w3-card w3-white w3-round w3-margin">
                <span style={{ 'margin-top': '10px' }} className="w3-right w3-opacity">{timeArray[1] + "/" + timeArray[2] + "/" + timeArray[0] + " at " + timeArray[3] + ":" + timeArray[4]}</span>
                <div style={{ 'display': 'flex', 'align-items': 'flex-start' }}>
                    <h4 style={{ 'border-radius': '25px', 'background-color': 'steelblue', 'color': 'white', 'padding-left': '15px', 'padding-top': '5px', 'padding-bottom': '5px', 'padding-right': '15px', 'margin-top': '10px' }} >{tempName}</h4>
                    <div style={{ 'float':'right', 'margin-left': '5px', 'margin-top': '0px' }} className="w3-half">
                        <button style={{ 'color': 'black', 'padding-right': '2px', 'padding-left': '2px', 'margin': '0px', 'width': '15%', 'border-radius': '15px' }} class="w3-button w3-block w3-red w3-section" title="Block User"><i style={{'color':'white'}} >Block</i></button>
                    </div>
                </div>
                <p style={{ 'word-wrap': 'break-word','margin-left': '25px', 'margin-top': '5px', 'padding-left': '5px' }}>{data.results[postIter2]['content']}</p>
                <hr class="w3-clear"></hr>

                <form>
                    <textarea type="text" style={{ 'resize': "none", 'width': "75%" }} className="w3-border w3-padding" placeholder="Leave a comment!"></textarea>
                    <br></br>
                    <button style={{ 'color': 'white', 'background-color': 'DarkSlateGray', 'margin-left': "0px", 'margin-top': "10px", 'margin-bottom': "30px" }} type="submit" className="w3-button w3-theme-d2 w3-margin-bottom"><i style={{ 'color': 'white' }} className="fa fa-comment"></i> Comment</button>
                </form>
            </div>
        </div>

        //todo: on comment submit, when displaying comments when retrived from the API, parse the comments for hashtags.

            //<p>{"---------------Post #" + data.results[postIter2]['id'] + "---------------------"}</p>
            //<p>{"Name: " + tempName}</p>
            //<p>{"User: " + data.results[postIter2]['user']}</p>
            //<p>{"Email: " + tempEmail}</p>
            //<p>{"Content: " + data.results[postIter2]['content']}</p>
            //<p>{"-------------------------------------------"}</p>
    }

    drawError = false;

    nextPage = () => {
        this.drawError = false;
        console.log("next page called!"); 
        const { data } = this.state;
        if (data['count'] <= (this.currentPage) * 10) {
            //this.drawError = true;
            //this.loadData();
            return;
        }
        //possibly check if the user is going too far (using count from API call)
        this.currentPage += 1;
        this.loadData();
    }

    previousPage = () => {
        this.drawError = false;
        console.log("prev page called!");
        if (this.currentPage === 1) {
            //do nothing cause at the end, maybe a visual cue saying u cant go back more
            //this.drawError = true;
            //this.loadData();
            return;
        }
        this.currentPage -= 1;
        this.loadData();
    }

    render() {
        const { data, loaded, placeholder } = this.state;

        let errorThing = <div />;
        if (this.drawError && this.tempUserCache.length>0) {
        const { data, loaded, placeholder } = this.state;
            errorThing = <Notification text={"Error, invalid page!"} type={"danger"} />;
            this.drawError = false;
        }

        if (loaded) {
            if (this.state.callerType === "HomeFeed") {
                let ta = [];

                this.postIter = -1;
                for (let i = 0; i < 10; i++) {
                    ta.push(this.renderPost());
                }

                this.postIter = -1;
                this.tempUserCache = []; 
                return <div>
                    {ta}
                    <p>
                        {<button className="button is-success" style={navPadding} onClick={this.previousPage}> Previous Page </button>}
                        {<button className="button is-success" style={navPadding} onClick={this.nextPage}> Next Page </button>}
                    </p>
                    {errorThing}
                    
                </div>
           
            } else {
                return this.props.render(data.results); //breaks if not in Table form
            }
        } else {
            return <p>{placeholder}</p>;
        }
    }
}

const navPadding = {
    paddingRight: '5px',
    paddingLeft: '5px',
    margin: '5px',
    textAlign: 'center',
    backgroundColor: 'DarkGreen',
    fontVariant: 'small-caps'
};

export default DataProvider;