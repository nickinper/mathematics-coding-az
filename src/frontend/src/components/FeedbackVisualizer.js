import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Divider,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme
} from '@mui/material';
import {
  Check as CheckIcon,
  Close as CloseIcon,
  Info as InfoIcon,
  Lightbulb as LightbulbIcon,
  Equalizer as EqualizerIcon,
  Timeline as TimelineIcon,
  BugReport as BugIcon,
  Functions as FunctionsIcon
} from '@mui/icons-material';

const ScoreGauge = ({ score, label, color }) => {
  const theme = useTheme();
  const getColor = () => {
    if (!color) {
      if (score >= 0.7) return theme.palette.success.main;
      if (score >= 0.4) return theme.palette.warning.main;
      return theme.palette.error.main;
    }
    return color;
  };

  return (
    <Box sx={{ textAlign: 'center', p: 1 }}>
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <Box
          sx={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            border: `8px solid ${theme.palette.grey[200]}`,
            position: 'relative',
          }}
        >
          <Box
            sx={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              position: 'absolute',
              top: -8,
              left: -8,
              border: '8px solid',
              borderColor: `${getColor()} ${theme.palette.grey[200]} ${theme.palette.grey[200]} ${theme.palette.grey[200]}`,
              transform: `rotate(${score * 360}deg)`,
              transition: 'transform 1s ease-out',
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              bottom: 0,
              right: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
              {Math.round(score * 100)}
            </Typography>
          </Box>
        </Box>
      </Box>
      <Typography variant="body2" sx={{ mt: 1 }}>
        {label}
      </Typography>
    </Box>
  );
};

const ConceptItem = ({ concept, confidence, mastery, evidence }) => {
  const theme = useTheme();
  const getColor = (value) => {
    if (value >= 0.7) return theme.palette.success.main;
    if (value >= 0.4) return theme.palette.warning.main;
    return theme.palette.error.main;
  };

  const masteryColor = getColor(mastery);
  const confidenceColor = getColor(confidence);

  return (
    <Paper sx={{ p: 2, mb: 2, border: `1px solid ${masteryColor}` }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="subtitle1">
          {concept.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
        </Typography>
        <Chip
          label={`${Math.round(mastery * 100)}% Mastery`}
          size="small"
          sx={{ bgcolor: masteryColor, color: 'white' }}
        />
      </Box>
      
      <Typography variant="body2" sx={{ mb: 1 }}>
        {evidence}
      </Typography>
      
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Typography variant="caption" sx={{ mr: 1 }}>
          Confidence:
        </Typography>
        <Box sx={{ flexGrow: 1, mr: 1 }}>
          <LinearProgress
            variant="determinate"
            value={confidence * 100}
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: theme.palette.grey[200],
              '& .MuiLinearProgress-bar': {
                backgroundColor: confidenceColor,
                borderRadius: 4,
              },
            }}
          />
        </Box>
        <Typography variant="caption">
          {Math.round(confidence * 100)}%
        </Typography>
      </Box>
    </Paper>
  );
};

const ProofStep = ({ step, index }) => {
  const theme = useTheme();
  
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        mb: 1,
        backgroundColor: step.is_valid 
          ? theme.palette.mode === 'dark' 
            ? theme.palette.success.dark 
            : theme.palette.success.light
          : theme.palette.mode === 'dark'
            ? theme.palette.error.dark
            : theme.palette.error.light,
        borderLeft: `4px solid ${step.is_valid ? theme.palette.success.main : theme.palette.error.main}`,
      }}
    >
      <Box sx={{ display: 'flex', mb: 1 }}>
        <Typography variant="body2" sx={{ fontWeight: 'bold', mr: 1 }}>
          Step {index + 1}:
        </Typography>
        <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
          {step.statement}
        </Typography>
      </Box>
      
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="caption">
          Justification: {step.justification}
        </Typography>
        <Chip
          icon={step.is_valid ? <CheckIcon /> : <CloseIcon />}
          label={step.is_valid ? "Valid" : "Invalid"}
          size="small"
          color={step.is_valid ? "success" : "error"}
          variant="outlined"
        />
      </Box>
    </Paper>
  );
};

