import dayjs from 'dayjs'
import React from 'react'
import { Container, Heading, Section } from 'react-bulma-components'
import Scroll from 'react-scroll'

import CommandInput from './CommandInput'
import LogHistory from './LogHistory'


export default class AppContainer extends React.Component {
  constructor(props) {
    super(props)
    this.commandInputRef = React.createRef()
    this.state = {
      inputValue: '',
      logs: [],
      socket: null,
    }
  }

  render() {
    return (
      <Section>
        <Container>
          <Heading>Errbot webapp</Heading>
          <LogHistory logs={this.state.logs} />
        </Container>
        <Container>
          <div ref={this.commandInputRef}>
            <CommandInput
              currentInput={this.state.inputValue}
              changeInput={(e) => this.changeInput(e)}
              submit={(e) => this.sendCommand(e)} 
            />
          </div>
        </Container>
      </Section>
    )
  }

  async sendCommand(e) {
    e.preventDefault()
    const { inputValue } = this.state
    this.setState((prev) => {
      return {
        ...prev,
        inputValue: '',
        logs: prev.logs.concat([
          {type:'send', body: inputValue, timestamp: dayjs().valueOf()}
        ])
      }
    })
    if (this.state.socket && this.state.socket.readyState == WebSocket.OPEN) {
    } else {
      await this.connectSocket()
    }
    this.state.socket.send(inputValue)
  }

  changeInput(e) {
    this.setState({inputValue: e.target.value})
  }

  async connectSocket() {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(this.props.socketUrl)
      socket.addEventListener('message', (e) => {
        this.setState(prev => {
          return {
            ...prev,
            logs: prev.logs.concat([
              {type:'recv', body: e.data, timestamp: dayjs().valueOf()}
            ])
          }
        })
        const target = this.commandInputRef.current
        const scroll = Scroll.animateScroll
        scroll.scrollTo(target.parentElement.offsetTop)
      })
      socket.onopen = () => resolve(socket)
      socket.onerror = (err) => reject(err)
      this.setState({socket, })
    })
  }
}
