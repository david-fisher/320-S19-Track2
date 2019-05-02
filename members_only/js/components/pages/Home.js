import React, {Component} from 'react';

class Home extends Component {
    render() {
        return (
            <div>
                <h1 style={header}> Welcome to Members Only </h1>
                <div className="container" style={all}>
                    <div className="c1" style = {c1}> Members Only is the newest and most exclusive social media platform that everyone is using.
                    </div>
                    <div className="c11" style={c11}> All
                    of your favorite influencers and idols are here posting never-before-seen content that you need to see.</div>
                    <div className="c2" style={c2}>
                        Registration is by <b>invite only</b>.
                    </div>
                </div>
            </div>
        );
    }
}


const header = {
    fontSize: '75px',
    fontVariant: 'small-caps',
    textAlign: 'center',
    marginTop: '5%'
};

const all = {
    fontVariant: 'small-caps'
};

const c1 = {
    fontSize: '30px',
    marginTop: '10%',
    textAlign: 'center'
};

const c11 = {
    fontSize: '25px',
    textAlign:'center',
    marginTop: '5%'
};

const c2 = {
    fontSize: '40px',
    marginTop: '10%',
    textAlign: 'center'
};

export default Home;