const FeedbackVisualizer = ({ feedback }) => {
  const theme = useTheme();
  
  if (!feedback) return null;
  
  const { validation_result } = feedback;
  
  return (
    <Box sx={{ mt: 2 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <EqualizerIcon sx={{ mr: 1 }} /> Overall Assessment
        </Typography>
        
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <ScoreGauge 
              score={validation_result.scores.mathematical_rigor} 
              label="Mathematical Rigor" 
              color={theme.palette.primary.main}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <ScoreGauge 
              score={validation_result.scores.proof_correctness} 
              label="Proof Correctness" 
              color={theme.palette.secondary.main}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <ScoreGauge 
              score={validation_result.scores.code_elegance} 
              label="Code Elegance" 
              color="#1565C0"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <ScoreGauge 
              score={validation_result.scores.concept_mastery} 
              label="Concept Mastery" 
              color="#7B1FA2"
            />
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          <FunctionsIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
          Mathematical Concepts Analysis
        </Typography>
        
        <Grid container spacing={2}>
          {validation_result.concepts_identified.map((concept, index) => (
            <Grid item xs={12} md={6} key={index}>
              <ConceptItem
                concept={concept.concept}
                confidence={concept.confidence}
                mastery={concept.mastery_level}
                evidence={concept.evidence}
              />
            </Grid>
          ))}
        </Grid>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          <TimelineIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
          Proof Analysis
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Typography variant="body2" sx={{ mr: 2 }}>
              {validation_result.proof_analysis.steps_found} steps identified
            </Typography>
            <Typography variant="body2">
              {validation_result.proof_analysis.valid_steps} valid steps
            </Typography>
          </Box>
          
          {validation_result.proof_analysis.proof_steps.map((step, index) => (
            <ProofStep key={index} step={step} index={index} />
          ))}
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          <BugIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
          Code Analysis
        </Typography>
        
        <Paper sx={{ p: 2, bgcolor: theme.palette.background.default }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Complexity: {validation_result.code_analysis.complexity}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Typography variant="body2" sx={{ width: 120 }}>
                  Efficiency:
                </Typography>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={validation_result.code_analysis.efficiency_score * 100}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: theme.palette.grey[200],
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: theme.palette.primary.main,
                        borderRadius: 4,
                      },
                    }}
                  />
                </Box>
                <Typography variant="body2">
                  {Math.round(validation_result.code_analysis.efficiency_score * 100)}%
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography variant="body2" sx={{ width: 120 }}>
                  Readability:
                </Typography>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={validation_result.code_analysis.readability_score * 100}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: theme.palette.grey[200],
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: theme.palette.secondary.main,
                        borderRadius: 4,
                      },
                    }}
                  />
                </Box>
                <Typography variant="body2">
                  {Math.round(validation_result.code_analysis.readability_score * 100)}%
                </Typography>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                Patterns Identified
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {validation_result.code_analysis.patterns_identified.map((pattern, index) => (
                  <Chip key={index} label={pattern} size="small" />
                ))}
              </Box>
            </Grid>
          </Grid>
        </Paper>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          <InfoIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
          Detailed Feedback
        </Typography>
        
        <Paper sx={{ p: 2, bgcolor: theme.palette.background.default }}>
          <Typography variant="body1">
            {validation_result.feedback}
          </Typography>
        </Paper>
        
        <Divider sx={{ my: 2 }} />
        
        <Typography variant="h6" gutterBottom>
          <LightbulbIcon sx={{ mr: 1, verticalAlign: 'middle' }} fontSize="small" />
          Suggestions for Improvement
        </Typography>
        
        <List sx={{ bgcolor: theme.palette.background.default, borderRadius: 1 }}>
          {validation_result.suggestions.map((suggestion, index) => (
            <ListItem key={index}>
              <ListItemIcon>
                <LightbulbIcon color="warning" />
              </ListItemIcon>
              <ListItemText primary={suggestion} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default FeedbackVisualizer;