import React from 'react'


const render = (props) => {
  const { log } = props
  return (
    <div>
      <p><strong>{log.body}</strong></p>
    </div>
  )
}

export default render
