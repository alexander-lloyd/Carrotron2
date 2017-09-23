import React from 'react'
import { Navbar, NavItem } from 'react-materialize';

const Nav = () => (
  <Navbar brand='Carrotron2' right>
    <NavItem href='/'>Home</NavItem>
    <NavItem href='/about'>About</NavItem>
  </Navbar>
);

export default Nav
