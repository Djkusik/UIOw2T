import React from 'react'
import styled from 'styled-components'
import background from '../../resources/backgroundalt.jpg'
import Navbar from '../../components/navbar/Navbar'
import LandingPanel from '../../components/landingPanel/LandingPanel'

const Background = styled.div`
  height: 100vh;
  width: 100vw;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: url(${background});
  overflow: hidden;
  transform-origin: bottom;
`

export default class App extends React.Component {
  ref = React.createRef()

  componentDidMount() {
    const image = this.ref.current
    // eslint-disable-next-line no-undef
    var engine = new RainyDay({
      image,
      blur: 10,
      onInitialized: () => {
        engine.rain([[1, 2, 4000]])
        engine.rain(
          [
            [3, 3, 0.88],
            [5, 5, 0.9],
            [6, 2, 1]
          ],
          100
        )
      }
    })
  }

  render() {
    return (
      <div style={{ display: 'flex' }}>
        <Navbar />
        <Background ref={this.ref} />
        <LandingPanel />
      </div>
    )
  }
}
