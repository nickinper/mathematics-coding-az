import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Tabs,
  Tab,
  Divider,
  CircularProgress,
  Alert,
  Snackbar,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import CodeIcon from '@mui/icons-material/Code';
import BugReportIcon from '@mui/icons-material/BugReport';
import SecurityIcon from '@mui/icons-material/Security';
import BarChartIcon from '@mui/icons-material/BarChart';
import CodeEditor from '../components/CodeEditor';
import TestResultsDisplay from '../components/TestResultsDisplay';
import FeedbackVisualizer from '../components/FeedbackVisualizer';
import ExecutionService from '../services/ExecutionService';
import { useTheme } from '@mui/material/styles';

// Default Python test case
const DEFAULT_TEST_CASES = [
  {
    input: { 'a': 2, 'b': 3 },
    expected_output: 5,
    function: 'add'
  },
  {
    input: { 'a': -1, 'b': 1 },
    expected_output: 0,
    function: 'add'
  }
];

// Default Python code
const DEFAULT_CODE = `# Example function that adds two numbers
def add(a, b):
    return a + b
`;

// Default Python unsafe code for testing security
const UNSAFE_CODE = `# This code attempts to use unsafe operations
import os

def dangerous_function():
    return os.system("echo 'This is dangerous'")

def add(a, b):
    return a + b
`;

/**
 * Interactive code execution dashboard
 */
