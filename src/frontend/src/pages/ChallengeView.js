import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Button, 
  Grid, 
  CircularProgress, 
  Paper, 
  Divider,
  Tabs,
  Tab,
  Alert,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  Drawer,
  AppBar,
  Toolbar,
} from '@mui/material';
import {
  Send as SendIcon,
  Save as SaveIcon,
  PlayArrow as RunIcon,
  Close as CloseIcon,
  Info as InfoIcon,
  Help as HelpIcon,
  Lightbulb as TipIcon,
  ArrowBack as BackIcon,
  BarChart as ResultsIcon,
  Code as CodeIcon,
  Article as ArticleIcon,
  Functions as MathIcon,
  BugReport as BugIcon
} from '@mui/icons-material';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import axios from 'axios';
import { useAuth } from '../services/AuthContext';
import ReactMarkdown from 'react-markdown';
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';

// Components for feedback visualization
import FeedbackVisualizer from '../components/FeedbackVisualizer';
import MathematicalConceptsGraph from '../components/MathematicalConceptsGraph';
import ProofAnalysis from '../components/ProofAnalysis';

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`challenge-tabpanel-${index}`}
      aria-labelledby={`challenge-tab-${index}`}
      {...other}
      style={{ height: '100%' }}
    >
      {value === index && (
        <Box sx={{ height: '100%', pt: 2 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

// For rendering mathematical formulas in markdown
const MarkdownWithMath = ({ children }) => {
  return (
    <ReactMarkdown
      children={children}
      components={{
        // eslint-disable-next-line react/display-name
        p: ({ node, ...props }) => <Typography variant="body1" gutterBottom {...props} />,
        // eslint-disable-next-line react/display-name
        h1: ({ node, ...props }) => <Typography variant="h4" gutterBottom {...props} />,
        // eslint-disable-next-line react/display-name
        h2: ({ node, ...props }) => <Typography variant="h5" gutterBottom {...props} />,
        // eslint-disable-next-line react/display-name
        h3: ({ node, ...props }) => <Typography variant="h6" gutterBottom {...props} />,
        // eslint-disable-next-line react/display-name
        code: ({ node, inline, ...props }) => 
          inline ? (
            <code {...props} style={{ backgroundColor: '#f5f5f5', padding: '2px 4px', borderRadius: 4 }} />
          ) : (
            <Paper elevation={0} sx={{ p: 2, my: 2, bgcolor: '#f5f5f5', overflow: 'auto' }}>
              <code {...props} style={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }} />
            </Paper>
          ),
        // Custom renderer for math
        // eslint-disable-next-line react/display-name
        inlineMath: ({ value }) => <InlineMath math={value} />,
        // eslint-disable-next-line react/display-name
        math: ({ value }) => <BlockMath math={value} />
      }}
    />
  );
};

const ChallengeView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [challenge, setChallenge] = useState(null);
  const [code, setCode] = useState('# Your solution here\n\n');
  const [mathReasoning, setMathReasoning] = useState('# Explain your mathematical reasoning here\n\n');
  const [tabValue, setTabValue] = useState(0);
  const [feedback, setFeedback] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  
  // Fetch challenge data
  useEffect(() => {
    const fetchChallenge = async () => {
      try {
        const response = await axios.get(`/api/challenges/${id}/details`);
        setChallenge(response.data);
        
        // Pre-populate code with template if available
        if (response.data.code_template) {
          setCode(response.data.code_template);
        }
        
        // Pre-populate math reasoning with template if available
        if (response.data.reasoning_template) {
          setMathReasoning(response.data.reasoning_template);
        }
      } catch (error) {
        console.error('Error fetching challenge:', error);
        // For demo, use sample data
        setChallenge({
          id: parseInt(id),
          title: "Modular Exponentiation Challenge",
          description: `
# Modular Exponentiation Challenge

Your task is to implement an efficient algorithm for modular exponentiation.

## Problem Statement

Given three integers $a$, $b$, and $m$, compute $a^b \\mod m$.

For example, to calculate $3^{200} \\mod 17$, a naive approach would compute $3^{200}$ (a very large number) and then take the remainder when divided by $17$. However, this is inefficient for large exponents.

Instead, use the property that:
$(a \\times b) \\mod m = ((a \\mod m) \\times (b \\mod m)) \\mod m$

And implement the **binary exponentiation** algorithm for efficient computation.

## Mathematical Proof Requirement

You must include a mathematical proof explaining why your algorithm works correctly. Your proof should:

1. Explain the binary exponentiation algorithm
2. Prove its correctness using mathematical induction
3. Analyze its time complexity

## Input and Output

Your function should:
- Accept three integers: base $a$, exponent $b$, and modulus $m$
- Return $a^b \\mod m$

## Example

\`\`\`
Input: a = 3, b = 200, m = 17
Output: 11  (because 3^200 ≡ 11 (mod 17))
\`\`\`

Remember to include your mathematical reasoning in the Mathematical Reasoning tab.
          `,
          level: "foundation",
          domain: "number_theory",
          mathematical_requirements: [
            {
              concept: "Modular Arithmetic",
              description: "Understanding of modular arithmetic operations and properties",
              proof_required: true,
              complexity_analysis: false
            },
            {
              concept: "Binary Exponentiation",
              description: "Algorithm for efficient computation of large powers",
              proof_required: true,
              complexity_analysis: true
            }
          ],
          time_limit: 300.0,
          example_test_cases: 5,
          code_template: `# Modular Exponentiation function
# Implement an efficient algorithm for computing (a^b) % m

def mod_exp(a, b, m):
    """
    Compute (a^b) % m efficiently
    
    Args:
        a: base (integer)
        b: exponent (integer)
        c: modulus (integer)
    
    Returns:
        The result of a^b % m
    """
    # Your implementation here
    pass

# Test your function
if __name__ == "__main__":
    # Example test: 3^200 % 17
    result = mod_exp(3, 200, 17)
    print(f"3^200 % 17 = {result}")  # Should output 11
`,
          reasoning_template: `# Mathematical Reasoning

## Modular Exponentiation and Binary Exponentiation Algorithm

In this solution, I'm implementing the binary exponentiation algorithm to efficiently compute a^b mod m.

### Property of Modular Arithmetic

First, let me establish the key property of modular arithmetic that makes this possible:

(a × b) mod m = ((a mod m) × (b mod m)) mod m

### Binary Exponentiation Algorithm

The binary exponentiation algorithm works by:

1. Converting the exponent to binary
2. Computing powers of the base that correspond to each bit position
3. Multiplying together only the powers where bits are set to 1

### Proof of Correctness

[Add your proof here, using mathematical induction]

### Time Complexity Analysis

[Add your analysis here, showing logarithmic time complexity O(log b)]

### Example Trace

For computing 3^200 mod 17:

[Add a trace of your algorithm's execution here]

`
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchChallenge();
  }, [id]);
  
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  // Handle code change
  const handleCodeChange = useCallback((value) => {
    setCode(value);
  }, []);
  
  // Handle mathematical reasoning change
  const handleMathReasoningChange = useCallback((value) => {
    setMathReasoning(value);
  }, []);
  
  // Handle run code (would be implemented with actual backend integration)
  const handleRunCode = async () => {
    // This would be connected to a backend service for sandboxed execution
    console.log('Running code...');
    alert('Code execution is simulated in this demo. In production, this would run your code in a sandbox environment.');
  };
  
  // Handle submission
  const handleSubmit = async () => {
    setSubmitting(true);
    
    try {
      // Submit to backend
      // const response = await axios.post('/api/submissions', {
      //   challenge_id: challenge.id,
      //   code: code,
      //   mathematical_reasoning: mathReasoning
      // });
      
      // Simulate API response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Sample feedback
      const sampleFeedback = {
        passed: Math.random() > 0.5,
        total_score: 0.78,
        feedback: {
          detailed_score: {
            criteria_scores: {
              functional_correctness: 0.9,
              mathematical_rigor: 0.75,
              code_quality: 0.85,
              innovation: 0.6
            },
            strengths: [
              "Efficient implementation of binary exponentiation",
              "Good mathematical explanation of modular properties",
              "Well-structured code with clear comments"
            ],
            improvement_areas: [
              "Proof by induction could be more rigorous",
              "Consider edge cases (e.g., negative exponents)",
              "Time complexity analysis could be more detailed"
            ],
            feedback: "Your solution implements binary exponentiation correctly and has good mathematical reasoning. The proof could be strengthened by a more formal induction step. Overall, excellent work!"
          },
          validation_result: {
            overall_score: 0.78,
            scores: {
              mathematical_rigor: 0.75,
              proof_correctness: 0.7,
              code_elegance: 0.85,
              concept_mastery: 0.8
            },
            concepts_identified: [
              {
                concept: "modular_arithmetic",
                confidence: 0.95,
                evidence: "Proper use of modular properties in code and explanation",
                mastery_level: 0.85
              },
              {
                concept: "binary_exponentiation",
                confidence: 0.9,
                evidence: "Correctly implemented efficient algorithm with O(log n) complexity",
                mastery_level: 0.8
              },
              {
                concept: "mathematical_induction",
                confidence: 0.7,
                evidence: "Attempted proof by induction, but missing some formality",
                mastery_level: 0.6
              }
            ],
            proof_analysis: {
              steps_found: 3,
              valid_steps: 2,
              proof_steps: [
                {
                  statement: "Base case: When b = 0, a^0 = 1 for any a ≠ 0",
                  justification: "Mathematical identity",
                  is_valid: true,
                  confidence: 0.95
                },
                {
                  statement: "For the inductive step, assume a^k mod m is correctly computed",
                  justification: "Induction hypothesis",
                  is_valid: true,
                  confidence: 0.9
                },
                {
                  statement: "Therefore the algorithm is correct for all exponents",
                  justification: "By induction",
                  is_valid: false,
                  confidence: 0.5
                }
              ]
            },
            code_analysis: {
              complexity: "O(log n)",
              efficiency_score: 0.9,
              readability_score: 0.85,
              patterns_identified: ["Divide and conquer", "Bit manipulation", "Power by squaring"]
            },
            feedback: "Your solution shows good understanding of modular arithmetic and binary exponentiation. The proof needs more rigor in the inductive step. Code implementation is efficient and well-structured.",
            suggestions: [
              "Strengthen your induction proof by explicitly showing how a^(k+1) relates to a^k",
              "Add handling for negative exponents to make your solution more complete",
              "Consider adding a brief explanation of time-space tradeoffs in your approach"
            ]
          }
        }
      };
      
      setFeedback(sampleFeedback);
      setShowFeedback(true);
      
    } catch (error) {
      console.error('Error submitting solution:', error);
      alert('An error occurred while submitting your solution. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };
  
  // Toggle requirements drawer
  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ height: 'calc(100vh - 136px)' }}>
      {/* Top Bar */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton onClick={() => navigate('/challenges')} sx={{ mr: 1 }}>
            <BackIcon />
          </IconButton>
          <Typography variant="h5" component="h1">
            {challenge.title}
          </Typography>
        </Box>
        
        <Box>
          <Chip
            label={challenge.domain.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            color="primary"
            sx={{ mr: 1 }}
          />
          <Chip
            label={challenge.level.charAt(0).toUpperCase() + challenge.level.slice(1)}
            variant="outlined"
          />
          <Tooltip title="View Mathematical Requirements">
            <IconButton onClick={toggleDrawer} color="primary" sx={{ ml: 1 }}>
              <InfoIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      {/* Main Content */}
      <Grid container spacing={2} sx={{ height: 'calc(100% - 48px)' }}>
        {/* Left Panel - Challenge Description */}
        <Grid item xs={12} md={6} sx={{ height: '100%' }}>
          <Paper sx={{ p: 2, height: '100%', overflow: 'auto' }}>
            <Box sx={{ height: '100%', overflow: 'auto' }}>
              <MarkdownWithMath>
                {challenge.description}
              </MarkdownWithMath>
            </Box>
          </Paper>
        </Grid>
        
        {/* Right Panel - Code Editor and Mathematical Reasoning */}
        <Grid item xs={12} md={6} sx={{ height: '100%' }}>
          <Paper sx={{ height: '100%', overflow: 'hidden' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                aria-label="challenge tabs"
                variant="fullWidth"
              >
                <Tab 
                  icon={<CodeIcon fontSize="small" />} 
                  label="Code" 
                  id="challenge-tab-0" 
                  aria-controls="challenge-tabpanel-0" 
                />
                <Tab 
                  icon={<MathIcon fontSize="small" />} 
                  label="Mathematical Reasoning" 
                  id="challenge-tab-1" 
                  aria-controls="challenge-tabpanel-1" 
                />
                <Tab 
                  icon={<ResultsIcon fontSize="small" />} 
                  label="Results" 
                  id="challenge-tab-2" 
                  aria-controls="challenge-tabpanel-2" 
                  disabled={!feedback}
                />
              </Tabs>
            </Box>
            
            <Box sx={{ height: 'calc(100% - 48px)' }}>
              {/* Code Editor Tab */}
              <TabPanel value={tabValue} index={0}>
                <Box sx={{ height: 'calc(100% - 64px)', borderRadius: 1, overflow: 'hidden' }}>
                  <CodeMirror
                    value={code}
                    height="100%"
                    extensions={[python()]}
                    onChange={handleCodeChange}
                    theme="light"
                  />
                </Box>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    startIcon={<RunIcon />}
                    onClick={handleRunCode}
                    sx={{ mr: 1 }}
                  >
                    Run
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<SaveIcon />}
                    sx={{ mr: 1 }}
                  >
                    Save
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<SendIcon />}
                    onClick={handleSubmit}
                    disabled={submitting}
                  >
                    {submitting ? 'Submitting...' : 'Submit'}
                  </Button>
                </Box>
              </TabPanel>
              
              {/* Mathematical Reasoning Tab */}
              <TabPanel value={tabValue} index={1}>
                <Box sx={{ height: 'calc(100% - 64px)', borderRadius: 1, overflow: 'hidden' }}>
                  <CodeMirror
                    value={mathReasoning}
                    height="100%"
                    onChange={handleMathReasoningChange}
                    theme="light"
                  />
                </Box>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    startIcon={<SaveIcon />}
                    sx={{ mr: 1 }}
                  >
                    Save
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<SendIcon />}
                    onClick={handleSubmit}
                    disabled={submitting}
                  >
                    {submitting ? 'Submitting...' : 'Submit'}
                  </Button>
                </Box>
              </TabPanel>
              
              {/* Results Tab */}
              <TabPanel value={tabValue} index={2}>
                {feedback && (
                  <Box sx={{ height: '100%', overflow: 'auto', px: 2 }}>
                    <Alert 
                      severity={feedback.passed ? "success" : "warning"} 
                      sx={{ mb: 3 }}
                    >
                      {feedback.passed 
                        ? "Congratulations! Your solution passed all tests." 
                        : "Your solution has some issues to address."}
                    </Alert>
                    
                    <Typography variant="h6" gutterBottom>
                      Overall Score: {Math.round(feedback.total_score * 100)}%
                    </Typography>
                    
                    <Grid container spacing={2} sx={{ mb: 3 }}>
                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            Strengths
                          </Typography>
                          <Divider sx={{ mb: 1 }} />
                          <ul style={{ paddingLeft: '20px', margin: 0 }}>
                            {feedback.feedback.detailed_score.strengths.map((item, index) => (
                              <li key={index}>
                                <Typography variant="body2">{item}</Typography>
                              </li>
                            ))}
                          </ul>
                        </Paper>
                      </Grid>
                      
                      <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            Areas for Improvement
                          </Typography>
                          <Divider sx={{ mb: 1 }} />
                          <ul style={{ paddingLeft: '20px', margin: 0 }}>
                            {feedback.feedback.detailed_score.improvement_areas.map((item, index) => (
                              <li key={index}>
                                <Typography variant="body2">{item}</Typography>
                              </li>
                            ))}
                          </ul>
                        </Paper>
                      </Grid>
                    </Grid>
                    
                    <Typography variant="h6" gutterBottom>
                      Mathematical Analysis
                    </Typography>
                    
                    <Paper sx={{ p: 2, mb: 3 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        Concepts Identified
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        {feedback.feedback.validation_result.concepts_identified.map((concept, index) => (
                          <Chip 
                            key={index} 
                            label={`${concept.concept.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} (${Math.round(concept.mastery_level * 100)}%)`}
                            color={concept.mastery_level > 0.7 ? "success" : concept.mastery_level > 0.4 ? "warning" : "error"}
                            variant="outlined" 
                          />
                        ))}
                      </Box>
                      
                      <Typography variant="subtitle1" gutterBottom>
                        Proof Analysis
                      </Typography>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          {feedback.feedback.validation_result.proof_steps_found} steps identified, 
                          {feedback.feedback.validation_result.valid_steps} valid
                        </Typography>
                        {feedback.feedback.validation_result.proof_steps.map((step, index) => (
                          <Paper 
                            key={index} 
                            elevation={0} 
                            sx={{ 
                              p: 1, 
                              my: 1, 
                              bgcolor: step.is_valid ? 'success.light' : 'error.light',
                              opacity: 0.8,
                              borderRadius: 1
                            }}
                          >
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                              {step.statement}
                            </Typography>
                            <Typography variant="caption">
                              Justification: {step.justification}
                            </Typography>
                          </Paper>
                        ))}
                      </Box>
                    </Paper>
                    
                    <Typography variant="h6" gutterBottom>
                      Detailed Feedback
                    </Typography>
                    <Paper sx={{ p: 2, mb: 3 }}>
                      <Typography variant="body1">
                        {feedback.feedback.validation_result.feedback}
                      </Typography>
                    </Paper>
                    
                    <Typography variant="h6" gutterBottom>
                      Suggestions for Improvement
                    </Typography>
                    <Paper sx={{ p: 2, mb: 3 }}>
                      <ul style={{ paddingLeft: '20px', margin: 0 }}>
                        {feedback.feedback.validation_result.suggestions.map((item, index) => (
                          <li key={index}>
                            <Typography variant="body2">{item}</Typography>
                          </li>
                        ))}
                      </ul>
                    </Paper>
                  </Box>
                )}
              </TabPanel>
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      {/* Mathematical Requirements Drawer */}
      <Drawer
        anchor="right"
        open={drawerOpen}
        onClose={toggleDrawer}
        sx={{ '& .MuiDrawer-paper': { width: { xs: '100%', sm: 400 } } }}
      >
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Mathematical Requirements
            </Typography>
            <IconButton edge="end" color="inherit" onClick={toggleDrawer} aria-label="close">
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        
        <Box sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Required Mathematical Concepts
          </Typography>
          
          {challenge.mathematical_requirements.map((requirement, index) => (
            <Paper key={index} sx={{ p: 2, mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                {requirement.concept}
              </Typography>
              <Typography variant="body2" gutterBottom>
                {requirement.description}
              </Typography>
              <Box sx={{ mt: 1 }}>
                {requirement.proof_required && (
                  <Chip 
                    icon={<ArticleIcon />} 
                    label="Proof Required" 
                    color="primary" 
                    size="small" 
                    sx={{ mr: 1, mb: 1 }} 
                  />
                )}
                {requirement.complexity_analysis && (
                  <Chip 
                    icon={<BugIcon />} 
                    label="Complexity Analysis" 
                    color="secondary" 
                    size="small"
                    sx={{ mb: 1 }} 
                  />
                )}
              </Box>
            </Paper>
          ))}
          
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Assessment Criteria
          </Typography>
          
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="body2" gutterBottom>
              Your solution will be evaluated on:
            </Typography>
            <ul style={{ paddingLeft: '20px', margin: 0 }}>
              <li>
                <Typography variant="body2">
                  <strong>Mathematical Rigor:</strong> Accuracy and completeness of mathematical reasoning
                </Typography>
              </li>
              <li>
                <Typography variant="body2">
                  <strong>Proof Correctness:</strong> Validity of mathematical proofs
                </Typography>
              </li>
              <li>
                <Typography variant="body2">
                  <strong>Code Elegance:</strong> Efficiency, readability, and structure
                </Typography>
              </li>
              <li>
                <Typography variant="body2">
                  <strong>Concept Mastery:</strong> Understanding of required mathematical concepts
                </Typography>
              </li>
            </ul>
          </Paper>
          
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <Button
              variant="outlined"
              startIcon={<HelpIcon />}
              onClick={() => window.open('/help/mathematical-requirements', '_blank')}
            >
              Learn More About Requirements
            </Button>
          </Box>
        </Box>
      </Drawer>
      
      {/* Feedback Dialog - Shown when submission completes */}
      <Dialog 
        open={showFeedback} 
        onClose={() => setShowFeedback(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Submission Result
          <IconButton
            aria-label="close"
            onClick={() => setShowFeedback(false)}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
            }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {feedback && (
            <>
              <Alert 
                severity={feedback.passed ? "success" : "warning"} 
                sx={{ mb: 3 }}
              >
                {feedback.passed 
                  ? "Congratulations! Your solution passed all tests." 
                  : "Your solution has some issues to address."}
              </Alert>
              
              <Typography variant="h6" gutterBottom>
                Overall Score: {Math.round(feedback.total_score * 100)}%
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle1">Criteria Scores:</Typography>
                    {Object.entries(feedback.feedback.detailed_score.criteria_scores).map(([key, value]) => (
                      <Box key={key} sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <Typography variant="body2" sx={{ width: '50%' }}>
                          {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}:
                        </Typography>
                        <Box sx={{ width: '50%', display: 'flex', alignItems: 'center' }}>
                          <Box
                            sx={{
                              width: '100%',
                              bgcolor: 'background.paper',
                              borderRadius: 1,
                              mr: 1,
                              border: '1px solid',
                              borderColor: 'divider',
                            }}
                          >
                            <Box
                              sx={{
                                width: `${value * 100}%`,
                                bgcolor: value > 0.7 ? 'success.main' : value > 0.4 ? 'warning.main' : 'error.main',
                                height: 10,
                                borderRadius: 1,
                              }}
                            />
                          </Box>
                          <Typography variant="body2">
                            {Math.round(value * 100)}%
                          </Typography>
                        </Box>
                      </Box>
                    ))}
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Box>
                    <Typography variant="subtitle1" gutterBottom>
                      Strengths
                    </Typography>
                    <ul style={{ paddingLeft: '20px', margin: 0 }}>
                      {feedback.feedback.detailed_score.strengths.map((item, index) => (
                        <li key={index}>
                          <Typography variant="body2">{item}</Typography>
                        </li>
                      ))}
                    </ul>
                    
                    <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                      Areas for Improvement
                    </Typography>
                    <ul style={{ paddingLeft: '20px', margin: 0 }}>
                      {feedback.feedback.detailed_score.improvement_areas.map((item, index) => (
                        <li key={index}>
                          <Typography variant="body2">{item}</Typography>
                        </li>
                      ))}
                    </ul>
                  </Box>
                </Grid>
              </Grid>
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" gutterBottom>
                Detailed Feedback
              </Typography>
              <Typography variant="body1" paragraph>
                {feedback.feedback.detailed_score.feedback}
              </Typography>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button 
            startIcon={<TipIcon />}
            onClick={() => { setShowFeedback(false); setTabValue(2); }}
          >
            View Detailed Analysis
          </Button>
          <Button 
            variant="contained" 
            onClick={() => setShowFeedback(false)}
          >
            Continue
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ChallengeView;