import React, { useState } from 'react'
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap'

function NavigationBar() {
  const [isOpen, setIsOpen] = useState(false)

  const toggle = () => setIsOpen(!isOpen)

  return (
    <div>
      <Navbar
        className="navbar navbar-expand-lg navbar-dark"
        style={{
          transition: 'all 1s ease',
          WebkitTransition: 'all 1s ease',
          MozTransition: 'all 1s ease',
          position: 'fixed',
          width: '100%',
          backgroundColor: 'rgba(0, 0, 0, 0.5)'
        }}
        light
        expand="md"
        sticky="top"
      >
        <NavbarBrand href="/">WIETactics</NavbarBrand>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={false} navbar>
          <Nav className="mr-auto" navbar>
            <NavItem>
              <NavLink href="/about">About</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="https://github.com/">GitHub</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/credits">Credits</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="https://github.com/">GitHub</NavLink>
            </NavItem>
          </Nav>
        </Collapse>
      </Navbar>
    </div>
  )
}
export default NavigationBar
