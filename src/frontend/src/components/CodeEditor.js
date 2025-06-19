import React, { useState } from 'react';
import { Box, Typography, Button, CircularProgress, Paper } from '@mui/material';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import BugReportIcon from '@mui/icons-material/BugReport';

/**
 * Code editor component with execution capabilities
 */
const CodeEditor = ({
  initialCode = '# Your solution here\n\n',
  language = 'python',
  onExecute,
  readOnly = false,
  onCodeChange,
  height = '400px',
  showExecuteButton = true
}) => {
  const [code, setCode] = useState(initialCode);
  const [executing, setExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  
  // Handle code change
  const handleChange = (value) => {
    setCode(value);
    if (onCodeChange) {
      onCodeChange(value);
    }
  };
  
  // Handle code execution
  const handleExecute = async () => {
    setExecuting(true);
    setExecutionResult(null);
    
    try {
      if (onExecute) {
        const result = await onExecute(code);
        setExecutionResult(result);
      }
    } catch (error) {
      setExecutionResult({
        status: 'error',
        error: error.message
      });
    } finally {
      setExecuting(false);
    }
  };
  
  // Determine language extension
  const getLangExtension = () => {
    switch (language.toLowerCase()) {
      case 'javascript':
      case 'js':
        return javascript();
      case 'python':
      case 'py':
        return python();
      default:
        return python();
    }
  };
  
  return (
    <Box sx={{ width: '100%' }}>
      <Paper 
        elevation={3}
        sx={{
          borderRadius: 1,
          overflow: 'hidden',
          mb: 2
        }}
      >
        <CodeMirror
          value={code}
          height={height}
          extensions={[getLangExtension()]}
          onChange={handleChange}
          readOnly={readOnly}
          theme="dark"
          style={{ fontSize: '14px' }}
        />
      </Paper>
      
      {showExecuteButton && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={executing ? <CircularProgress size={20} color="inherit" /> : <PlayArrowIcon />}
            onClick={handleExecute}
            disabled={executing}
            sx={{ minWidth: '120px' }}
          >
            {executing ? 'Running...' : 'Run Code'}
          </Button>
          
          {executionResult && (
            <Typography 
              variant="body2" 
              color={
                executionResult.status === 'success' ? 'success.main' : 
                executionResult.status === 'error' ? 'error.main' : 
                'warning.main'
              }
              sx={{ 
                display: 'flex', 
                alignItems: 'center',
                fontWeight: 'medium'
              }}
            >
              {executionResult.status === 'success' ? (
                <>
                  <CheckCircleIcon fontSize="small" sx={{ mr: 0.5 }} />
                  {executionResult.test_results?.passed === executionResult.test_results?.total ? 
                    `All tests passed (${executionResult.test_results?.passed}/${executionResult.test_results?.total})` : 
                    `${executionResult.test_results?.passed}/${executionResult.test_results?.total} tests passed`}
                </>
              ) : executionResult.status === 'error' ? (
                <>
                  <ErrorIcon fontSize="small" sx={{ mr: 0.5 }} />
                  Execution error
                </>
              ) : (
                <>
                  <BugReportIcon fontSize="small" sx={{ mr: 0.5 }} />
                  {executionResult.status.replace('_', ' ')}
                </>
              )}
            </Typography>
          )}
        </Box>
      )}
      
      {executionResult && executionResult.error && (
        <Paper 
          elevation={1}
          sx={{ 
            p: 2, 
            mb: 2,
            backgroundColor: 'error.light',
            color: 'error.contrastText',
            borderRadius: 1,
            fontFamily: 'monospace',
            whiteSpace: 'pre-wrap',
            overflowX: 'auto'
          }}
        >
          {executionResult.error}
        </Paper>
      )}
      
      {executionResult && executionResult.output && executionResult.output.trim() !== '' && (
        <Paper 
          elevation={1}
          sx={{ 
            p: 2, 
            mb: 2,
            backgroundColor: 'background.paper',
            borderRadius: 1,
            fontFamily: 'monospace',
            whiteSpace: 'pre-wrap',
            overflowX: 'auto'
          }}
        >
          <Typography variant="body2" component="div" fontFamily="monospace">
            {executionResult.output}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default CodeEditor;