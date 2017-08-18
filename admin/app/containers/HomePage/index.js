import React from 'react';
import { FormattedMessage } from 'react-intl';
import messages from './messages';
import { Button } from 'react-bootstrap';

export default class HomePage extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {

    return (
      <div style={{marginTop: '20px', marginBottom: '20px'}}>
        C O N T E N T <br />
        <iframe width="560" height="315" src="https://www.youtube.com/embed/af2wLahd8WM" frameborder="0" allowfullscreen></iframe>
      </div>
    );
  }
}
