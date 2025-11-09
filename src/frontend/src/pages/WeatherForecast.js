import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Button, Form } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { FaCloudSun, FaTint, FaWind, FaThermometerHalf, FaSearch } from 'react-icons/fa';

const WeatherForecast = () => {
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [coordinates, setCoordinates] = useState({ lat: 14.7167, lon: -17.4677 });
  const [days, setDays] = useState(7);
  
  useEffect(() => {
    fetchForecast();
  }, [coordinates, days]);

  const fetchForecast = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(
        `http://localhost:8000/api/weather/forecast?latitude=${coordinates.lat}&longitude=${coordinates.lon}&days=${days}`
      );
      
      setForecastData(response.data);
      setLoading(false);
    } catch (err) {
      setError('Erreur lors de la récupération des prévisions');
      setLoading(false);
      console.error(err);
    }
  };

  // Prepare temperature chart data
  const getTempChart = () => {
    if (!forecastData || !forecastData.forecasts) return null;
    
    const dates = forecastData.forecasts.map(f => new Date(f.date).toLocaleDateString());
    const tempsMin = forecastData.forecasts.map(f => f.temp_min);
    const tempsMax = forecastData.forecasts.map(f => f.temp_max);
    const tempsDay = forecastData.forecasts.map(f => f.temp_day);
    
    return {
      data: [
        {
          x: dates,
          y: tempsMax,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Temp. Max',
          line: { color: '#FF6B6B' }
        },
        {
          x: dates,
          y: tempsDay,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Temp. Jour',
          line: { color: '#4ECDC4' }
        },
        {
          x: dates,
          y: tempsMin,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Temp. Min',
          line: { color: '#45B7D1' }
        }
      ],
      layout: {
        title: `Prévisions de température (${days} jours)`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Température (°C)' },
        hovermode: 'closest'
      }
    };
  };

  // Prepare rain chart data
  const getRainChart = () => {
    if (!forecastData || !forecastData.forecasts) return null;
    
    const dates = forecastData.forecasts.map(f => new Date(f.date).toLocaleDateString());
    const rain = forecastData.forecasts.map(f => f.rain_mm);
    const pop = forecastData.forecasts.map(f => f.pop); // Probability of precipitation
    
    return {
      data: [
        {
          x: dates,
          y: rain,
          type: 'bar',
          name: 'Précipitations (mm)',
          marker: { color: '#3498db' }
        },
        {
          x: dates,
          y: pop,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Probabilité (%)',
          yaxis: 'y2',
          line: { color: '#e74c3c' }
        }
      ],
      layout: {
        title: `Prévisions de précipitations (${days} jours)`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Pluie (mm)' },
        yaxis2: {
          title: 'Probabilité (%)',
          overlaying: 'y',
          side: 'right'
        },
        hovermode: 'closest'
      }
    };
  };

  // Prepare humidity chart data
  const getHumidityChart = () => {
    if (!forecastData || !forecastData.forecasts) return null;
    
    const dates = forecastData.forecasts.map(f => new Date(f.date).toLocaleDateString());
    const humidity = forecastData.forecasts.map(f => f.humidity);
    
    return {
      data: [
        {
          x: dates,
          y: humidity,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Humidité (%)',
          line: { color: '#9b59b6' },
          fill: 'tonexty'
        }
      ],
      layout: {
        title: `Prévisions d'humidité (${days} jours)`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Humidité (%)' },
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
    fetchForecast();
  };

  if (loading && !forecastData) {
    return (
      <div className="spinner">
        <Spinner animation="border" variant="success" />
      </div>
    );
  }

  return (
    <Container>
      <h2 className="mb-4">Prévisions Météo</h2>
      
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
      
      {forecastData && (
        <>
          <Row>
            <Col lg={8}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaThermometerHalf className="me-2" /> Température</Card.Title>
                  {getTempChart() && (
                    <Plot
                      data={getTempChart().data}
                      layout={getTempChart().layout}
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
                  <Card.Title><FaCloudSun className="me-2" /> Conditions actuelles</Card.Title>
                  <p><strong>Localisation:</strong> {coordinates.lat}, {coordinates.lon}</p>
                  <p><strong>Prévisions pour:</strong> {days} jours</p>
                  {forecastData.forecasts[0] && (
                    <>
                      <p><strong>Température aujourd'hui:</strong> {forecastData.forecasts[0].temp_day?.toFixed(1)}°C</p>
                      <p><strong>Précipitations aujourd'hui:</strong> {forecastData.forecasts[0].rain_mm?.toFixed(1)}mm</p>
                    </>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
          
          <Row className="mt-4">
            <Col lg={6}>
              <Card className="dashboard-card">
                <Card.Body>
                  <Card.Title><FaTint className="me-2" /> Précipitations</Card.Title>
                  {getRainChart() && (
                    <Plot
                      data={getRainChart().data}
                      layout={getRainChart().layout}
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
                  <Card.Title><FaWind className="me-2" /> Humidité</Card.Title>
                  {getHumidityChart() && (
                    <Plot
                      data={getHumidityChart().data}
                      layout={getHumidityChart().layout}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%', height: '400px' }}
                    />
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
};

export default WeatherForecast;