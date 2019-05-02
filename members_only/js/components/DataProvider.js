import React, {Component} from "react";
import PropTypes from "prop-types";

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
            <p>{"---------------Post #" + data.results[postIter2]['id'] + "---------------------"}</p>
            <p>{"Name: " + tempName}</p>
            <p>{"User: " + data.results[postIter2]['user']}</p>
            <p>{"Email: " + tempEmail}</p>
            <p>{"Content: " + data.results[postIter2]['content']}</p>
            <p>{"-------------------------------------------"}</p>
        </div>
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