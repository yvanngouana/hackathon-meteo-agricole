import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Table, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';
import { FaPlus, FaTrash, FaEdit, FaMapMarkerAlt } from 'react-icons/fa';

const FieldManagement = () => {
  const [fields, setFields] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    latitude: '',
    longitude: '',
    crop_type: '',
    area_hectares: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('success');

  useEffect(() => {
    fetchFields();
  }, []);

  const fetchFields = async () => {
    try {
      setLoading(true);
      // In a real app, we would fetch from the API
      // For now, using mock data
      const mockFields = [
        {
          id: 1,
          name: 'Champ Nord',
          latitude: 14.7167,
          longitude: -17.4677,
          crop_type: 'riz',
          area_hectares: 2.5,
          created_at: '2024-01-15'
        },
        {
          id: 2,
          name: 'Champ Sud',
          latitude: 14.6969,
          longitude: -17.4440,
          crop_type: 'millet',
          area_hectares: 1.8,
          created_at: '2024-01-20'
        }
      ];
      setFields(mockFields);
      setLoading(false);
    } catch (error) {
      setMessage('Erreur lors de la récupération des champs');
      setMessageType('danger');
      setLoading(false);
      console.error(error);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      
      // Mock API call for now
      const newField = {
        id: fields.length + 1,
        ...formData,
        area_hectares: parseFloat(formData.area_hectares),
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        created_at: new Date().toISOString().split('T')[0]
      };
      
      setFields([...fields, newField]);
      
      setMessage('Champ créé avec succès !');
      setMessageType('success');
      
      // Reset form
      setFormData({
        name: '',
        latitude: '',
        longitude: '',
        crop_type: '',
        area_hectares: ''
      });
      
      setLoading(false);
    } catch (error) {
      setMessage('Erreur lors de la création du champ');
      setMessageType('danger');
      setLoading(false);
      console.error(error);
    }
  };

  const deleteField = (id) => {
    setFields(fields.filter(field => field.id !== id));
    setMessage('Champ supprimé avec succès !');
    setMessageType('success');
  };

  return (
    <Container>
      <Row>
        <Col md={8}>
          <h2 className="mb-4">Gestion des Champs Agricoles</h2>
          
          {message && (
            <Alert variant={messageType}>
              {message}
            </Alert>
          )}
          
          <Card className="dashboard-card">
            <Card.Body>
              <Card.Title><FaMapMarkerAlt className="me-2" /> Liste des Champs</Card.Title>
              
              {loading ? (
                <div className="text-center my-4">
                  <Spinner animation="border" variant="success" />
                </div>
              ) : (
                <Table striped hover responsive>
                  <thead>
                    <tr>
                      <th>Nom</th>
                      <th>Coordonnées</th>
                      <th>Culture</th>
                      <th>Superficie (ha)</th>
                      <th>Créé le</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {fields.map(field => (
                      <tr key={field.id}>
                        <td>{field.name}</td>
                        <td>{field.latitude.toFixed(4)}, {field.longitude.toFixed(4)}</td>
                        <td>{field.crop_type}</td>
                        <td>{field.area_hectares}</td>
                        <td>{field.created_at}</td>
                        <td>
                          <Button 
                            variant="outline-danger" 
                            size="sm" 
                            onClick={() => deleteField(field.id)}
                            className="me-2"
                          >
                            <FaTrash />
                          </Button>
                          <Button variant="outline-primary" size="sm">
                            <FaEdit />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="dashboard-card">
            <Card.Body>
              <Card.Title><FaPlus className="me-2" /> Ajouter un Champ</Card.Title>
              
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Nom du champ</Form.Label>
                  <Form.Control
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>Latitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="latitude"
                    value={formData.latitude}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>Longitude</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="longitude"
                    value={formData.longitude}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>Type de culture</Form.Label>
                  <Form.Select
                    name="crop_type"
                    value={formData.crop_type}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Sélectionner une culture</option>
                    <option value="rice">Riz</option>
                    <option value="millet">Millet</option>
                    <option value="maize">Maïs</option>
                    <option value="groundnut">Arachide</option>
                    <option value="cotton">Coton</option>
                    <option value="mixed">Mixte</option>
                  </Form.Select>
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>Superficie (hectares)</Form.Label>
                  <Form.Control
                    type="number"
                    step="any"
                    name="area_hectares"
                    value={formData.area_hectares}
                    onChange={handleInputChange}
                    required
                  />
                </Form.Group>
                
                <Button 
                  variant="success" 
                  type="submit" 
                  disabled={loading}
                  className="w-100"
                >
                  {loading ? (
                    <>
                      <Spinner
                        as="span"
                        animation="border"
                        size="sm"
                        role="status"
                        className="me-2"
                      />
                      Chargement...
                    </>
                  ) : (
                    <><FaPlus className="me-2" /> Ajouter le Champ</>
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default FieldManagement;