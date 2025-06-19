import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  TextField,
  MenuItem,
  FormControl,
  FormControlLabel,
  InputLabel,
  Select,
  Switch,
  Chip,
  CircularProgress,
  Alert,
  Snackbar,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  CardActions,
  Divider
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import SaveIcon from '@mui/icons-material/Save';
import FunctionsIcon from '@mui/icons-material/Functions';
import BarChartIcon from '@mui/icons-material/BarChart';
import SchoolIcon from '@mui/icons-material/School';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

/**
 * Task Generator page
 */
const TaskGenerator = () => {
  const [domains, setDomains] = useState([
    'number_theory', 'linear_algebra', 'calculus', 'probability',
    'differential_equations', 'optimization_techniques', 'graph_theory',
    'combinatorics', 'abstract_algebra', 'topology', 'model_theory'
  ]);
  
  const [levels, setLevels] = useState([
    'foundation', 'intermediate', 'advanced'
  ]);
  
  const [generationParams, setGenerationParams] = useState({
    domain: 'number_theory',
    level: 'intermediate',
    strategy: 'template_based',
    parameters: {}
  });
  
  const [customParameters, setCustomParameters] = useState({
    number: 1234,
    complexity: 'medium'
  });
  
  const [generatedChallenge, setGeneratedChallenge] = useState(null);
  const [generationHistory, setGenerationHistory] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info'
  });
  
  // Load history on component mount
  useEffect(() => {
    // In a real app, you would fetch history from API
    const mockHistory = [
      {
        id: 'hist_1',
        title: 'Prime Factorization Challenge',
        domain: 'number_theory',
        level: 'intermediate',
        generated_at: '2025-06-18T14:30:00Z'
      },
      {
        id: 'hist_2',
        title: 'Matrix Eigenvalue Problem',
        domain: 'linear_algebra',
        level: 'advanced',
        generated_at: '2025-06-17T09:15:00Z'
      }
    ];
    
    setGenerationHistory(mockHistory);
  }, []);
  
  // Handle parameter change
  const handleParamChange = (event) => {
    setGenerationParams({
      ...generationParams,
      [event.target.name]: event.target.value
    });
  };
  
  // Handle custom parameter change
  const handleCustomParamChange = (event) => {
    setCustomParameters({
      ...customParameters,
      [event.target.name]: event.target.value
    });
  };
  
  // Generate challenge
  const handleGenerateChallenge = async () => {
    setIsGenerating(true);
    
    try {
      // In a real app, this would be an API call
      // const response = await axios.post('/api/generation/generate', {
      //   ...generationParams,
      //   parameters: customParameters
      // });
      
      // Mock response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockResponse = {
        id: `gen_${Date.now()}`,
        title: "Prime Factorization Challenge",
        description: `
# Prime Factorization Challenge

## Problem Statement

Find the prime factorization of the number ${customParameters.number}.

## Mathematical Foundation

A prime number is a natural number greater than 1 that is not a product of two smaller natural numbers.
The prime factorization of a number is the product of prime numbers that equals the original number.

## Task

Your task is to implement a function \`prime_factorize(n)\` that:

1. Takes an integer \`n\` as input
2. Returns a list of prime factors of \`n\` in ascending order
3. For repeated prime factors, the prime should appear multiple times in the result

## Example

\`\`\`
Input: 60
Output: [2, 2, 3, 5]
\`\`\`

Explanation: 60 = 2 × 2 × 3 × 5

## Requirements

1. Your solution should handle inputs up to 10^9
2. Time complexity analysis is required
3. Explain the mathematical principles behind your approach
        `,
        domain: generationParams.domain,
        level: generationParams.level,
        mathematical_requirements: [
          {
            concept: "Prime Numbers",
            description: "Understanding of prime numbers and their properties",
            proof_required: true
          },
          {
            concept: "Factorization Algorithms",
            description: "Knowledge of efficient factorization techniques",
            proof_required: false,
            complexity_analysis: true
          }
        ],
        test_cases: [
          {
            input_data: { "input": 60, "function": "prime_factorize" },
            expected_output: [2, 2, 3, 5],
            description: "Test with 60"
          },
          {
            input_data: { "input": 100, "function": "prime_factorize" },
            expected_output: [2, 2, 5, 5],
            description: "Test with 100"
          },
          {
            input_data: { "input": customParameters.number, "function": "prime_factorize" },
            expected_output: "To be calculated",
            description: `Test with ${customParameters.number}`
          }
        ],
        time_limit: 600.0
      };
      
      setGeneratedChallenge(mockResponse);
      
      // Add to history
      setGenerationHistory([mockResponse, ...generationHistory]);
      
      showSnackbar('Challenge generated successfully', 'success');
    } catch (error) {
      showSnackbar(`Error generating challenge: ${error.message}`, 'error');
    } finally {
      setIsGenerating(false);
    }
  };
  
  // Save challenge to database
  const handleSaveChallenge = async () => {
    if (!generatedChallenge) return;
    
    setIsSaving(true);
    
    try {
      // In a real app, this would be an API call
      // const response = await axios.post('/api/generation/save', generatedChallenge);
      
      // Mock response
      await new Promise(resolve => setTimeout(resolve, 800));
      
      showSnackbar('Challenge saved to database', 'success');
    } catch (error) {
      showSnackbar(`Error saving challenge: ${error.message}`, 'error');
    } finally {
      setIsSaving(false);
    }
  };
  
  // Show snackbar message
  const showSnackbar = (message, severity = 'info') => {
    setSnackbar({
      open: true,
      message,
      severity
    });
  };
  
  // Close snackbar
  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };
  
  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <AutoFixHighIcon sx={{ mr: 1 }} />
          Challenge Generator
        </Typography>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          Generate mathematics-based coding challenges using customizable templates and parameters.
          These challenges can be saved to the platform and assigned to users.
        </Typography>
        
        <Grid container spacing={3}>
          {/* Generation parameters */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                <FunctionsIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
                Generation Parameters
              </Typography>
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="domain-label">Mathematical Domain</InputLabel>
                <Select
                  labelId="domain-label"
                  name="domain"
                  value={generationParams.domain}
                  onChange={handleParamChange}
                  label="Mathematical Domain"
                >
                  {domains.map(domain => (
                    <MenuItem key={domain} value={domain}>
                      {domain.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="level-label">Difficulty Level</InputLabel>
                <Select
                  labelId="level-label"
                  name="level"
                  value={generationParams.level}
                  onChange={handleParamChange}
                  label="Difficulty Level"
                >
                  {levels.map(level => (
                    <MenuItem key={level} value={level}>
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="strategy-label">Generation Strategy</InputLabel>
                <Select
                  labelId="strategy-label"
                  name="strategy"
                  value={generationParams.strategy}
                  onChange={handleParamChange}
                  label="Generation Strategy"
                >
                  <MenuItem value="template_based">Template Based</MenuItem>
                  <MenuItem value="parameterized">Parameterized</MenuItem>
                  <MenuItem value="adaptive">Adaptive</MenuItem>
                  <MenuItem value="learning_path">Learning Path</MenuItem>
                </Select>
              </FormControl>
              
              <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                Custom Parameters
              </Typography>
              
              <TextField
                label="Number"
                name="number"
                type="number"
                value={customParameters.number}
                onChange={handleCustomParamChange}
                fullWidth
                margin="dense"
              />
              
              <FormControl fullWidth margin="dense">
                <InputLabel id="complexity-label">Complexity</InputLabel>
                <Select
                  labelId="complexity-label"
                  name="complexity"
                  value={customParameters.complexity}
                  onChange={handleCustomParamChange}
                  label="Complexity"
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
              
              <Box sx={{ mt: 3 }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={isGenerating ? <CircularProgress size={20} color="inherit" /> : <AutoFixHighIcon />}
                  onClick={handleGenerateChallenge}
                  disabled={isGenerating}
                  fullWidth
                >
                  {isGenerating ? 'Generating...' : 'Generate Challenge'}
                </Button>
              </Box>
            </Paper>
          </Grid>
          
          {/* Generated challenge */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  <SchoolIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
                  Generated Challenge
                </Typography>
                
                {generatedChallenge && (
                  <Button
                    variant="outlined"
                    color="primary"
                    startIcon={isSaving ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
                    onClick={handleSaveChallenge}
                    disabled={isSaving}
                  >
                    {isSaving ? 'Saving...' : 'Save to Database'}
                  </Button>
                )}
              </Box>
              
              {generatedChallenge ? (
                <Box>
                  <Typography variant="h5" gutterBottom>
                    {generatedChallenge.title}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                    <Chip 
                      label={generatedChallenge.domain.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} 
                      color="primary" 
                      variant="outlined" 
                      size="small"
                    />
                    <Chip 
                      label={generatedChallenge.level.charAt(0).toUpperCase() + generatedChallenge.level.slice(1)} 
                      color="secondary" 
                      variant="outlined" 
                      size="small"
                    />
                  </Box>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <Box sx={{ bgcolor: 'background.default', p: 2, borderRadius: 1, mb: 2 }}>
                    <ReactMarkdown>
                      {generatedChallenge.description}
                    </ReactMarkdown>
                  </Box>
                  
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography>Mathematical Requirements</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      {generatedChallenge.mathematical_requirements.map((req, index) => (
                        <Box key={index} sx={{ mb: 1 }}>
                          <Typography variant="subtitle2">
                            {req.concept}
                          </Typography>
                          <Typography variant="body2">
                            {req.description}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                            {req.proof_required && (
                              <Chip label="Proof Required" size="small" color="info" variant="outlined" />
                            )}
                            {req.complexity_analysis && (
                              <Chip label="Complexity Analysis" size="small" color="info" variant="outlined" />
                            )}
                          </Box>
                        </Box>
                      ))}
                    </AccordionDetails>
                  </Accordion>
                  
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography>Test Cases</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      {generatedChallenge.test_cases.map((test, index) => (
                        <Box key={index} sx={{ mb: 1 }}>
                          <Typography variant="subtitle2">
                            {test.description}
                          </Typography>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                            Input: {JSON.stringify(test.input_data)}
                          </Typography>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                            Expected: {JSON.stringify(test.expected_output)}
                          </Typography>
                        </Box>
                      ))}
                    </AccordionDetails>
                  </Accordion>
                </Box>
              ) : (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    No challenge generated yet. Set parameters and click "Generate Challenge".
                  </Typography>
                </Box>
              )}
            </Paper>
            
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                <BarChartIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
                Generation History
              </Typography>
              
              {generationHistory.length > 0 ? (
                <Grid container spacing={2}>
                  {generationHistory.map(challenge => (
                    <Grid item xs={12} sm={6} key={challenge.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            {challenge.title}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                            <Chip 
                              label={challenge.domain.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} 
                              size="small" 
                              color="primary" 
                              variant="outlined" 
                            />
                            <Chip 
                              label={challenge.level.charAt(0).toUpperCase() + challenge.level.slice(1)} 
                              size="small" 
                              color="secondary" 
                              variant="outlined" 
                            />
                          </Box>
                          <Typography variant="body2" color="text.secondary">
                            Generated: {new Date(challenge.generated_at).toLocaleString()}
                          </Typography>
                        </CardContent>
                        <CardActions>
                          <Button size="small">View</Button>
                          <Button size="small">Regenerate</Button>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Alert severity="info">
                  No generation history available
                </Alert>
              )}
            </Paper>
          </Grid>
        </Grid>
      </Box>
      
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default TaskGenerator;