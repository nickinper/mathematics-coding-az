import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Alert,
  Divider,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import { useTheme } from '@mui/material/styles';

/**
 * A component for analyzing and displaying mathematical proofs
 */
const ProofAnalysis = ({ proof, feedback }) => {
  const theme = useTheme();
  const [activeStep, setActiveStep] = useState(0);
  
  // If no proof is provided, show a placeholder
  if (!proof || !proof.steps || proof.steps.length === 0) {
    return (
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Proof Analysis
        </Typography>
        <Alert severity="info">
          No proof has been submitted for analysis yet.
        </Alert>
      </Paper>
    );
  }
  
  const handleStepChange = (step) => {
    setActiveStep(step);
  };
  
  // Calculate overall validity
  const validSteps = proof.steps.filter(step => step.valid).length;
  const isProofValid = validSteps === proof.steps.length;
  const validityPercentage = Math.round((validSteps / proof.steps.length) * 100);
  
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Proof Analysis
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Alert severity={isProofValid ? "success" : "warning"}>
          <Typography variant="body2">
            {isProofValid 
              ? "Your proof is mathematically sound and follows logical steps." 
              : `Your proof has ${proof.steps.length - validSteps} invalid or unclear steps.`
            }
          </Typography>
        </Alert>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
          <Typography variant="body2">
            Valid steps: {validSteps}/{proof.steps.length} ({validityPercentage}%)
          </Typography>
          
          <Chip 
            label={proof.complexity_level} 
            color={
              proof.complexity_level === 'Elementary' ? 'success' :
              proof.complexity_level === 'Intermediate' ? 'primary' : 'secondary'
            }
            size="small"
          />
        </Box>
      </Box>
      
      <Divider sx={{ my: 2 }} />
      
      <Typography variant="subtitle1" gutterBottom>
        Proof Steps
      </Typography>
      
      <Stepper activeStep={activeStep} orientation="vertical">
        {proof.steps.map((step, index) => (
          <Step key={index} expanded>
            <StepLabel
              onClick={() => handleStepChange(index)}
              StepIconComponent={() => 
                step.valid 
                  ? <CheckCircleOutlineIcon color="success" /> 
                  : <ErrorOutlineIcon color="error" />
              }
            >
              <Typography variant="subtitle2">
                {step.description}
              </Typography>
            </StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" paragraph>
                  {step.details}
                </Typography>
                
                {step.valid ? (
                  <Alert severity="success" sx={{ mb: 2 }}>
                    {step.feedback}
                  </Alert>
                ) : (
                  <Alert severity="error" sx={{ mb: 2 }}>
                    {step.feedback}
                  </Alert>
                )}
                
                {step.suggestion && (
                  <Alert severity="info">
                    <Typography variant="body2">
                      <strong>Suggestion:</strong> {step.suggestion}
                    </Typography>
                  </Alert>
                )}
              </Box>
              <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
                <Button
                  disabled={index === 0}
                  onClick={() => handleStepChange(index - 1)}
                  size="small"
                >
                  Previous
                </Button>
                <Button
                  disabled={index === proof.steps.length - 1}
                  onClick={() => handleStepChange(index + 1)}
                  size="small"
                >
                  Next
                </Button>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
      
      <Divider sx={{ my: 3 }} />
      
      <Typography variant="subtitle1" gutterBottom>
        Mathematical Rigor Analysis
      </Typography>
      
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle2">
            Axioms and Definitions Used
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {proof.axioms_used?.map((axiom, index) => (
              <Chip key={index} label={axiom} size="small" />
            )) || (
              <Typography variant="body2" color="text.secondary">
                No specific axioms identified in this proof.
              </Typography>
            )}
          </Box>
        </AccordionDetails>
      </Accordion>
      
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle2">
            Proof Techniques
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {proof.techniques_used?.map((technique, index) => (
              <Chip key={index} label={technique} size="small" />
            )) || (
              <Typography variant="body2" color="text.secondary">
                No specific proof techniques identified.
              </Typography>
            )}
          </Box>
        </AccordionDetails>
      </Accordion>
      
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle2">
            Overall Feedback
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" paragraph>
            {feedback || "No overall feedback available for this proof."}
          </Typography>
          
          {proof.improvement_suggestions && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Suggestions for Improvement
              </Typography>
              <ul>
                {proof.improvement_suggestions.map((suggestion, index) => (
                  <li key={index}>
                    <Typography variant="body2">
                      {suggestion}
                    </Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}
        </AccordionDetails>
      </Accordion>
    </Paper>
  );
};

export default ProofAnalysis;