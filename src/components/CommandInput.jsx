import React from 'react'


const render = (props) => {
  return (
    <div>
      <form onSubmit={props.submit}>
        <input type="text" value={props.currentInput} onChange={props.changeInput} />
        <button onKeyPress={props.submit}>Submit</button>
      </form>
    </div>
  )
}

export default render
