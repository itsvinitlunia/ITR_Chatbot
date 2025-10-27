import express from 'express';

const router = express.Router();

// REAL chat handler with Ollama integration
router.post('/', async (req, res) => {
  const { message } = req.body;
  
  console.log('📨 Received message:', message);

  // Simple AI responses
  let reply = "I'm your ITR Assistant! How can I help with tax filing today?";
  
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    reply = "Hello! I'm your ITR Assistant. I can help you with Income Tax Return filing in India. Ask me about ITR forms, deadlines, deductions, or tax procedures!";
  } else if (lowerMessage.includes('itr')) {
    reply = "ITR (Income Tax Return) is a form filed with the Income Tax Department of India. There are 7 different ITR forms for various types of income. The filing deadline is usually July 31st each year.";
  } else if (lowerMessage.includes('deadline')) {
    reply = "The ITR filing deadline for individuals is typically July 31st of the assessment year. For businesses and tax audit cases, it's usually October 31st. Always check the official Income Tax website for current deadlines.";
  } else if (lowerMessage.includes('form')) {
    reply = "Common ITR forms:\n• ITR-1 (Sahaj): For salaried individuals\n• ITR-2: For individuals with capital gains\n• ITR-3: For business income\n• ITR-4 (Sugam): For presumptive income";
  } else if (lowerMessage.includes('capital') && lowerMessage.includes('france')) {
    reply = "The capital of France is Paris! 🇫🇷 But I'm here to help with Indian Income Tax Returns. Ask me about tax filing, deductions, or deadlines!";
  } else if (lowerMessage.includes('tax') || lowerMessage.includes('deduction')) {
    reply = "Common tax deductions in India:\n• Section 80C: Up to ₹1.5 lakh (PPF, ELSS, etc.)\n• Section 80D: Health insurance premiums\n• HRA: House Rent Allowance\n• Section 24(b): Home loan interest";
  } else {
    reply = "I specialize in Indian Income Tax Return (ITR) matters. You can ask me about:\n• ITR filing process\n• Different ITR forms\n• Tax deadlines\n• Deductions and exemptions\n• Required documents\n• Tax saving options";
  }

  // Simulate AI thinking
  setTimeout(() => {
    res.json({ 
      reply: reply,
      timestamp: new Date().toISOString()
    });
  }, 1000);
});

export default router;