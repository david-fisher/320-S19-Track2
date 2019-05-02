import React, {Component} from "react";
import PropTypes from "prop-types";
import './pages/frontend_style.css'

class DataProvider extends Component {

    // temp variables to handle posts
    postIter = -1;
    tempUserCache = [];
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
        callerType: "hoi",
        loaded: false,
        placeholder: "Loading...",
        time: Date.now()
    };

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
                .then(data => { if (this.tempUserCache.length <= 0) { this.getUsers(); } this.setState({ data: data, loaded: true, callerType: this.props.callerType }) });
        }else{
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

        const { data } = this.state;

        let postIter2 = this.postIter + 1;
        this.postIter += 1;

        if (postIter2 < 0 || postIter2 >= data.results.length) {
            return <p></p>
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

        return <div>
            <div className="w3-container w3-card w3-white w3-round w3-margin">
                <span style={{ 'margin-top': '10px' }} className="w3-right w3-opacity">1 min ago</span>
                <div style={{ 'display': 'flex', 'align-items': 'flex-start' }}>
                    <h4 style={{ 'border-radius': '25px', 'background-color': 'steelblue', 'color': 'white', 'padding-left': '15px', 'padding-top': '5px', 'padding-bottom': '5px', 'padding-right': '15px', 'margin-top': '10px' }} >{tempName}</h4>
                </div>
                <p style={{ 'margin-left': '25px', 'margin-top': '5px', 'padding-left': '5px' }}>{data.results[postIter2]['content']}</p>
                <hr class="w3-clear"></hr>

                <form>
                    <textarea type="text" style={{ 'resize': "none", 'width': "75%" }} className="w3-border w3-padding" placeholder="Leave a comment!"></textarea>
                    <br></br>
                    <button style={{ 'color': 'white', 'background-color': 'DarkSlateGray', 'margin-left': "0px", 'margin-top': "10px", 'margin-bottom': "30px" }} type="submit" className="w3-button w3-theme-d2 w3-margin-bottom"><i style={{ 'color': 'white' }} className="fa fa-comment"></i> Comment</button>
                </form>
            </div>
        </div>

            //<p>{"---------------Post #" + data.results[postIter2]['id'] + "---------------------"}</p>
            //<p>{"Name: " + tempName}</p>
            //<p>{"User: " + data.results[postIter2]['user']}</p>
            //<p>{"Email: " + tempEmail}</p>
            //<p>{"Content: " + data.results[postIter2]['content']}</p>
            //<p>{"-------------------------------------------"}</p>
    }

    nextPage = () => {
        console.log("next page called!"); 
        const { data } = this.state;
        if (data['count'] <= (this.currentPage)*10 ) {
            return;
        }
        //possibly check if the user is going too far (using count from API call)
        this.currentPage += 1;
        this.loadData();
    }

    previousPage = () => {
        console.log("prev page called!");
        if (this.currentPage === 1) {
            //do nothing cause at the end, maybe a visual cue saying u cant go back more
            return;
        }
        this.currentPage -= 1;
        this.loadData();
    }

    render() {
        const { data, loaded, placeholder } = this.state;

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
                        {<button onClick={this.previousPage}> Previous Page </button>}
                        {<button onClick={this.nextPage}> Next Page </button>}
                    </p>
                    
                </div>
           
            } else {
                return this.props.render(data.results); //breaks if not in Table form
            }
        } else {
            return <p>{placeholder}</p>;
        }
    }
}

export default DataProvider;