const Executor = () => {
  const theme = useTheme();
  const [activeTab, setActiveTab] = useState(0);
  const [code, setCode] = useState(DEFAULT_CODE);
  const [testCases, setTestCases] = useState(DEFAULT_TEST_CASES);
  const [executionResult, setExecutionResult] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [executionMetrics, setExecutionMetrics] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [isLoadingMetrics, setIsLoadingMetrics] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [language, setLanguage] = useState('python');
  const [testCaseInput, setTestCaseInput] = useState('');
  const [testCaseExpected, setTestCaseExpected] = useState('');
  const [testCaseFunction, setTestCaseFunction] = useState('add');

  // Load execution metrics on component mount
  useEffect(() => {
    loadExecutionMetrics();
  }, []);

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    
    // Reset the code based on tab
    if (newValue === 2) { // Security tab
      setCode(UNSAFE_CODE);
    } else if (code === UNSAFE_CODE) {
      setCode(DEFAULT_CODE);
    }
  };

  // Execute code
  const handleExecuteCode = async () => {
    setIsExecuting(true);
    setExecutionResult(null);
    
    try {
      const result = await ExecutionService.executeCode(code, testCases, language);
      setExecutionResult(result);
      
      // Show success/error message
      if (result.status === 'success') {
        const passRate = result.test_results.passed / result.test_results.total;
        if (passRate === 1) {
          showSnackbar('All tests passed successfully!', 'success');
        } else {
          showSnackbar(`${result.test_results.passed}/${result.test_results.total} tests passed`, 'warning');
        }
      } else {
        showSnackbar(`Execution failed: ${result.status}`, 'error');
      }
      
    } catch (error) {
      showSnackbar(`Error: ${error.message}`, 'error');
    } finally {
      setIsExecuting(false);
    }
  };

  // Validate code for security issues
  const handleValidateCode = async () => {
    setIsValidating(true);
    setValidationResult(null);
    
    try {
      const result = await ExecutionService.validateCode(code, testCases, language);
      setValidationResult(result);
      
      if (result.is_valid) {
        showSnackbar('Code passed security validation', 'success');
      } else {
        showSnackbar(`Security validation failed: ${result.message}`, 'error');
      }
      
    } catch (error) {
      showSnackbar(`Error: ${error.message}`, 'error');
    } finally {
      setIsValidating(false);
    }
  };

  // Load execution metrics
  const loadExecutionMetrics = async () => {
    setIsLoadingMetrics(true);
    
    try {
      const metrics = await ExecutionService.getMetrics();
      setExecutionMetrics(metrics);
    } catch (error) {
      showSnackbar(`Error loading metrics: ${error.message}`, 'error');
    } finally {
      setIsLoadingMetrics(false);
    }
  };

  // Add a new test case
  const handleAddTestCase = () => {
    try {
      // Parse the input and expected values
      const parsedInput = testCaseInput.trim() ? JSON.parse(testCaseInput) : {};
      const parsedExpected = testCaseExpected.trim() ? JSON.parse(testCaseExpected) : null;
      
      const newTestCase = {
        input: parsedInput,
        expected_output: parsedExpected,
        function: testCaseFunction.trim() || 'add'
      };
      
      setTestCases([...testCases, newTestCase]);
      
      // Clear inputs
      setTestCaseInput('');
      setTestCaseExpected('');
      
      showSnackbar('Test case added', 'success');
    } catch (error) {
      showSnackbar(`Error adding test case: ${error.message}`, 'error');
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
        <Typography variant="h4" component="h1" gutterBottom>
          <CodeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Code Execution Engine
        </Typography>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          This interactive dashboard allows you to execute code in a secure sandbox environment,
          test it against custom test cases, validate it for security issues, and view detailed execution metrics.
        </Typography>
        
        <Paper sx={{ mb: 4 }}>
          <Tabs 
            value={activeTab} 
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab icon={<PlayArrowIcon />} label="Execute" />
            <Tab icon={<BugReportIcon />} label="Test" />
            <Tab icon={<SecurityIcon />} label="Security" />
            <Tab icon={<BarChartIcon />} label="Metrics" />
          </Tabs>
          
          <Divider />
          
          <Box sx={{ p: 3 }}>
            {/* Execute Tab */}
            {activeTab === 0 && (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Code Editor
                  </Typography>
                  <FormControl sx={{ mb: 2, minWidth: 200 }}>
                    <InputLabel id="language-select-label">Language</InputLabel>
                    <Select
                      labelId="language-select-label"
                      value={language}
                      label="Language"
                      onChange={(e) => setLanguage(e.target.value)}
                    >
                      <MenuItem value="python">Python</MenuItem>
                      <MenuItem value="javascript">JavaScript (Coming Soon)</MenuItem>
                    </Select>
                  </FormControl>
                  <CodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={setCode}
                    onExecute={handleExecuteCode}
                    height="300px"
                    showExecuteButton={false}
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={isExecuting ? <CircularProgress size={20} color="inherit" /> : <PlayArrowIcon />}
                    onClick={handleExecuteCode}
                    disabled={isExecuting}
                    sx={{ mb: 2 }}
                  >
                    {isExecuting ? 'Executing...' : 'Execute Code'}
                  </Button>
                  
                  {executionResult && executionResult.test_results && (
                    <TestResultsDisplay results={executionResult.test_results} />
                  )}
                </Grid>
              </Grid>
            )}
            
            {/* Test Tab */}
            {activeTab === 1 && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Code Editor
                  </Typography>
                  <CodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={setCode}
                    height="300px"
                    showExecuteButton={false}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={isExecuting ? <CircularProgress size={20} color="inherit" /> : <PlayArrowIcon />}
                    onClick={handleExecuteCode}
                    disabled={isExecuting}
                    sx={{ mt: 2 }}
                  >
                    {isExecuting ? 'Running Tests...' : 'Run Tests'}
                  </Button>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Test Cases
                  </Typography>
                  <Paper sx={{ p: 2, mb: 2, bgcolor: theme.palette.background.default }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Add New Test Case
                    </Typography>
                    <TextField
                      label="Function Name"
                      value={testCaseFunction}
                      onChange={(e) => setTestCaseFunction(e.target.value)}
                      fullWidth
                      margin="dense"
                      size="small"
                      placeholder="add"
                    />
                    <TextField
                      label="Input (JSON)"
                      value={testCaseInput}
                      onChange={(e) => setTestCaseInput(e.target.value)}
                      fullWidth
                      margin="dense"
                      size="small"
                      placeholder='{"a": 1, "b": 2}'
                    />
                    <TextField
                      label="Expected Output (JSON)"
                      value={testCaseExpected}
                      onChange={(e) => setTestCaseExpected(e.target.value)}
                      fullWidth
                      margin="dense"
                      size="small"
                      placeholder="3"
                    />
                    <Button 
                      variant="outlined" 
                      onClick={handleAddTestCase}
                      sx={{ mt: 1 }}
                    >
                      Add Test Case
                    </Button>
                  </Paper>
                  
                  <Typography variant="subtitle2" gutterBottom>
                    Current Test Cases ({testCases.length})
                  </Typography>
                  {testCases.map((testCase, index) => (
                    <Paper key={index} sx={{ p: 2, mb: 1, bgcolor: theme.palette.background.default }}>
                      <Typography variant="body2">
                        <strong>Function:</strong> {testCase.function}
                      </Typography>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        <strong>Input:</strong> {JSON.stringify(testCase.input)}
                      </Typography>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                        <strong>Expected:</strong> {JSON.stringify(testCase.expected_output)}
                      </Typography>
                    </Paper>
                  ))}
                </Grid>
                
                {executionResult && executionResult.test_results && (
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                      Test Results
                    </Typography>
                    <TestResultsDisplay results={executionResult.test_results} />
                  </Grid>
                )}
              </Grid>
            )}
            
            {/* Security Tab */}
            {activeTab === 2 && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Code Editor (Try unsafe code)
                  </Typography>
                  <CodeEditor
                    initialCode={code}
                    language={language}
                    onCodeChange={setCode}
                    height="300px"
                    showExecuteButton={false}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={isValidating ? <CircularProgress size={20} color="inherit" /> : <SecurityIcon />}
                    onClick={handleValidateCode}
                    disabled={isValidating}
                    sx={{ mt: 2 }}
                  >
                    {isValidating ? 'Validating...' : 'Validate Security'}
                  </Button>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Security Validation
                  </Typography>
                  
                  {validationResult ? (
                    <Paper sx={{ p: 2, bgcolor: theme.palette.background.default }}>
                      <Alert 
                        severity={validationResult.is_valid ? "success" : "error"}
                        sx={{ mb: 2 }}
                      >
                        {validationResult.is_valid 
                          ? "Code passed security validation"
                          : `Security validation failed: ${validationResult.message}`
                        }
                      </Alert>
                      
                      <Typography variant="subtitle2" gutterBottom>
                        Security Rules
                      </Typography>
                      <ul>
                        <li>
                          <Typography variant="body2">
                            No system access (os, sys, subprocess)
                          </Typography>
                        </li>
                        <li>
                          <Typography variant="body2">
                            No network access (socket, requests, urllib)
                          </Typography>
                        </li>
                        <li>
                          <Typography variant="body2">
                            No dangerous builtins (eval, exec, compile)
                          </Typography>
                        </li>
                        <li>
                          <Typography variant="body2">
                            No file operations (open, __file__, etc.)
                          </Typography>
                        </li>
                      </ul>
                      
                      {validationResult.is_valid && validationResult.test_results && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="subtitle2" gutterBottom>
                            Execution Results
                          </Typography>
                          <TestResultsDisplay results={validationResult.test_results} />
                        </Box>
                      )}
                    </Paper>
                  ) : (
                    <Paper sx={{ p: 2, bgcolor: theme.palette.background.default }}>
                      <Typography variant="body2">
                        Click "Validate Security" to check the code for security issues.
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        The code is analyzed for potentially dangerous operations
                        before execution in the sandbox environment.
                      </Typography>
                    </Paper>
                  )}
                </Grid>
              </Grid>
            )}
            
            {/* Metrics Tab */}
            {activeTab === 3 && (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      Execution Metrics
                    </Typography>
                    <Button
                      variant="outlined"
                      onClick={loadExecutionMetrics}
                      disabled={isLoadingMetrics}
                      startIcon={isLoadingMetrics ? <CircularProgress size={20} /> : null}
                    >
                      {isLoadingMetrics ? 'Loading...' : 'Refresh'}
                    </Button>
                  </Box>
                  
                  {isLoadingMetrics ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                      <CircularProgress />
                    </Box>
                  ) : executionMetrics ? (
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={6} lg={3}>
                        <Paper sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                          <Typography variant="h3" color="primary.main">
                            {executionMetrics.total_executions}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Total Executions
                          </Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={12} md={6} lg={3}>
                        <Paper sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                          <Typography variant="h3" color="success.main">
                            {executionMetrics.successful_executions}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Successful Executions
                          </Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={12} md={6} lg={3}>
                        <Paper sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                          <Typography variant="h3" color="error.main">
                            {executionMetrics.failed_executions}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Failed Executions
                          </Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={12} md={6} lg={3}>
                        <Paper sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                          <Typography variant="h3" color="info.main">
                            {executionMetrics.average_execution_time.toFixed(2)}s
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Average Execution Time
                          </Typography>
                        </Paper>
                      </Grid>
                      
                      <Grid item xs={12}>
                        <Paper sx={{ p: 2, mt: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            Executions by Hour
                          </Typography>
                          <Box sx={{ height: 200, bgcolor: theme.palette.background.default, p: 2 }}>
                            {/* In a real app, you would render a chart here */}
                            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
                              Chart visualization would be displayed here
                            </Typography>
                          </Box>
                        </Paper>
                      </Grid>
                    </Grid>
                  ) : (
                    <Alert severity="info">
                      No metrics data available
                    </Alert>
                  )}
                </Grid>
              </Grid>
            )}
          </Box>
        </Paper>
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

export default Executor;