import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { FaThermometerHalf, FaTint, FaWind, FaCloudSun, FaSeedling, FaExclamationTriangle } from 'react-icons/fa';

const Dashboard = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Using Dakar coordinates as default
  const lat = 14.7167;
  const lon = -17.4677;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch current weather
        const weatherResponse = await axios.get(`http://localhost:8000/api/weather/current?latitude=${lat}&longitude=${lon}`);
        setWeatherData(weatherResponse.data.weather);
        
        // Fetch forecast
        const forecastResponse = await axios.get(`http://localhost:8000/api/weather/forecast?latitude=${lat}&longitude=${lon}&days=7`);
        setForecastData(forecastResponse.data);
        
        setLoading(false);
      } catch (err) {
        setError('Erreur lors de la récupération des données météo');
        setLoading(false);
        console.error(err);
      }
    };

    fetchData();
  }, []);

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
          type: 'bar',
          name: 'Temp. Max',
          marker: { color: '#FF6B6B' }
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
          type: 'bar',
          name: 'Temp. Min',
          marker: { color: '#45B7D1' }
        }
      ],
      layout: {
        title: 'Prévisions de température (7 jours)',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Température (°C)' }
      }
    };
  };

  // Prepare rain chart data
  const getRainChart = () => {
    if (!forecastData || !forecastData.forecasts) return null;
    
    const dates = forecastData.forecasts.map(f => new Date(f.date).toLocaleDateString());
    const rain = forecastData.forecasts.map(f => f.rain_mm);
    
    return {
      data: [
        {
          x: dates,
          y: rain,
          type: 'bar',
          name: 'Précipitations',
          marker: { color: '#3498db' }
        }
      ],
      layout: {
        title: 'Prévisions de précipitations (7 jours)',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Pluie (mm)' }
      }
    };
  };

  if (loading) {
    return (
      <div className="spinner">
        <Spinner animation="border" variant="success" />
      </div>
    );
  }

  if (error) {
    return (
      <Container>
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container>
      <h2 className="mb-4">Tableau de bord agricole - {forecastData?.location ? `${forecastData.location.latitude}, ${forecastData.location.longitude}` : 'Dakar'}</h2>
      
      {weatherData && (
        <Row>
          <Col md={3} className="mb-3">
            <Card className="dashboard-card text-center">
              <Card.Body>
                <FaThermometerHalf className="weather-icon text-danger" />
                <Card.Title>{weatherData.temperature_celsius?.toFixed(1)}°C</Card.Title>
                <Card.Text className="text-muted">Température</Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} className="mb-3">
            <Card className="dashboard-card text-center">
              <Card.Body>
                <FaTint className="weather-icon text-primary" />
                <Card.Title>{weatherData.humidity_percent}%</Card.Title>
                <Card.Text className="text-muted">Humidité</Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} className="mb-3">
            <Card className="dashboard-card text-center">
              <Card.Body>
                <FaWind className="weather-icon text-info" />
                <Card.Title>{weatherData.wind_speed_ms?.toFixed(1)} m/s</Card.Title>
                <Card.Text className="text-muted">Vent</Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} className="mb-3">
            <Card className="dashboard-card text-center">
              <Card.Body>
                <FaCloudSun className="weather-icon text-warning" />
                <Card.Title>{weatherData.weather_description}</Card.Title>
                <Card.Text className="text-muted">Temps</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
      
      <Row className="mt-4">
        <Col lg={6}>
          <Card className="dashboard-card">
            <Card.Body>
              <Card.Title><FaThermometerHalf className="me-2" /> Prévisions de température</Card.Title>
              {getTempChart() && (
                <Plot
                  data={getTempChart().data}
                  layout={getTempChart().layout}
                  config={{ displayModeBar: false }}
                  style={{ width: '100%', height: '350px' }}
                />
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col lg={6}>
          <Card className="dashboard-card">
            <Card.Body>
              <Card.Title><FaTint className="me-2" /> Prévisions de précipitations</Card.Title>
              {getRainChart() && (
                <Plot
                  data={getRainChart().data}
                  layout={getRainChart().layout}
                  config={{ displayModeBar: false }}
                  style={{ width: '100%', height: '350px' }}
                />
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <Row className="mt-4">
        <Col>
          <Card className="dashboard-card">
            <Card.Body>
              <Card.Title><FaSeedling className="me-2" /> Indicateurs agricoles</Card.Title>
              <Alert variant="info">
                <FaExclamationTriangle className="me-2" />
                Basé sur les prévisions, irrigation recommandée dans 2 jours si pas de pluie
              </Alert>
              <Alert variant="warning">
                <FaExclamationTriangle className="me-2" />
                Risque modéré de maladies fongiques dans 3-4 jours (humidité > 75%)
              </Alert>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;