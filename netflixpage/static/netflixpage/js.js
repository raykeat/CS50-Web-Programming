import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

function ActionAreaCard() {
  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="140"
          image="/static/netflixpage/netflix-reuse-official.jpg"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            Show
          </Typography>
          <Typography variant="body2" color="text.secondary">
            This is a porn film
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}

const element = document.getElementById('app')
ReactDOM.render(<ActionAreaCard />, element)
