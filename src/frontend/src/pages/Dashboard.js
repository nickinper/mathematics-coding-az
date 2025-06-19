import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  CircularProgress,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Paper,
  Chip
} from '@mui/material';
import { 
  PlayArrow as PlayIcon,
  School as SchoolIcon,
  EmojiEvents as TrophyIcon,
  BarChart as ProgressIcon,
  LocalFireDepartment as StreakIcon,
  Lightbulb as InsightIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import axios from 'axios';

// Import chart components
import { 
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

// Helper function to capitalize domain names
const capitalizeDomain = (domain) => {
  return domain
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [recentChallenges, setRecentChallenges] = useState([]);
  const [progressData, setProgressData] = useState(null);
  const [recommendedChallenges, setRecommendedChallenges] = useState([]);
  const [stats, setStats] = useState({
    completedChallenges: 0,
    currentStreak: 0,
    mathScore: 0,
    codingScore: 0
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch all required data in parallel
        const [
          challengesResponse, 
          progressResponse, 
          recommendationsResponse
        ] = await Promise.all([
          axios.get('/api/submissions?limit=5'),
          axios.get(`/api/users/${user?.id || 1}/progress`),
          axios.get('/api/challenges?recommended=true&limit=3')
        ]);
        
        setRecentChallenges(challengesResponse.data);
        setProgressData(progressResponse.data);
        setRecommendedChallenges(recommendationsResponse.data);
        
        // Set stats based on progress data
        setStats({
          completedChallenges: progressResponse.data.challenges_completed || 0,
          currentStreak: progressResponse.data.current_streak || 0,
          mathScore: user?.mathematics_score || 0.75,
          codingScore: user?.coding_score || 0.68
        });
        
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Use dummy data for demo purposes
        setRecentChallenges([
          {
            id: 1,
            challenge_id: 1,
            title: "RSA Cryptography",
            passed: true,
            total_score: 0.92,
            domain: "number_theory",
            submitted_at: "2025-06-18T14:30:00Z"
          },
          {
            id: 2,
            challenge_id: 2,
            title: "Matrix Transformations",
            passed: false,
            total_score: 0.45,
            domain: "linear_algebra",
            submitted_at: "2025-06-17T11:20:00Z"
          }
        ]);
        
        setProgressData({
          total_submissions: 8,
          challenges_attempted: 5,
          challenges_completed: 3,
          average_score: 0.78,
          mathematical_concepts_mastered: ["modular_arithmetic", "prime_theory"],
          areas_for_improvement: ["proof_writing", "complexity_analysis"],
          learning_velocity: {
            number_theory: 0.8,
            linear_algebra: 0.6,
            calculus: 0.3
          }
        });
        
        setRecommendedChallenges([
          {
            id: 3,
            title: "Neural Network from Scratch",
            description: "Implement a basic neural network using calculus principles",
            level: "intermediate",
            domain: "calculus",
            difficulty_score: 0.75
          },
          {
            id: 4,
            title: "The Traveling Salesman Problem",
            description: "Solve the classic TSP using graph theory",
            level: "intermediate",
            domain: "discrete_math",
            difficulty_score: 0.8
          }
        ]);
        
        setStats({
          completedChallenges: 3,
          currentStreak: 2,
          mathScore: 0.75,
          codingScore: 0.68
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [user]);

  // Chart data for learning progress
  const learningProgressData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
      {
        label: 'Mathematical Rigor',
        data: [0.3, 0.5, 0.6, 0.75],
        borderColor: 'rgba(101, 115, 195, 1)',
        backgroundColor: 'rgba(101, 115, 195, 0.2)',
        tension: 0.4
      },
      {
        label: 'Coding Quality',
        data: [0.5, 0.55, 0.62, 0.68],
        borderColor: 'rgba(126, 87, 194, 1)',
        backgroundColor: 'rgba(126, 87, 194, 0.2)',
        tension: 0.4
      }
    ]
  };

  // Chart data for domain mastery
  const domainMasteryData = {
    labels: Object.keys(progressData?.learning_velocity || {
      number_theory: 0.8,
      linear_algebra: 0.6,
      calculus: 0.3
    }).map(capitalizeDomain),
    datasets: [
      {
        data: Object.values(progressData?.learning_velocity || {
          number_theory: 0.8,
          linear_algebra: 0.6,
          calculus: 0.3
        }).map(value => value * 100),
        backgroundColor: [
          'rgba(101, 115, 195, 0.8)',
          'rgba(126, 87, 194, 0.8)',
          'rgba(94, 53, 177, 0.8)',
          'rgba(69, 39, 160, 0.8)',
          'rgba(49, 27, 146, 0.8)'
        ],
        borderWidth: 1
      }
    ]
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box className="fade-in">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome, {user?.full_name || user?.username || 'Student'}!
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Continue your journey in mathematical programming
        </Typography>
      </Box>
      
      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} md={4}>
          <Card className="dashboard-widget" sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', py: 3 }}>
              <SchoolIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h5" component="div">
                {stats.completedChallenges}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Completed Challenges
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card className="dashboard-widget" sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', py: 3 }}>
              <StreakIcon color="error" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h5" component="div">
                {stats.currentStreak} days
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Current Streak
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card className="dashboard-widget" sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', py: 3 }}>
              <TrophyIcon color="warning" sx={{ fontSize: 48, mb: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 3 }}>
                <Box>
                  <Typography variant="h5" component="div">
                    {Math.round(stats.mathScore * 100)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Math Score
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h5" component="div">
                    {Math.round(stats.codingScore * 100)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Coding Score
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Recent Challenges */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Recent Submissions
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {recentChallenges.length > 0 ? (
                <List sx={{ p: 0 }}>
                  {recentChallenges.map((submission) => (
                    <ListItem
                      key={submission.id}
                      alignItems="flex-start"
                      disablePadding
                      sx={{ mb: 2 }}
                      secondaryAction={
                        <Chip 
                          label={submission.passed ? 'Passed' : 'Failed'} 
                          color={submission.passed ? 'success' : 'error'}
                          size="small"
                        />
                      }
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: submission.passed ? 'success.main' : 'error.main' }}>
                          {submission.passed ? '✓' : '✗'}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={submission.title}
                        secondary={
                          <>
                            <Typography component="span" variant="body2" color="text.primary">
                              {capitalizeDomain(submission.domain)}
                            </Typography>
                            {` — Score: ${Math.round(submission.total_score * 100)}%`}
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                  No recent submissions. Start solving challenges!
                </Typography>
              )}
              
              <Button 
                variant="outlined" 
                fullWidth 
                onClick={() => navigate('/challenges')}
                sx={{ mt: 2 }}
              >
                View All Submissions
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Recommended Challenges */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Recommended Challenges
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {recommendedChallenges.length > 0 ? (
                <List sx={{ p: 0 }}>
                  {recommendedChallenges.map((challenge) => (
                    <Paper 
                      key={challenge.id} 
                      elevation={0} 
                      sx={{ 
                        p: 2, 
                        mb: 2, 
                        bgcolor: 'background.default',
                        borderRadius: 2
                      }}
                    >
                      <Typography variant="subtitle1" component="div" gutterBottom>
                        {challenge.title}
                      </Typography>
                      <Box sx={{ display: 'flex', mb: 1 }}>
                        <Chip 
                          label={capitalizeDomain(challenge.domain)} 
                          size="small" 
                          sx={{ mr: 1 }}
                        />
                        <Chip 
                          label={challenge.level.charAt(0).toUpperCase() + challenge.level.slice(1)} 
                          size="small" 
                          color="primary" 
                          variant="outlined"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        {challenge.description.length > 100 
                          ? challenge.description.substring(0, 100) + '...' 
                          : challenge.description}
                      </Typography>
                      <Button 
                        variant="contained" 
                        size="small" 
                        startIcon={<PlayIcon />}
                        onClick={() => navigate(`/challenges/${challenge.id}`)}
                      >
                        Start Challenge
                      </Button>
                    </Paper>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                  No recommendations available yet. Complete more challenges to get personalized recommendations.
                </Typography>
              )}
              
              <Button 
                variant="outlined" 
                fullWidth 
                onClick={() => navigate('/challenges')}
                sx={{ mt: 2 }}
              >
                Browse All Challenges
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Progress Chart */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Learning Progress
              </Typography>
              <Box sx={{ height: 300, p: 1 }}>
                <Line
                  data={learningProgressData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                          callback: (value) => `${value * 100}%`
                        }
                      }
                    },
                    plugins: {
                      legend: {
                        position: 'top',
                      },
                      tooltip: {
                        callbacks: {
                          label: (context) => `${context.dataset.label}: ${context.parsed.y * 100}%`
                        }
                      }
                    }
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Domain Mastery */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom>
                Domain Mastery
              </Typography>
              <Box sx={{ height: 300, display: 'flex', justifyContent: 'center' }}>
                <Doughnut
                  data={domainMasteryData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'right',
                      },
                      tooltip: {
                        callbacks: {
                          label: (context) => `${context.label}: ${context.parsed}%`
                        }
                      }
                    }
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Learning Insights */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <InsightIcon sx={{ mr: 1 }} color="primary" /> Learning Insights
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" gutterBottom>
                    Concepts Mastered
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {(progressData?.mathematical_concepts_mastered || []).map((concept, index) => (
                      <Chip 
                        key={index} 
                        label={capitalizeDomain(concept)} 
                        color="success" 
                        variant="outlined" 
                      />
                    ))}
                    {(progressData?.mathematical_concepts_mastered || []).length === 0 && (
                      <Typography variant="body2" color="text.secondary">
                        No concepts mastered yet. Keep practicing!
                      </Typography>
                    )}
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" gutterBottom>
                    Areas for Improvement
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {(progressData?.areas_for_improvement || []).map((area, index) => (
                      <Chip 
                        key={index} 
                        label={capitalizeDomain(area)} 
                        color="warning" 
                        variant="outlined" 
                      />
                    ))}
                    {(progressData?.areas_for_improvement || []).length === 0 && (
                      <Typography variant="body2" color="text.secondary">
                        No specific areas identified yet. Complete more challenges to get insights.
                      </Typography>
                    )}
                  </Box>
                </Grid>
              </Grid>
              
              <Button 
                variant="outlined" 
                fullWidth 
                startIcon={<ProgressIcon />}
                onClick={() => navigate('/progress')}
                sx={{ mt: 3 }}
              >
                View Detailed Progress
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;