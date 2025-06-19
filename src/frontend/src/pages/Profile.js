import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Avatar,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  Chip,
  LinearProgress,
  TextField,
  Card,
  CardContent
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import { useAuth } from '../services/AuthContext';

const Profile = () => {
  const { user } = useAuth();
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    bio: '',
    education: '',
    interests: ''
  });

  useEffect(() => {
    // Simulate API call to fetch user profile
    const fetchUserProfile = async () => {
      setLoading(true);
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Mock user profile data
      const mockProfile = {
        name: 'Alex Johnson',
        username: user?.username || 'alexj',
        email: 'alex.johnson@example.com',
        bio: 'Mathematics student passionate about algorithm design and computational mathematics.',
        education: 'BSc in Mathematics, University of Technology',
        interests: ['Number Theory', 'Algorithms', 'Machine Learning', 'Cryptography'],
        joined_date: '2025-01-15',
        challenges_completed: 27,
        average_score: 85.4,
        skills: [
          { name: 'Number Theory', level: 0.78 },
          { name: 'Linear Algebra', level: 0.65 },
          { name: 'Graph Theory', level: 0.92 },
          { name: 'Calculus', level: 0.81 },
          { name: 'Probability', level: 0.72 }
        ],
        recent_activity: [
          { type: 'challenge', name: 'Prime Factorization Challenge', date: '2025-06-15', score: 92 },
          { type: 'challenge', name: 'Matrix Eigenvalue Problem', date: '2025-06-10', score: 87 },
          { type: 'certificate', name: 'Advanced Algorithms Mastery', date: '2025-05-28' },
          { type: 'challenge', name: 'Graph Traversal Algorithms', date: '2025-05-21', score: 95 }
        ],
        badges: [
          { name: 'Algorithm Master', description: 'Completed 10 algorithm challenges with 90%+ score' },
          { name: 'Graph Theory Expert', description: 'Mastered all graph theory challenges' },
          { name: 'Early Adopter', description: 'Joined during the platform beta phase' }
        ]
      };
      
      setUserProfile(mockProfile);
      setFormData({
        name: mockProfile.name,
        bio: mockProfile.bio,
        education: mockProfile.education,
        interests: mockProfile.interests.join(', ')
      });
      setLoading(false);
    };
    
    fetchUserProfile();
  }, [user]);

  // Handle input change for profile editing
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle profile save
  const handleSaveProfile = () => {
    // In a real app, this would make an API call
    const updatedProfile = {
      ...userProfile,
      name: formData.name,
      bio: formData.bio,
      education: formData.education,
      interests: formData.interests.split(',').map(item => item.trim())
    };
    
    setUserProfile(updatedProfile);
    setEditing(false);
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
        <Paper sx={{ p: 3, mb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Avatar
                sx={{
                  width: 120,
                  height: 120,
                  fontSize: '3rem',
                  mb: 2
                }}
              >
                {userProfile.name.charAt(0)}
              </Avatar>
              
              <Typography variant="h6" align="center" gutterBottom>
                {userProfile.name}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" align="center" gutterBottom>
                @{userProfile.username}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" align="center">
                Member since {new Date(userProfile.joined_date).toLocaleDateString()}
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={9}>
              {editing ? (
                <Box component="form" noValidate autoComplete="off">
                  <TextField
                    fullWidth
                    label="Name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    margin="normal"
                  />
                  
                  <TextField
                    fullWidth
                    label="Bio"
                    name="bio"
                    value={formData.bio}
                    onChange={handleInputChange}
                    margin="normal"
                    multiline
                    rows={3}
                  />
                  
                  <TextField
                    fullWidth
                    label="Education"
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                    margin="normal"
                  />
                  
                  <TextField
                    fullWidth
                    label="Interests (comma-separated)"
                    name="interests"
                    value={formData.interests}
                    onChange={handleInputChange}
                    margin="normal"
                    helperText="Enter interests separated by commas"
                  />
                  
                  <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                      onClick={handleSaveProfile}
                    >
                      Save
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<CancelIcon />}
                      onClick={() => setEditing(false)}
                    >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h5" gutterBottom>
                      Profile
                    </Typography>
                    <Button
                      variant="outlined"
                      startIcon={<EditIcon />}
                      onClick={() => setEditing(true)}
                    >
                      Edit Profile
                    </Button>
                  </Box>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    Bio
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {userProfile.bio}
                  </Typography>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    Education
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {userProfile.education}
                  </Typography>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    Interests
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    {userProfile.interests.map((interest, index) => (
                      <Chip key={index} label={interest} sx={{ mr: 1, mb: 1 }} />
                    ))}
                  </Box>
                  
                  <Typography variant="subtitle1" gutterBottom>
                    Contact
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {userProfile.email}
                  </Typography>
                </>
              )}
            </Grid>
          </Grid>
        </Paper>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Skills & Proficiency
              </Typography>
              
              {userProfile.skills.map((skill, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2">{skill.name}</Typography>
                    <Typography variant="body2">{Math.round(skill.level * 100)}%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={skill.level * 100}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              ))}
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Statistics
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemText
                    primary="Challenges Completed"
                    secondary={userProfile.challenges_completed}
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Average Score"
                    secondary={`${userProfile.average_score}%`}
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Badges Earned"
                    secondary={userProfile.badges.length}
                  />
                </ListItem>
              </List>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              
              <List>
                {userProfile.recent_activity.map((activity, index) => (
                  <React.Fragment key={index}>
                    <ListItem alignItems="flex-start">
                      <ListItemText
                        primary={activity.name}
                        secondary={
                          <>
                            <Typography
                              component="span"
                              variant="body2"
                              color="text.primary"
                            >
                              {activity.type.charAt(0).toUpperCase() + activity.type.slice(1)}
                            </Typography>
                            {` — ${new Date(activity.date).toLocaleDateString()}`}
                            {activity.score && ` — Score: ${activity.score}%`}
                          </>
                        }
                      />
                    </ListItem>
                    {index < userProfile.recent_activity.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>
          
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Badges & Achievements
              </Typography>
              
              <Grid container spacing={2}>
                {userProfile.badges.map((badge, index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {badge.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {badge.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Profile;