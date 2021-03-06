import React from 'react'
import styled from 'styled-components'
import Loader from 'react-loader-spinner'
import { Col } from 'reactstrap'

const BackgroundShade = styled.div`
  height: 100vh;
  width: 100vw;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  align-items: center;
`

export default class AwaitModal extends React.Component {

    render() {
        return this.props.playersWaiting !== 1 && (
            <BackgroundShade>
                <Col xs="6" sm="4" />
                <Col xs="6" sm="4">
                    <div style={{ textAlign: 'center' }}>
                        <Loader
                            type="Oval"
                            color="#FFFFFF"
                            height={50}
                            width={50}
                            style={{ alignSelf: 'center' }}
                        />
                    </div>


                    <div style={{
                        textAlign: 'center'
                    }}>{this.props.playersWaiting === 1 ? String(this.props.playersWaiting) + ' player waiting' : String(this.props.playersWaiting) + ' players waiting'}</div>
                </Col>
                <Col sm="4" />
            </BackgroundShade>

        )
    }
}