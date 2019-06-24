import React from 'react'
import { Card, Content, Image, Media } from 'react-bulma-components'


const render = (props) => {
  const { log } = props
  return (
    <Card>
      <Card.Content>
        <Media>
          <Media.Item>
            <Content align="right">
              <p>{log.body}</p>
            </Content>
          </Media.Item>
          <Media.Item renderAs="figure" position="right">
            <Image size={32} src="http://errbot.io/en/latest/_static/errbot.png" />
          </Media.Item>
        </Media>
      </Card.Content>
    </Card>
  )
}

export default render
