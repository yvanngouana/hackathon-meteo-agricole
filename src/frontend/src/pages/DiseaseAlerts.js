import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Button, Form } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { FaBug, FaExclamationTriangle, FaInfoCircle, FaSearch } from 'react-icons/fa';

const DiseaseAlerts = () => {
  const [diseaseAlerts, setDiseaseAlerts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [coordinates, setCoordinates] = useState({ lat: 14.7167, lon: -17.4677 });
  const [days, setDays] = useState(7);
  
  useEffect(() => {
    fetchDiseaseAlerts();
  }, [coordinates, days]);

  const fetchDiseaseAlerts = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(
        `http://localhost:8000/api/predictions/disease-risk?latitude=${coordinates.lat}&longitude=${coordinates.lon}&days=${days}`
      );
      
      setDiseaseAlerts(response.data);
      setLoading(false);
    } catch (err) {
      setError('Erreur lors de la récupération des alertes de maladies');
      setLoading(false);
      console.error(err);
    }
  };

  // Prepare disease risk chart data
  const getDiseaseRiskChart = () => {
    if (!diseaseAlerts || !diseaseAlerts.alerts) return null;
    
    // Prepare data for each risk level
    const dates = diseaseAlerts.alerts.map(a => new Date(a.date).toLocaleDateString());
    const highRisk = diseaseAlerts.alerts.map(a => a.risk_level === 'high' ? 1 : 0);
    const mediumRisk = diseaseAlerts.alerts.map(a => a.risk_level === 'medium' ? 1 : 0);
    const lowRisk = diseaseAlerts.alerts.map(a => a.risk_level === 'low' ? 1 : 0);
    const humidity = diseaseAlerts.alerts.map(a => a.humidity || 0);
    const temperature = diseaseAlerts.alerts.map(a => a.temperature || 0);
    
    return {
      data: [
        {
          x: dates,
          y: highRisk,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Risque élevé',
          line: { color: '#e74c3c', width: 3 },
          marker: { size: 10 }
        },
        {
          x: dates,
          y: mediumRisk,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Risque modéré',
          line: { color: '#f39c12', width: 3 },
          marker: { size: 10 }
        },
        {
          x: dates,
          y: lowRisk,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Risque faible',
          line: { color: '#27ae60', width: 3 },
          marker: { size: 10 }
        }
      ],
      layout: {
        title: `Risques de maladies agricoles (${days} jours)`,
        xaxis: { title: 'Date' },
        yaxis: { 
          title: 'Niveau de risque', 
          tickvals: [0, 1], 
          ticktext: ['Faible', 'Élevé'] 
        },
        hovermode: 'closest'
      }
    };
  };

  // Prepare environmental factors chart
  const getEnvFactorsChart = () => {
    if (!diseaseAlerts || !diseaseAlerts.alerts) return null;
    
    const dates = diseaseAlerts.alerts.map(a => new Date(a.date).toLocaleDateString());
    const humidity = diseaseAlerts.alerts.map(a => a.humidity || 0);
    const temperature = diseaseAlerts.alerts.map(a => a.temperature || 0);
    
    return {
      data: [
        {
          x: dates,
          y: humidity,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Humidité (%)',
          yaxis: 'y',
          line: { color: '#3498db' }
        },
        {
          x: dates,
          y: temperature,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Température (°C)',
          yaxis: 'y2',
          line: { color: '#e67e22' }
        }
      ],
      layout: {
        title: 'Facteurs environnementaux favorisant les maladies',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Humidité (%)' },
        yaxis2: {
          title: 'Température (°C)',
          overlaying: 'y',
          side: 'right'
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
    fetchDiseaseAlerts();
  };

  if (loading && !diseaseAlerts) {
    return (
      <div className="spinner">
        <Spinner animation="border" variant="success" />
      </div>
    );
  }

  return (
    <Container>
      <h2 className="mb-4">Risques de Maladies Agricoles</h2>
      
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
      
      {diseaseAlerts && (
        <>
          <Row>
            <Col lg={8}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaBug className="me-2" /> Niveaux de risque de maladies</Card.Title>
                  {getDiseaseRiskChart() && (
                    <Plot
                      data={getDiseaseRiskChart().data}
                      layout={getDiseaseRiskChart().layout}
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
                  <Card.Title><FaInfoCircle className="me-2" /> Résumé des risques</Card.Title>
                  <p><strong>Localisation:</strong> {coordinates.lat}, {coordinates.lon}</p>
                  <p><strong>Période:</strong> {days} jours</p>
                  {diseaseAlerts.alerts && (
                    <>
                      <p><strong>Alertes hautes:</strong> {diseaseAlerts.alerts.filter(a => a.risk_level === 'high').length}</p>
                      <p><strong>Alertes modérées:</strong> {diseaseAlerts.alerts.filter(a => a.risk_level === 'medium').length}</p>
                      <p><strong>Alertes actuelles:</strong> {diseaseAlerts.alert_count}</p>
                    </>
                  )}
                  <Alert variant="warning" className="mt-3">
                    <strong>Attention:</strong> Les conditions d'humidité élevée et de température modérée favorisent les maladies fongiques.
                  </Alert>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row className="mt-4">
            <Col lg={6}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaExclamationTriangle className="me-2" /> Facteurs environnementaux</Card.Title>
                  {getEnvFactorsChart() && (
                    <Plot
                      data={getEnvFactorsChart().data}
                      layout={getEnvFactorsChart().layout}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%', height: '400px' }}
                    />
                  )}
                </Card.Body>
              </Card>
            </Col>
            <Col lg={6}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaInfoCircle className="me-2" /> Recommandations</Card.Title>
                  <ul className="list-unstyled">
                    <li className="mb-2">
                      <strong>Risque élevé:</strong> Surveillance renforcée des cultures, application préventive de fongicides
                    </li>
                    <li className="mb-2">
                      <strong>Risque modéré:</strong> Inspecter les cultures régulièrement, ventilation des plantations
                    </li>
                    <li className="mb-2">
                      <strong>Risque faible:</strong> Surveillance normale, maintenir les bonnes pratiques
                    </li>
                    <li className="mt-3">
                      <strong>Conditions favorables:</strong> Humidité >75% + Température 15-30°C
                    </li>
                  </ul>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row className="mt-4">
            <Col>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaBug className="me-2" /> Détail des alertes</Card.Title>
                  <div className="table-responsive">
                    <table className="table table-striped">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Niveau de risque</th>
                          <th>Humidité (%)</th>
                          <th>Température (°C)</th>
                          <th>Recommandation</th>
                        </tr>
                      </thead>
                      <tbody>
                        {diseaseAlerts.alerts && diseaseAlerts.alerts.map((alert, index) => (
                          <tr key={index} className={
                            alert.risk_level === 'high' ? 'table-danger' : 
                            alert.risk_level === 'medium' ? 'table-warning' : 'table-success'
                          }>
                            <td>{new Date(alert.date).toLocaleDateString()}</td>
                            <td>
                              <span className={
                                `badge ${
                                  alert.risk_level === 'high' ? 'bg-danger' : 
                                  alert.risk_level === 'medium' ? 'bg-warning text-dark' : 'bg-success'
                                }`
                              }>
                                {alert.risk_level === 'high' ? 'Élevé' : 
                                 alert.risk_level === 'medium' ? 'Modéré' : 'Faible'}
                              </span>
                            </td>
                            <td>{alert.humidity?.toFixed(1) || 'N/A'}</td>
                            <td>{alert.temperature?.toFixed(1) || 'N/A'}</td>
                            <td>{alert.recommendation}</td>
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

export default DiseaseAlerts;