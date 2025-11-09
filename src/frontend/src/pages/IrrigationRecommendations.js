import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Button, Form } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { FaTint, FaCalendarAlt, FaInfoCircle, FaSearch } from 'react-icons/fa';

const IrrigationRecommendations = () => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [coordinates, setCoordinates] = useState({ lat: 14.7167, lon: -17.4677 });
  const [days, setDays] = useState(7);
  
  useEffect(() => {
    fetchRecommendations();
  }, [coordinates, days]);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(
        `http://localhost:8000/api/predictions/irrigation?latitude=${coordinates.lat}&longitude=${coordinates.lon}&days=${days}`
      );
      
      setRecommendations(response.data);
      setLoading(false);
    } catch (err) {
      setError('Erreur lors de la récupération des recommandations d\'irrigation');
      setLoading(false);
      console.error(err);
    }
  };

  // Prepare irrigation chart data
  const getIrrigationChart = () => {
    if (!recommendations || !recommendations.recommendations) return null;
    
    const dates = recommendations.recommendations.map(r => new Date(r.date).toLocaleDateString());
    const irrigationNeeded = recommendations.recommendations.map(r => r.irrigation_needed ? r.water_amount_mm : 0);
    const needsIrrigation = recommendations.recommendations.map(r => r.irrigation_needed ? 1 : 0);
    
    return {
      data: [
        {
          x: dates,
          y: irrigationNeeded,
          type: 'bar',
          name: 'Besoin en irrigation (mm)',
          marker: { color: '#27ae60' }
        },
        {
          x: dates,
          y: needsIrrigation,
          type: 'scatter',
          mode: 'markers',
          name: 'Irrigation nécessaire',
          marker: { 
            color: 'red',
            size: 10,
            symbol: 'diamond'
          },
          yaxis: 'y2'
        }
      ],
      layout: {
        title: `Recommandations d'irrigation (${days} jours)`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Quantité d\'eau (mm)' },
        yaxis2: {
          title: 'Irrigation ?',
          overlaying: 'y',
          side: 'right',
          tickvals: [0, 1],
          ticktext: ['Non', 'Oui']
        },
        hovermode: 'closest'
      }
    };
  };

  const handleCoordsChange = (e) => {
    const { name, value } = e.target;
    setCoordinates(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleDaysChange = (e) => {
    setDays(parseInt(e.target.value));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchRecommendations();
  };

  if (loading && !recommendations) {
    return (
      <div className="spinner">
        <Spinner animation="border" variant="success" />
      </div>
    );
  }

  return (
    <Container>
      <h2 className="mb-4">Recommandations d'Irrigation</h2>
      
      <Card className="dashboard-card mb-4">
        <Card.Body>
          <Form onSubmit={handleSearch}>
            <Row>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Latitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="lat"
                    value={coordinates.lat}
                    onChange={handleCoordsChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Longitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="lon"
                    value={coordinates.lon}
                    onChange={handleCoordsChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Jours de prévision</Form.Label>
                  <Form.Select value={days} onChange={handleDaysChange}>
                    <option value="3">3 jours</option>
                    <option value="7">7 jours</option>
                    <option value="14">14 jours</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3} className="d-flex align-items-end">
                <Button 
                  variant="success" 
                  type="submit"
                  className="w-100"
                >
                  <FaSearch className="me-2" /> Rechercher
                </Button>
              </Col>
            </Row>
          </Form>
        </Card.Body>
      </Card>
      
      {error && (
        <Alert variant="danger">{error}</Alert>
      )}
      
      {recommendations && (
        <>
          <Row>
            <Col lg={8}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaTint className="me-2" /> Recommandations d'Irrigation</Card.Title>
                  {getIrrigationChart() && (
                    <Plot
                      data={getIrrigationChart().data}
                      layout={getIrrigationChart().layout}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%', height: '400px' }}
                    />
                  )}
                </Card.Body>
              </Card>
            </Col>
            <Col lg={4}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaInfoCircle className="me-2" /> Résumé</Card.Title>
                  <p><strong>Localisation:</strong> {coordinates.lat}, {coordinates.lon}</p>
                  <p><strong>Période:</strong> {days} jours</p>
                  {recommendations.recommendations && (
                    <>
                      <p><strong>Jours d'irrigation:</strong> {recommendations.recommendations.filter(r => r.irrigation_needed).length}</p>
                      <p><strong>Besoin total en eau:</strong> {recommendations.recommendations.filter(r => r.irrigation_needed).reduce((sum, r) => sum + r.water_amount_mm, 0).toFixed(1)}mm</p>
                    </>
                  )}
                  <Alert variant="info" className="mt-3">
                    <strong>Comment lire le graphique:</strong><br />
                    Les barres vertes montrent la quantité d'eau recommandée.<br />
                    Les diamants rouges indiquent les jours où l'irrigation est nécessaire.
                  </Alert>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row className="mt-4">
            <Col>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaCalendarAlt className="me-2" /> Détail des recommandations</Card.Title>
                  <div className="table-responsive">
                    <table className="table table-striped table-hover">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Irrigation nécessaire</th>
                          <th>Quantité d'eau (mm)</th>
                          <th>Raison</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recommendations.recommendations && recommendations.recommendations.map((rec, index) => (
                          <tr key={index} className={rec.irrigation_needed ? 'table-warning' : ''}>
                            <td>{new Date(rec.date).toLocaleDateString()}</td>
                            <td>{rec.irrigation_needed ? 'Oui' : 'Non'}</td>
                            <td>{rec.water_amount_mm}mm</td>
                            <td>{rec.reason}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
};

export default IrrigationRecommendations;