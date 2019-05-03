import React, {Component} from "react";
import PropTypes from "prop-types";
import './pages/frontend_style.css'
import Notification from "./Notification";

class DataProvider extends Component {

    // temp variables to handle posts
    postIter = -1;
    tempUserCache = [];

    tempAllComments = [];

    comment = [];
    commentPostId = [];
    //commentPageIter = 1;
    //tempIter = 0;
    tempCommentSomething = 0;

    curUserId = 0;

    currentPage = 1;

    madeNewComment = false;

    constructor(props) {
        super(props);
        this.curUserId = this.props.userID;
        this.handleSubmit = this.handleSubmit.bind(this);
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
        //tempAllComments: []
    };

    ass = () => {
        return "hi";
    }

    loadCommentPage = (pageNum) => {
        fetch("/api/comment/?page=" + pageNum, {
            headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
        })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({ placeholder: "Something went wrong" });
                }

                return response.json();
            }).then(data => {
                this.tempAllComments = []; //wipe for now
                this.tempAllComments.push(data);
                this.setState({}); //empty refesh

            });
    }

    getComments = () => {
        this.loadCommentPage(1);
        //this.tempAllComments.push(this.loadCommentPage(1));
    }

    //fun = (tempCommentNum) => {
    //    this.setState({ tempAllComments: [] }); //reset

    //    if (this.state.tempIter < tempCommentNum) {
    //        console.log("currently tempiter is " + this.state.tempIter + " and num to reach is " + tempCommentNum);
    //        console.log("also currently page thing is " + this.state.commentPageIter);
    //        fetch("/api/comment/?page=" + this.state.commentPageIter, {
    //            headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
    //        }).then(response => {
    //            if (response.status !== 200) {
    //                return this.setState({ placeholder: "Something went wrong" });
    //            }

    //            return response.json();
    //        }).then(innerData => {

    //            for (let i = 0; i < innerData.results.length; i++) { //for every comment on that page
    //                console.log("found a comment, adding!");
    //                this.setState({ tempIter: this.state.tempIter + 1 });
    //                this.setState({ tempAllComments: this.state.tempAllComments + innerData.results[i] });
    //                //tempAllComments.push(innerData.results[i]);
    //            }
    //            this.setState({ commentPageIter: this.state.commentPageIter + 1 });
    //            //this.state.commentPageIter += 1; //increment page and continue until count is filled.
    //            //console.log("new tempiter is: " + this.state.tempIter);
    //            if (this.state.tempIter < tempCommentNum) {
    //                console.log("next page!");
    //                this.fun(tempCommentNum);
    //            }
    //        });
    //    }
    //    //console.log("loop done! comments array is length " + this.state.tempAllComments.length);
    //    this.getUsers(); //fucking whatever, just to reload without breaking.
    //}

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
                .then(data => {
                    //if (this.tempUserCache.length <= 0) { this.getUsers(); }
                    this.getUsers(); //do it every time to prevent bugs, slower but who cares

                    if (this.tempAllComments.length <= 0 || this.madeNewComment) {
                        this.getComments();
                        this.madeNewComment = false;
                    }

                    this.setState({ blocked_members: this.props.blockedMembers, data: data, loaded: true, callerType: this.props.callerType })
                });

            //this.tempIter = 0;
            //console.log(this.state.tempIter);
            //this.setState({ tempIter: 0 });
            //this.setState({ commentPageIter: 1 });
            

            //fetch("/api/comment/?page=" + "1", {
            //    headers: new Headers({ 'Authorization': 'Token ' + this.props.token }),
            //}).then(response => {
            //    if (response.status !== 200) {
            //        console.log("big oopsie: " + response.status);
            //        return this.setState({ placeholder: "Something went wrong" });
            //    }

            //    return response.json();
            //    })
            //    .then(data => {
            //        console.log(data);
            //        console.log("trying to get to " + "/api/comment/?page=" + this.state.commentPageIter);
            //        //console.log(data['count']);
            //        //if (!data['count']) {
            //        //    console.log("Ahh!");
            //        //}

            //        let tempCommentNum = data['count'];
            //        //if (tempCommentNum === this.state.tempAllComments.length) {
            //        //    return;
            //        //}

            //        //this.tempIter = 0;
                    
            //        //this.tempAllComments = []; //wipe to reset, not sure if it works

            //        if (this.state.tempIter < tempCommentNum) { //go through every single comment


            //            let but = this.fun(tempCommentNum);
            //            //    .then(welp => {
            //            //    this.setState({ tempIter: 0 });
            //            //    this.setState({ commentPageIter: 1 });
            //            //    let but2 = this.fun(tempCommentNum);
            //            //});
            //            //console.log("got " + but + " from fun(), checking state: " + this.state.tempIter);
                       
            //            //console.log("returning " + this.state.tempIter);
            //            //return this.state.tempIter;
            //        }

            //    });
            
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

    handleSubmit(event, testVal) {
        console.log(testVal);

        event.preventDefault();
        //console.log("userid: " + this.props.userID);
        //console.log("comment: " + this.comment);
        //console.log("comment lenght: " + this.comment.length);
        //console.log("comment at testval: " + this.comment.find(testVal));
        //console.log("commen valuet at testval: " + this.comment[testval].value);
        //console.log("content unvalue: " + this.comment);
        //console.log("post: " + this.commentPostId);

        let epic = JSON.stringify({
            "user": this.curUserId,
            "content": this.comment[testVal + 10].value, //WATCH THIS EPIC FIX
            "post": this.commentPostId[testVal + 10],
            "by_admin": false
        });
        console.log("EPIC SUBMIT3");

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", (event) => {
            if (event.target.readyState === 4) {
                console.log(this.responseText);

                this.setState({
                    notificationText: "Posted Comment: " + this.comment.value
                });

                this.comment = [];
                this.commentPostId = [];

                //this.loadData();
            }
        });
        //console.log(this.props.userID);

        xhr.open("POST", "/api/comment/");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("cache-control", "no-cache");
        xhr.setRequestHeader("Authorization", "Token " + this.props.token);

        this.madeNewComment = true;
        document.getElementsByName("comment:" + testVal)[0].reset();

        xhr.send(epic);
        this.loadData();

    }


    renderPost = () => {
        const { data, blocked_members } = this.state;

        let postIter2 = this.postIter + 1;
        this.postIter += 1;

        if (postIter2 < 0 || postIter2 >= data.results.length) {
            return <p></p>
        }

        //console.log(blocked_members);
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
        let tempComments = (<div />);
        if (this.tempAllComments.length != 0) {
            //console.log(this.tempAllComments.length);
            //console.log(this.tempAllComments);
            //console.log(this.tempAllComments[0]);
            //console.log(this.tempAllComments[0].results);
            //console.log(this.tempAllComments[0].results[0]['content']);
            tempComments = [];
            for (let i = 0; i < this.tempAllComments[0].results.length; i++) { //page 0 is 0 here, more pages later?
                if (data.results[postIter2]['id'] === this.tempAllComments[0].results[i]['post']) {
                    let tempCommentName = "_loading_"
                    if (emailCheck >= 0) {
                        //console.log("tempusercache is " + this.tempUserCache.length);
                        //console.log("the index i want is " + (this.tempUserCache.length - this.tempAllComments[0].results[i]['user']));
                        //console.log("the value inside index 6 is " + this.tempUserCache[6]);
                        //console.log("the value inside our thing is " + this.tempUserCache[ (this.tempUserCache.length - this.tempAllComments[0].results[i]['user']) ]);
                        //console.log("the email inside our thing is " + this.tempUserCache[(this.tempUserCache.length - this.tempAllComments[0].results[i]['user'])]['email']);
                        //let finalWhatever
                        tempCommentName = this.tempUserCache[(this.tempUserCache.length - this.tempAllComments[0].results[i]['user'])]['first_name'] + " " + this.tempUserCache[(this.tempUserCache.length - this.tempAllComments[0].results[i]['user'])]['last_name'];
                        //console.log(finalWhatever);
                        //tempCommentName = this.tempUserCache[this.tempUserCache.length - this.tempAllComments[0].results[i]['user']];
                    }

                    tempComments.push(
                        <div style={{ 'display': 'flex', 'align-items': 'flex-start' }}>
                            <p style={{ 'border-radius': '25px', 'background-color': 'DarkTurquoise', 'color': 'black', 'padding-left': '15px', 'padding-top': '5px', 'padding-bottom': '5px', 'padding-right': '15px', 'margin-top': '10px' }}  > {tempCommentName}</p >
                        </div>
                    );
                    tempComments.push(
                        <p style={{ 'word-wrap': 'break-word', 'margin-left': '25px', 'margin-top': '5px', 'padding-left': '5px' }} >{this.tempAllComments[0].results[i]['content']}</p>
                    );
                }
            }
            //tempComments = this.tempAllComments.results[0]['content'];
        }

        let tempVal = this.tempCommentSomething;
        this.tempCommentSomething += 1;

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
                <hr></hr>
                <p style={navPadding2}>Comments:</p>
                {tempComments}
                <form name={"comment:" + tempVal} onSubmit={(event) => this.handleSubmit(event, tempVal)}>
                    <textarea ref={(input) => { this.comment.push(input); this.commentPostId.push(data.results[postIter2]['id']) }} type="text" style={{ 'margin-top': '5px', 'resize': "none", 'width': "100%" }} className="w3-border w3-padding" placeholder="Leave a comment!"></textarea>
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
                this.tempCommentSomething = 0;
                this.comment = [];
                this.commentPostId = [];
                for (let i = 0; i < 10; i++) {
                    ta.push(this.renderPost());
                }

                this.postIter = -1;
                //this.tempCommentSomething = 0;
                //this.comment = [];
                //this.commentPostId = [];

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
const navPadding2 = {
    paddingRight: '5px',
    paddingLeft: '5px',
    margin: '5px',
    //textAlign: 'center',
    backgroundColor: 'DodgerBlue',
    color: 'white',
    fontVariant: 'small-caps'
};

export default DataProvider;