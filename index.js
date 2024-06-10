const express = require('express');
const app = express();

app.use(express.json());

app.post('/ussd', (req, res) => {
  const { text } = req.body;
  let response = '';

  if (text === '') {
    response = 'CON Welcome to the USSD app\n1. Option 1\n2. Option 2';
  } else if (text === '1') {
    response = 'END You chose option 1';
  } else if (text === '2') {
    response = 'END You chose option 2';
  } else {
    response = 'END Invalid choice';
  }

  res.send(response);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
