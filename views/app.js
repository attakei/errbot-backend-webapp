import React from 'react'
import ReactDOM from 'react-dom'
import 'react-bulma-components/dist/react-bulma-components.min.css'

import AppContainer from './components/AppContainer'

const socketUrl = SOCKET_URL || 'ws://localhost:8080/connect'

ReactDOM.render(
  <AppContainer socketUrl={socketUrl} />,
  document.getElementById('main')
);  
