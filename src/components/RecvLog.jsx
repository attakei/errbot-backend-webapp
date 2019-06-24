import React from 'react'
import marked from 'marked'


const render = (props) => {
  const { log } = props
  return (
    <div>
      <ul>
        <li>{log.timestamp}</li>
      </ul>
      <div 
        dangerouslySetInnerHTML={{__html: marked(log.body)}}
      />
    </div>
  )
}

export default render
