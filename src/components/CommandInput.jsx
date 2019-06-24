import React from 'react'
import { Button, Form } from 'react-bulma-components'


const render = (props) => {
  return (
    <form onSubmit={props.submit}>
      <Form.Field horizontal>
        <Form.Label>Command?: </Form.Label>
        <Form.Input value={props.currentInput} onChange={props.changeInput} />
        <Button onClick={props.submit}>Submit</Button>
      </Form.Field>
    </form>
  )
}

export default render
