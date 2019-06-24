import React from 'react'

import SendLog from './SendLog'
import RecvLog from './RecvLog'


const render = (props) => {
  return (
    <div>
      {props.logs.map(log => {
        if (log.type === 'send') {
          return <SendLog key={log.timestamp} log={log} />
        } else if (log.type === 'recv') {
          return <RecvLog key={log.timestamp} log={log} />
        }
        console.error(`Invalid log type: ${log.type}`)
      })}
    </div>
  )
}

export default render
