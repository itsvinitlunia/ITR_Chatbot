/**
 * Ollama AI Wrapper
 * Handles communication with Ollama API
 */

class OllamaWrapper {
  constructor() {
    this.baseURL = 'http://localhost:11434';
    this.model = 'llama3:latest';
    this.timeout = 30000;
  }

  async generateResponse(userMessage) {
    try {
      console.log('🦙 Calling Ollama API...');
      
      const response = await fetch(`${this.baseURL}/api/generate`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.model,
          prompt: this.buildPrompt(userMessage),
          stream: false,
          options: {
            temperature: 0.3,
            top_p: 0.9,
            top_k: 40
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Ollama API error: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Ollama response received');
      
      return this.formatResponse(data.response);
      
    } catch (error) {
      console.error('❌ Ollama API call failed:', error.message);
      throw new Error('AI service temporarily unavailable. Please ensure Ollama is running.');
    }
  }

  buildPrompt(userMessage) {
    return `You are an expert Income Tax Return (ITR) assistant for India. Provide accurate, helpful information about Indian tax filing.

USER QUESTION: "${userMessage}"

Please provide a professional response that:
- Answers the question accurately based on Indian tax laws
- Is concise and easy to understand (2-4 sentences)
- Includes relevant examples if helpful
- Mentions important deadlines or requirements if applicable

Keep the tone professional and educational.

RESPONSE:`;
  }

  formatResponse(response) {
    // Clean up response
    const cleanResponse = response
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .trim();
    
    return `${cleanResponse}\n\n*For official filing, please verify with incometax.gov.in.*`;
  }
}

export default OllamaWrapper;