import express from 'express';
import cors from 'cors';
import chatbotHandler from './chatbot-handler.js';

// Load environment variables
const PORT = process.env.PORT || 5000;

const app = express();

// Middleware
app.use(cors({
  origin: 'http://localhost:5173', // Explicitly allow frontend
  credentials: true
}));
app.use(express.json());

// Routes
app.use('/api/chat', chatbotHandler);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Server is running',
    port: PORT,
    frontend: 'http://localhost:5173'
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
  console.log(`🎯 Frontend: http://localhost:5173`);
});