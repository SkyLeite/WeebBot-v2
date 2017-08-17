import React from 'react';
import { FormattedMessage } from 'react-intl';
import messages from './messages';
import Layout from '../../components/Layout';
import { Button } from 'react-bootstrap';

export default class HomePage extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (
      <Layout>
        <h1>
          <FormattedMessage {...messages.header} />
        </h1>
        <Button> Hi </Button>
      </Layout>
    );
  }
}
