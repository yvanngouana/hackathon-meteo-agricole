import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { FaLeaf, FaCloudSun, FaTint, FaWind } from 'react-icons/fa';

const Header = () => {
  return (
    <Navbar bg="success" variant="dark" expand="lg" className="py-3">
      <Container>
        <Navbar.Brand href="/" className="d-flex align-items-center">
          <FaLeaf className="me-2" />
          <span className="fs-4 fw-bold">Météo Agricole</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link href="/">Tableau de bord</Nav.Link>
            <Nav.Link href="/fields">Champs</Nav.Link>
            <Nav.Link href="/weather">Météo</Nav.Link>
            <Nav.Link href="/irrigation">Irrigation</Nav.Link>
            <Nav.Link href="/diseases">Maladies</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;