// botpress-chatbot/actions/ollama-fallback.js
const { OllamaIntegration } = require('../integrations/ollama-integration');

const ollama = new OllamaIntegration();

// Tax-related keywords to identify when to use Ollama
const taxKeywords = [
  'itr', 'income tax', 'tds', 'form 16', '26as', 'refund', 'deduction',
  'hra', '80c', 'section', 'tax saving', 'filing', 'deadline',
  'pan', 'aadhaar', 'e-verify', 'revised return', 'notice',
  'capital gain', 'house property', 'business income', 'professional',
  'exemption', 'rebate', 'advance tax', 'self assessment'
];

async function ollamaFallbackAction(event) {
  const userMessage = event.payload.text.toLowerCase();
  
  // Check if it's a tax-related question
  const isTaxRelated = taxKeywords.some(keyword => 
    userMessage.includes(keyword)
  );

  // Check if it's a complex question that might need AI
  const isComplexQuestion = 
    userMessage.includes('how to') || 
    userMessage.includes('what if') ||
    userMessage.includes('explain') ||
    userMessage.includes('difference between') ||
    userMessage.includes('calculate') ||
    userMessage.includes('step by step');

  // Get QnA confidence (if available)
  const qnaConfidence = event.state.session.qnaConfidence || 0;

  // Use Ollama if:
  // 1. QnA confidence is low AND it's tax-related, OR
  // 2. It's a complex tax question, OR  
  // 3. User explicitly asks for explanation
  const shouldUseOllama = 
    (qnaConfidence < 0.7 && isTaxRelated) || 
    (isComplexQuestion && isTaxRelated) ||
    userMessage.includes('explain');

  if (shouldUseOllama) {
    try {
      console.log('Using Ollama for question:', userMessage);
      
      const context = determineContext(userMessage);
      const ollamaResponse = await ollama.generateResponse(event.payload.text, context);
      
      // Add educational disclaimer
      const finalResponse = `${ollamaResponse}\n\n*Note: This is AI-generated educational guidance. For official information and actual filing, please verify with incometax.gov.in or consult a tax professional.*`;
      
      return {
        success: true,
        response: finalResponse,
        source: 'ollama'
      };
    } catch (error) {
      console.error('Ollama fallback error:', error);
      return {
        success: false,
        response: "I'm not sure about that specific tax question. Could you rephrase or ask about common ITR topics like form selection, deadlines, or basic filing procedures?",
        source: 'error'
      };
    }
  }

  return {
    success: false,
    response: null,
    source: 'qna_only'
  };
}

function determineContext(userMessage) {
  if (userMessage.includes('form') || userMessage.includes('itr-')) {
    return 'ITR form selection and specifications';
  } else if (userMessage.includes('deadline') || userMessage.includes('due date')) {
    return 'ITR filing deadlines and late filing penalties';
  } else if (userMessage.includes('calculate') || userMessage.includes('tax liability')) {
    return 'Tax calculation methods and examples';
  } else if (userMessage.includes('deduction') || userMessage.includes('80c') || userMessage.includes('hra')) {
    return 'Tax deductions and exemptions';
  } else if (userMessage.includes('refund')) {
    return 'Tax refund process and status checking';
  } else if (userMessage.includes('tds') || userMessage.includes('26as')) {
    return 'TDS reconciliation and Form 26AS';
  } else if (userMessage.includes('how to') || userMessage.includes('step')) {
    return 'Step-by-step ITR filing procedure';
  }
  
  return 'General Income Tax Return filing assistance';
}

module.exports = { ollamaFallbackAction };