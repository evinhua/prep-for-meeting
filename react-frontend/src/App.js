import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  TextField, 
  Button, 
  Paper, 
  LinearProgress,
  Chip,
  Grid,
  Card,
  CardContent,
  IconButton,
  Snackbar,
  Alert
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  // State for form inputs
  const [formData, setFormData] = useState({
    participants: [
      'Jensen Huang <jensen.huang@nvidia.com>', 
      'Mark Zuckerberg <mark.zuckerberg@meta.com>', 
      'Elon Musk <elon.musk@tesla.coom>'
    ],
    company: "Future AI News",
    context: "Sharing the latest AI news from the recent two weeks",
    objective: "Summarize the latest AI news and creating working action points",
    prior_interactions: "providing latest roadmap in each company",
  });

  // State for new participant input
  const [newParticipant, setNewParticipant] = useState('');
  
  // State for progress and results
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle adding a new participant
  const handleAddParticipant = () => {
    if (newParticipant.trim()) {
      setFormData({
        ...formData,
        participants: [...formData.participants, newParticipant.trim()]
      });
      setNewParticipant('');
    }
  };

  // Handle removing a participant
  const handleRemoveParticipant = (index) => {
    const updatedParticipants = [...formData.participants];
    updatedParticipants.splice(index, 1);
    setFormData({
      ...formData,
      participants: updatedParticipants
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setProgress(0);
    setResult(null);
    setError(null);

    try {
      // Make API call to backend
      const response = await axios.post('/api/run-crew', formData);
      const jobId = response.data.job_id;
      
      // Poll for job status
      const statusInterval = setInterval(async () => {
        try {
          const statusResponse = await axios.get(`/api/job/${jobId}`);
          const jobStatus = statusResponse.data;
          
          // Update progress
          setProgress(jobStatus.progress || 0);
          
          // Check if job is completed or failed
          if (jobStatus.status === 'completed') {
            clearInterval(statusInterval);
            setResult({
              content: jobStatus.content,
              downloadUrl: jobStatus.downloadUrl
            });
            setProgress(100);
            setIsLoading(false);
          } else if (jobStatus.status === 'failed') {
            clearInterval(statusInterval);
            setError(jobStatus.error || 'Job failed');
            setIsLoading(false);
          }
        } catch (pollError) {
          console.error('Error polling job status:', pollError);
        }
      }, 2000); // Poll every 2 seconds
      
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred while processing your request');
      setIsLoading(false);
    }
  };

  // Simulate progress for better UX - Not needed anymore as we get real progress from backend
  // const simulateProgress = () => {
  //   return setInterval(() => {
  //     setProgress((prevProgress) => {
  //       const diff = Math.random() * 10;
  //       return Math.min(prevProgress + diff, 95);
  //     });
  //   }, 1000);
  // };

  // Handle closing the error alert
  const handleCloseError = () => {
    setError(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Meeting Preparation Assistant
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Meeting Participants
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                    {formData.participants.map((participant, index) => (
                      <Chip
                        key={index}
                        label={participant}
                        onDelete={() => handleRemoveParticipant(index)}
                        deleteIcon={<DeleteIcon />}
                        color="primary"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <TextField
                      fullWidth
                      label="Add Participant (name <email>)"
                      value={newParticipant}
                      onChange={(e) => setNewParticipant(e.target.value)}
                      variant="outlined"
                      size="small"
                    />
                    <IconButton 
                      color="primary" 
                      onClick={handleAddParticipant}
                      sx={{ border: '1px solid', borderColor: 'primary.main' }}
                    >
                      <AddIcon />
                    </IconButton>
                  </Box>
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Company"
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                    variant="outlined"
                    required
                    margin="normal"
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Objective"
                    name="objective"
                    value={formData.objective}
                    onChange={handleInputChange}
                    variant="outlined"
                    required
                    margin="normal"
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Context"
                    name="context"
                    value={formData.context}
                    onChange={handleInputChange}
                    variant="outlined"
                    required
                    multiline
                    rows={2}
                    margin="normal"
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Prior Interactions"
                    name="prior_interactions"
                    value={formData.prior_interactions}
                    onChange={handleInputChange}
                    variant="outlined"
                    multiline
                    rows={2}
                    margin="normal"
                  />
                </Grid>

                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    size="large"
                    fullWidth
                    disabled={isLoading}
                  >
                    {isLoading ? 'Generating...' : 'Generate Meeting Preparation'}
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Paper>

          {isLoading && (
            <Box sx={{ width: '100%', mb: 4 }}>
              <Typography variant="body1" gutterBottom>
                Generating your meeting preparation materials... This may take a few minutes.
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={progress} 
                sx={{ height: 10, borderRadius: 5 }}
              />
              <Typography variant="body2" color="text.secondary" align="right">
                {Math.round(progress)}%
              </Typography>
            </Box>
          )}

          {result && (
            <Card variant="outlined" sx={{ mb: 4 }}>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Meeting Preparation Complete
                </Typography>
                <Typography variant="body1" paragraph>
                  Your meeting preparation materials have been generated successfully.
                </Typography>
                
                <Box sx={{ mt: 2, p: 2, bgcolor: '#f8f9fa', borderRadius: 1, overflow: 'auto', maxHeight: '500px' }}>
                  <Typography variant="h6" gutterBottom>
                    Report Preview
                  </Typography>
                  <div 
                    dangerouslySetInnerHTML={{ 
                      __html: result.content ? result.content.replace(/\n/g, '<br>') : '' 
                    }} 
                  />
                </Box>
                
                {result.downloadUrl && (
                  <Button 
                    variant="contained" 
                    color="primary"
                    sx={{ mt: 2 }}
                    href={result.downloadUrl}
                    target="_blank"
                  >
                    Download Report
                  </Button>
                )}
              </CardContent>
            </Card>
          )}
        </Box>
      </Container>
      
      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseError}>
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
}

export default App;
