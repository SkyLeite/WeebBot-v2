import React from 'react';
import cx from 'classnames';
import s from '!!style-loader!css-loader!./layout.css';
import { Grid, Row, Col, ListGroup, ListGroupItem, Image, Button } from 'react-bootstrap';

class User extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Grid>
                <Row>
                    <Col md={1}>
                        <Image thumbnail src={`https://cdn.discordapp.com/avatars/${this.props.user.id}/${this.props.user.avatar}.gif`} />
                    </Col>
                    <Col md={0}>
                        {`${this.props.user.username}#${this.props.user.discriminator}`}
                    </Col>
                </Row>
            </Grid>
        )
    }
}

class Layout extends React.Component {
    constructor(props) {
        super(props);
    }

    async componentWillMount() {
        fetch('/api/me', { method: 'GET', credentials: 'same-origin' })
            .then(r => r.json())
            .then(data => {
                if (!data.STATUS_CODE) {
                    this.setState({ user: data.user });
                }
            })
    }

    render() {
        return (
            <div className={"content"}>
                <Grid>
                    <Row>
                        <Col md={2}>
                            <div style={{ marginTop: '20px' }}>
                                {this.state ? <User user={this.state.user} /> : <Button href="/auth/discord/">Login with Discord</Button>}
                            </div>
                            <ListGroup style={{ marginTop: '20px' }}>
                                <ListGroupItem href="/">Home</ListGroupItem>
                                {this.state ?
                                    <div>
                                        <ListGroupItem href="/admin">Admin</ListGroupItem>
                                        <ListGroupItem href="/api/logout">Logout</ListGroupItem>
                                    </div> : null}
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