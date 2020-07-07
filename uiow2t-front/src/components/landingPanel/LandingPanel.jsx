import React from 'react'
import { Button, Form, Input, } from 'reactstrap'
import './LandingPanel.css'; // Tell webpack that Button.js uses these styles

function LandingPanel() {
  // const [isHovered, setHovered] = useState(false)

  return (
    <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
      <Form className="usernameForm" style={{ top: '75%' }}>

        <Input id="nickInput" placeholder="Nickname" />
      </Form>
      <Button className="joinButton" color="red">
        <div style={{ color: 'rgba(255,255,255,0.75)' }}>Join the game</div></Button>
    </div>

  )
}
export default LandingPanel
