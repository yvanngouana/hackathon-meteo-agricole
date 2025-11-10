import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Table, Alert, Modal } from 'react-bootstrap';
import { FaBell, FaPlus, FaEdit, FaTrash, FaCheck, FaTimes } from 'react-icons/fa';
import axios from 'axios';

const WeatherAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentAlert, setCurrentAlert] = useState({
    id: null,
    name: '',
    location: { lat: 14.7167, lon: -17.4677 },
    conditions: {
      minTemp: null,
      maxTemp: null,
      minRain: null,
      maxRain: null,
      minHumidity: null,
      maxHumidity: null
    },
    active: true,
    frequency: 'daily'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Chargement des alertes existantes
  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      // Dans une vraie application, ceci serait un appel API
      // const response = await axios.get('/api/alerts');
      // setAlerts(response.data);
      
      // Pour démonstration, on simule des données
      setAlerts([
        {
          id: 1,
          name: 'Alerte Champ Sud',
          location: { lat: 14.7167, lon: -17.4677 },
          conditions: {
            minTemp: 10,
            maxTemp: 35,
            minRain: 5,
            maxRain: 50,
            minHumidity: 30,
            maxHumidity: 80
          },
          active: true,
          frequency: 'daily',
          created: new Date().toISOString()
        }
      ]);
    } catch (err) {
      setError('Erreur lors du chargement des alertes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'number') {
      setCurrentAlert(prev => ({
        ...prev,
        conditions: {
          ...prev.conditions,
          [name]: value ? parseFloat(value) : null
        }
      }));
    } else if (name in currentAlert.conditions) {
      setCurrentAlert(prev => ({
        ...prev,
        conditions: {
          ...prev.conditions,
          [name]: value ? parseFloat(value) : null
        }
      }));
    } else if (type === 'checkbox') {
      setCurrentAlert(prev => ({
        ...prev,
        [name]: checked
      }));
    } else {
      setCurrentAlert(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleLocationChange = (e) => {
    const { name, value } = e.target;
    setCurrentAlert(prev => ({
      ...prev,
      location: {
        ...prev.location,
        [name]: parseFloat(value)
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError('');
      
      if (currentAlert.id) {
        // Mise à jour d'une alerte existante
        // await axios.put(`/api/alerts/${currentAlert.id}`, currentAlert);
      } else {
        // Création d'une nouvelle alerte
        // await axios.post('/api/alerts', currentAlert);
      }
      
      // Actualiser la liste
      loadAlerts();
      setShowModal(false);
      setCurrentAlert({
        id: null,
        name: '',
        location: { lat: 14.7167, lon: -17.4677 },
        conditions: {
          minTemp: null,
          maxTemp: null,
          minRain: null,
          maxRain: null,
          minHumidity: null,
          maxHumidity: null
        },
        active: true,
        frequency: 'daily'
      });
    } catch (err) {
      setError('Erreur lors de l\'enregistrement de l\'alerte');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (alert) => {
    setCurrentAlert({
      ...alert,
      location: alert.location || { lat: 14.7167, lon: -17.4677 }
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette alerte ?')) {
      try {
        setLoading(true);
        // await axios.delete(`/api/alerts/${id}`);
        loadAlerts(); // Actualiser la liste
      } catch (err) {
        setError('Erreur lors de la suppression de l\'alerte');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  const toggleAlertStatus = async (id, isActive) => {
    try {
      setLoading(true);
      // await axios.patch(`/api/alerts/${id}/toggle`, { active: !isActive });
      loadAlerts(); // Actualiser la liste
    } catch (err) {
      setError('Erreur lors de la mise à jour de l\'état de l\'alerte');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <h2 className="mb-4">
        <FaBell className="me-2" /> Gestion des Alertes Météo
      </h2>

      {error && (
        <Alert variant="danger">{error}</Alert>
      )}

      <Row className="mb-4">
        <Col>
          <Button 
            variant="success" 
            onClick={() => {
              setCurrentAlert({
                id: null,
                name: '',
                location: { lat: 14.7167, lon: -17.4677 },
                conditions: {
                  minTemp: null,
                  maxTemp: null,
                  minRain: null,
                  maxRain: null,
                  minHumidity: null,
                  maxHumidity: null
                },
                active: true,
                frequency: 'daily'
              });
              setShowModal(true);
            }}
          >
            <FaPlus className="me-2" /> Nouvelle Alert
          </Button>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Table responsive>
                <thead>
                  <tr>
                    <th>Nom</th>
                    <th>Localisation</th>
                    <th>Conditions</th>
                    <th>Fréquence</th>
                    <th>Statut</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {alerts.map(alert => (
                    <tr key={alert.id}>
                      <td>{alert.name}</td>
                      <td>{alert.location.lat.toFixed(4)}, {alert.location.lon.toFixed(4)}</td>
                      <td>
                        Temp: {alert.conditions.minTemp || 'N/A'}°C - {alert.conditions.maxTemp || 'N/A'}°C<br />
                        Pluie: {alert.conditions.minRain || 'N/A'}mm - {alert.conditions.maxRain || 'N/A'}mm<br />
                        Humidité: {alert.conditions.minHumidity || 'N/A'}% - {alert.conditions.maxHumidity || 'N/A'}%
                      </td>
                      <td>{alert.frequency}</td>
                      <td>
                        <Button 
                          variant={alert.active ? "success" : "secondary"} 
                          size="sm"
                          onClick={() => toggleAlertStatus(alert.id, alert.active)}
                        >
                          {alert.active ? <FaCheck className="me-1" /> : <FaTimes className="me-1" />}
                          {alert.active ? 'Actif' : 'Inactif'}
                        </Button>
                      </td>
                      <td>
                        <Button 
                          variant="outline-primary" 
                          size="sm" 
                          className="me-2"
                          onClick={() => handleEdit(alert)}
                        >
                          <FaEdit />
                        </Button>
                        <Button 
                          variant="outline-danger" 
                          size="sm"
                          onClick={() => handleDelete(alert.id)}
                        >
                          <FaTrash />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Modal pour créer/modifier une alerte */}
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {currentAlert.id ? 'Modifier l\'alerte' : 'Créer une nouvelle alerte'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Nom de l'alerte</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={currentAlert.name}
                onChange={handleInputChange}
                required
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Latitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="lat"
                    value={currentAlert.location.lat}
                    onChange={handleLocationChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Longitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="lon"
                    value={currentAlert.location.lon}
                    onChange={handleLocationChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <h5 className="mt-4 mb-3">Conditions d'alerte</h5>
            
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Température minimale (°C)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="minTemp"
                    value={currentAlert.conditions.minTemp || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Température maximale (°C)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="maxTemp"
                    value={currentAlert.conditions.maxTemp || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Précipitations minimales (mm)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="minRain"
                    value={currentAlert.conditions.minRain || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Précipitations maximales (mm)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="maxRain"
                    value={currentAlert.conditions.maxRain || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Humidité minimale (%)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="minHumidity"
                    value={currentAlert.conditions.minHumidity || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Humidité maximale (%)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    name="maxHumidity"
                    value={currentAlert.conditions.maxHumidity || ''}
                    onChange={handleInputChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Fréquence</Form.Label>
              <Form.Select
                name="frequency"
                value={currentAlert.frequency}
                onChange={handleInputChange}
              >
                <option value="hourly">Toutes les heures</option>
                <option value="daily">Quotidien</option>
                <option value="weekly">Hebdomadaire</option>
              </Form.Select>
            </Form.Group>

            <Form.Check 
              type="switch"
              id="active-switch"
              label="Alerte active"
              name="active"
              checked={currentAlert.active}
              onChange={(e) => setCurrentAlert(prev => ({ ...prev, active: e.target.checked }))}
            />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Annuler
            </Button>
            <Button variant="success" type="submit" disabled={loading}>
              {loading ? 'Enregistrement...' : (currentAlert.id ? 'Modifier' : 'Créer')}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </Container>
  );
};

export default WeatherAlerts;