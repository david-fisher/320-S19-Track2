import React, {Component} from 'react';
import DataProvider from "../DataProvider";
import Table from "../Table";

class Feed extends Component {
    render() {
        return (
            <div>
                <DataProvider endpoint="/api/post/" token={this.props.token} render={data => <Table data={data}/>}/>
            </div>
        );
    }
}

export default Feed;
