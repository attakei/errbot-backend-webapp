import React from 'react'
import { Card, Content, Image, Media } from 'react-bulma-components'
import marked from 'marked'


const render = (props) => {
  const { log } = props
  return (
    <Card>
      <Card.Content>
        <Media>
          <Media.Item renderAs="figure" position="left">
            <Image size={32} src="http://errbot.io/en/latest/_static/errbot.png" />
          </Media.Item>
          <Media.Item>
            <Content dangerouslySetInnerHTML={{__html: marked(log.body)}} />
          </Media.Item>
        </Media>
      </Card.Content>
    </Card>
  )
}

export default render
