import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Accordion, 
  AccordionSummary, 
  AccordionDetails,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

/**
 * Component to display test execution results
 */
const TestResultsDisplay = ({ results }) => {
  if (!results) return null;
  
  const { total, passed, failed, details = [] } = results;
  const passRate = total > 0 ? (passed / total) * 100 : 0;
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'passed': return 'success.main';
      case 'failed': return 'error.main';
      case 'error': return 'warning.main';
      default: return 'text.secondary';
    }
  };
  
  const getStatusIcon = (status) => {
    switch (status) {
      case 'passed': return <CheckCircleOutlineIcon fontSize="small" />;
      case 'failed': return <HighlightOffIcon fontSize="small" />;
      case 'error': return <ErrorOutlineIcon fontSize="small" />;
      default: return null;
    }
  };
  
  const formatValue = (value) => {
    if (value === undefined || value === null) return 'null';
    if (typeof value === 'object') return JSON.stringify(value, null, 2);
    return String(value);
  };
  
  return (
    <Paper elevation={2} sx={{ mb: 3, overflow: 'hidden', borderRadius: 1 }}>
      <Box sx={{ p: 2, backgroundColor: 'background.paper' }}>
        <Typography variant="h6" gutterBottom>
          Test Results
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ flexGrow: 1, mr: 2 }}>
            <LinearProgress 
              variant="determinate" 
              value={passRate} 
              color={passed === total ? "success" : "primary"}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Box>
          <Typography variant="body2" color="text.secondary">
            {passed}/{total} tests passed ({Math.round(passRate)}%)
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <Chip 
            icon={<CheckCircleOutlineIcon />} 
            label={`${passed} passed`} 
            color="success" 
            variant="outlined" 
            size="small"
          />
          <Chip 
            icon={<HighlightOffIcon />} 
            label={`${failed} failed`} 
            color="error" 
            variant="outlined" 
            size="small"
          />
        </Box>
        
        {details.length > 0 && (
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Test Details</Typography>
            </AccordionSummary>
            <AccordionDetails sx={{ p: 0 }}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Test</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Input</TableCell>
                      <TableCell>Expected</TableCell>
                      <TableCell>Actual</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {details.map((test, index) => (
                      <TableRow key={index} hover>
                        <TableCell>
                          {test.description || `Test ${test.test_id || index + 1}`}
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', color: getStatusColor(test.status) }}>
                            {getStatusIcon(test.status)}
                            <Typography variant="body2" sx={{ ml: 0.5 }}>
                              {test.status}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
                            {formatValue(test.input)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
                            {formatValue(test.expected_output)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
                            {formatValue(test.actual_output)}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>
        )}
        
        {results.error && (
          <Box sx={{ mt: 2, p: 2, backgroundColor: 'error.light', borderRadius: 1 }}>
            <Typography variant="subtitle2" color="error.contrastText">Error</Typography>
            <Typography 
              variant="body2" 
              color="error.contrastText" 
              sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}
            >
              {results.error}
            </Typography>
          </Box>
        )}
      </Box>
    </Paper>
  );
};

export default TestResultsDisplay;