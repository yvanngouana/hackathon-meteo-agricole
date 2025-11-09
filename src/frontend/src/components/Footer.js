import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="bg-dark text-white py-4 mt-5">
      <Container>
        <Row>
          <Col md={6}>
            <h5>Météo Agricole</h5>
            <p>Plateforme intelligente d'aide à la décision agricole</p>
          </Col>
          <Col md={3}>
            <h5>Ressources</h5>
            <ul className="list-unstyled">
              <li><a href="#!" className="text-white">Documentation</a></li>
              <li><a href="#!" className="text-white">API</a></li>
              <li><a href="#!" className="text-white">Support</a></li>
            </ul>
          </Col>
          <Col md={3}>
            <h5>Contact</h5>
            <ul className="list-unstyled">
              <li>Email: contact@meteo-agricole.sn</li>
              <li>Tél: +221 123 456 789</li>
            </ul>
          </Col>
        </Row>
        <hr className="my-3" />
        <Row>
          <Col className="text-center">
            <small>&copy; 2024 Météo Agricole - Tous droits réservés</small>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;