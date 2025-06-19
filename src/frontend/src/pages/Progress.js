import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Tab,
  Tabs,
  Card,
  CardContent,
  Chip,
  Button
} from '@mui/material';
import BarChartIcon from '@mui/icons-material/BarChart';
import TimelineIcon from '@mui/icons-material/Timeline';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import SchoolIcon from '@mui/icons-material/School';
import FunctionsIcon from '@mui/icons-material/Functions';
import { useTheme } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

const Progress = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(0);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch progress data
    const fetchProgressData = async () => {
      setLoading(true);
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock progress data
      const mockProgress = {
        overall_completion: 0.38,
        challenges_completed: 27,
        total_challenges: 72,
        mathematical_domains: [
          { name: 'Number Theory', completed: 8, total: 15, score: 0.85 },
          { name: 'Linear Algebra', completed: 5, total: 12, score: 0.76 },
          { name: 'Calculus', completed: 6, total: 14, score: 0.92 },
          { name: 'Probability', completed: 4, total: 12, score: 0.71 },
          { name: 'Graph Theory', completed: 4, total: 9, score: 0.88 },
          { name: 'Differential Equations', completed: 0, total: 10, score: 0 }
        ],
        skill_levels: [
          { name: 'Mathematical Modeling', level: 0.82 },
          { name: 'Algorithmic Thinking', level: 0.91 },
          { name: 'Proof Writing', level: 0.68 },
          { name: 'Code Optimization', level: 0.76 },
          { name: 'Problem Decomposition', level: 0.88 }
        ],
        recent_achievements: [
          { 
            title: 'Linear Algebra Master',
            description: 'Completed 5 linear algebra challenges with an average score of 75%+',
            date: '2025-06-10',
            icon: 'school'
          },
          { 
            title: 'Consistency Streak',
            description: 'Completed at least one challenge every day for a week',
            date: '2025-06-05',
            icon: 'timeline'
          },
          { 
            title: 'Perfect Solution',
            description: 'Achieved 100% score on "Prime Factorization Challenge"',
            date: '2025-05-28',
            icon: 'functions'
          }
        ],
        learning_path_progress: [
          { 
            path_name: 'Algorithms Fundamentals',
            completed_steps: 8,
            total_steps: 12,
            next_challenge: 'Dynamic Programming Basics'
          },
          { 
            path_name: 'Computational Mathematics',
            completed_steps: 5,
            total_steps: 15,
            next_challenge: 'Numerical Integration Methods'
          }
        ],
        recommended_challenges: [
          {
            id: 'rec1',
            title: 'Eigenvalue Computation',
            domain: 'linear_algebra',
            difficulty: 'intermediate',
            reason: 'Based on your Linear Algebra progress'
          },
          {
            id: 'rec2',
            title: 'Probabilistic Algorithms',
            domain: 'probability',
            difficulty: 'advanced',
            reason: 'To improve your probability skills'
          },
          {
            id: 'rec3',
            title: 'Differential Equation Basics',
            domain: 'differential_equations',
            difficulty: 'foundation',
            reason: 'New domain to explore'
          }
        ]
      };
      
      setProgress(mockProgress);
      setLoading(false);
    };
    
    fetchProgressData();
  }, []);

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
          <LinearProgress sx={{ width: '100%' }} />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Progress
        </Typography>
        
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab icon={<BarChartIcon />} label="Overview" />
            <Tab icon={<TimelineIcon />} label="Learning Paths" />
            <Tab icon={<EmojiEventsIcon />} label="Achievements" />
          </Tabs>
          
          <Divider />
          
          {/* Overview Tab */}
          {activeTab === 0 && (
            <Box sx={{ p: 3 }}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Overall Progress
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ flexGrow: 1, mr: 2 }}>
                      <LinearProgress
                        variant="determinate"
                        value={progress.overall_completion * 100}
                        sx={{ height: 12, borderRadius: 6 }}
                      />
                    </Box>
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                      {Math.round(progress.overall_completion * 100)}%
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {progress.challenges_completed} out of {progress.total_challenges} challenges completed
                  </Typography>
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Progress by Domain
                  </Typography>
                  <Grid container spacing={2}>
                    {progress.mathematical_domains.map((domain, index) => (
                      <Grid item xs={12} sm={6} key={index}>
                        <Paper variant="outlined" sx={{ p: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            {domain.name}
                          </Typography>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="body2" color="text.secondary">
                              {domain.completed} / {domain.total} challenges
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Avg. Score: {Math.round(domain.score * 100)}%
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Box sx={{ flexGrow: 1, mr: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={(domain.completed / domain.total) * 100}
                                sx={{ 
                                  height: 8, 
                                  borderRadius: 4,
                                  '& .MuiLinearProgress-bar': {
                                    backgroundColor: domain.score > 0.8 ? theme.palette.success.main : 
                                                    domain.score > 0.6 ? theme.palette.info.main : 
                                                    theme.palette.warning.main
                                  }
                                }}
                              />
                            </Box>
                            <Typography variant="body2">
                              {Math.round((domain.completed / domain.total) * 100)}%
                            </Typography>
                          </Box>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Skill Levels
                  </Typography>
                  {progress.skill_levels.map((skill, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">{skill.name}</Typography>
                        <Typography variant="body2">{Math.round(skill.level * 100)}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={skill.level * 100}
                        sx={{ 
                          height: 8, 
                          borderRadius: 4,
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: skill.level > 0.8 ? theme.palette.success.main : 
                                          skill.level > 0.6 ? theme.palette.info.main : 
                                          theme.palette.warning.main
                          }
                        }}
                      />
                    </Box>
                  ))}
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Recommended Challenges
                  </Typography>
                  <List>
                    {progress.recommended_challenges.map((challenge, index) => (
                      <Paper 
                        key={index} 
                        variant="outlined" 
                        sx={{ mb: 2, p: 2 }}
                      >
                        <Typography variant="subtitle1" gutterBottom>
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
                            label={challenge.difficulty.charAt(0).toUpperCase() + challenge.difficulty.slice(1)} 
                            size="small"
                            color={
                              challenge.difficulty === 'foundation' ? 'success' :
                              challenge.difficulty === 'intermediate' ? 'warning' : 'error'
                            }
                            variant="outlined"
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {challenge.reason}
                        </Typography>
                        <Button 
                          variant="outlined" 
                          size="small"
                          onClick={() => navigate(`/challenges/${challenge.id}`)}
                        >
                          Start Challenge
                        </Button>
                      </Paper>
                    ))}
                  </List>
                </Grid>
              </Grid>
            </Box>
          )}
          
          {/* Learning Paths Tab */}
          {activeTab === 1 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Your Learning Paths
              </Typography>
              
              {progress.learning_path_progress.map((path, index) => (
                <Paper key={index} variant="outlined" sx={{ p: 2, mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    {path.path_name}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Progress: {path.completed_steps} / {path.total_steps} steps
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {Math.round((path.completed_steps / path.total_steps) * 100)}% Complete
                    </Typography>
                  </Box>
                  
                  <LinearProgress
                    variant="determinate"
                    value={(path.completed_steps / path.total_steps) * 100}
                    sx={{ height: 8, borderRadius: 4, mb: 2 }}
                  />
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="subtitle2">
                        Next Challenge:
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {path.next_challenge}
                      </Typography>
                    </Box>
                    
                    <Button variant="contained" color="primary" size="small">
                      Continue Path
                    </Button>
                  </Box>
                </Paper>
              ))}
              
              <Box sx={{ textAlign: 'center', mt: 4 }}>
                <Button variant="outlined" color="primary">
                  Explore More Learning Paths
                </Button>
              </Box>
            </Box>
          )}
          
          {/* Achievements Tab */}
          {activeTab === 2 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recent Achievements
              </Typography>
              
              <List>
                {progress.recent_achievements.map((achievement, index) => (
                  <ListItem key={index} alignItems="flex-start" sx={{ px: 0 }}>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: theme.palette.primary.main }}>
                        {achievement.icon === 'school' ? <SchoolIcon /> : 
                         achievement.icon === 'timeline' ? <TimelineIcon /> : <FunctionsIcon />}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={achievement.title}
                      secondary={
                        <>
                          <Typography component="span" variant="body2" color="text.primary">
                            {achievement.description}
                          </Typography>
                          {` — Achieved on ${new Date(achievement.date).toLocaleDateString()}`}
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" gutterBottom>
                Achievements to Pursue
              </Typography>
              
              <Grid container spacing={2}>
                {[
                  {
                    title: 'Calculus Master',
                    description: 'Complete all Calculus challenges with 80%+ average score',
                    progress: 0.67
                  },
                  {
                    title: 'Code Optimization Expert',
                    description: 'Optimize 5 solutions to achieve O(n) or better time complexity',
                    progress: 0.4
                  },
                  {
                    title: 'Mathematical Proof Virtuoso',
                    description: 'Write 10 perfect mathematical proofs',
                    progress: 0.3
                  }
                ].map((achievement, index) => (
                  <Grid item xs={12} md={4} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {achievement.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                          {achievement.description}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Box sx={{ flexGrow: 1, mr: 1 }}>
                            <LinearProgress
                              variant="determinate"
                              value={achievement.progress * 100}
                              sx={{ height: 6, borderRadius: 3 }}
                            />
                          </Box>
                          <Typography variant="body2">
                            {Math.round(achievement.progress * 100)}%
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  );
};

export default Progress;