import React from 'react';
import cx from 'classnames';
import s from '!!style-loader!css-loader!./layout.css';
import { Grid, Row, Col, ListGroup, ListGroupItem } from 'react-bootstrap';

class Layout extends React.Component {
    constructor(props) {
        super(props);
    }

    componentWillMount() {
        console.log(this.props.children)
    }

    render() {
        return (
            <div className={"content"}>
                <Grid>
                    <Row>
                        <Col md={2}>
                            <ListGroup>
                                <ListGroupItem>Home</ListGroupItem>
                                <ListGroupItem>Admin</ListGroupItem>
                            </ListGroup>
                        </Col>
                        <Col md={10} className={"main"}>{this.props.children}</Col>
                    </Row>
                </Grid>
            </div>
        )
    }
}

export default Layout;