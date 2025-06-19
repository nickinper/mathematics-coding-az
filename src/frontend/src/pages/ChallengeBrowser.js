import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardActions, 
  Button, 
  Chip,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  CircularProgress
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';

const ChallengeBrowser = () => {
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    // Simulate API call to fetch challenges
    const fetchChallenges = async () => {
      setLoading(true);
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data
      const mockChallenges = [
        {
          id: 'ch1',
          title: 'Prime Factorization Challenge',
          description: 'Implement an efficient algorithm to find the prime factorization of a number.',
          difficulty: 'intermediate',
          domain: 'number_theory',
          completion_rate: 0.68
        },
        {
          id: 'ch2',
          title: 'Matrix Eigenvalue Problem',
          description: 'Compute eigenvalues and eigenvectors of a given matrix using power iteration.',
          difficulty: 'advanced',
          domain: 'linear_algebra',
          completion_rate: 0.45
        },
        {
          id: 'ch3',
          title: 'Numerical Integration',
          description: 'Implement various numerical integration techniques and analyze their error bounds.',
          difficulty: 'intermediate',
          domain: 'calculus',
          completion_rate: 0.72
        },
        {
          id: 'ch4',
          title: 'Probability Distribution Sampler',
          description: 'Implement methods to sample from different probability distributions.',
          difficulty: 'intermediate',
          domain: 'probability',
          completion_rate: 0.59
        },
        {
          id: 'ch5',
          title: 'Graph Traversal Algorithms',
          description: 'Implement and compare different graph traversal algorithms.',
          difficulty: 'foundation',
          domain: 'graph_theory',
          completion_rate: 0.81
        },
        {
          id: 'ch6',
          title: 'Differential Equation Solver',
          description: 'Implement numerical methods to solve ordinary differential equations.',
          difficulty: 'advanced',
          domain: 'differential_equations',
          completion_rate: 0.38
        }
      ];
      
      setChallenges(mockChallenges);
      setTotalPages(Math.ceil(mockChallenges.length / 4));
      setLoading(false);
    };
    
    fetchChallenges();
  }, []);

  // Handle search input change
  const handleSearchChange = (event) => {
    setSearch(event.target.value);
    setPage(1);
  };

  // Handle filter change
  const handleFilterChange = (event) => {
    setFilter(event.target.value);
    setPage(1);
  };

  // Handle page change
  const handlePageChange = (event, value) => {
    setPage(value);
  };

  // Navigate to challenge view
  const handleChallengeClick = (id) => {
    navigate(`/challenges/${id}`);
  };

  // Filter and search challenges
  const filteredChallenges = challenges
    .filter(challenge => 
      challenge.title.toLowerCase().includes(search.toLowerCase()) ||
      challenge.description.toLowerCase().includes(search.toLowerCase())
    )
    .filter(challenge => 
      filter === 'all' || challenge.difficulty === filter
    );

  // Paginate challenges
  const paginatedChallenges = filteredChallenges.slice((page - 1) * 4, page * 4);

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Challenges
        </Typography>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          Explore mathematics-based coding challenges across various domains and difficulty levels.
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Search Challenges"
              value={search}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel id="difficulty-filter-label">Difficulty</InputLabel>
              <Select
                labelId="difficulty-filter-label"
                value={filter}
                label="Difficulty"
                onChange={handleFilterChange}
              >
                <MenuItem value="all">All Levels</MenuItem>
                <MenuItem value="foundation">Foundation</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="advanced">Advanced</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Grid container spacing={3}>
              {paginatedChallenges.map(challenge => (
                <Grid item xs={12} sm={6} key={challenge.id}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" component="h2" gutterBottom>
                        {challenge.title}
                      </Typography>
                      
                      <Box sx={{ mb: 2 }}>
                        <Chip 
                          label={challenge.domain.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} 
                          size="small" 
                          color="primary" 
                          sx={{ mr: 1, mb: 1 }} 
                        />
                        <Chip 
                          label={challenge.difficulty.charAt(0).toUpperCase() + challenge.difficulty.slice(1)} 
                          size="small" 
                          color={
                            challenge.difficulty === 'foundation' ? 'success' :
                            challenge.difficulty === 'intermediate' ? 'warning' : 'error'
                          }
                          sx={{ mb: 1 }} 
                        />
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {challenge.description}
                      </Typography>
                      
                      <Typography variant="body2" color="text.secondary">
                        Completion Rate: {Math.round(challenge.completion_rate * 100)}%
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" onClick={() => handleChallengeClick(challenge.id)}>
                        View Challenge
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
            
            {filteredChallenges.length === 0 && (
              <Box sx={{ textAlign: 'center', my: 4 }}>
                <Typography variant="body1" color="text.secondary">
                  No challenges found matching your criteria.
                </Typography>
              </Box>
            )}
            
            {filteredChallenges.length > 0 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Pagination 
                  count={Math.ceil(filteredChallenges.length / 4)} 
                  page={page} 
                  onChange={handlePageChange} 
                  color="primary" 
                />
              </Box>
            )}
          </>
        )}
      </Box>
    </Container>
  );
};

export default ChallengeBrowser;