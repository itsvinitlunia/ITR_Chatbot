// botpress-chatbot/integrations/ollama-integration.js
const axios = require('axios');

class OllamaIntegration {
  constructor() {
    this.baseURL = 'http://localhost:11434';
    this.model = 'llama3';
    this.timeout = 30000; // 30 seconds timeout
  }

  async generateResponse(userMessage, context = 'ITR filing assistance') {
    try {
      const prompt = this.buildPrompt(userMessage, context);
      
      const response = await axios.post(`${this.baseURL}/api/generate`, {
        model: this.model,
        prompt: prompt,
        stream: false,
        options: {
          temperature: 0.2,
          top_p: 0.9,
          top_k: 40,
          num_ctx: 4096
        }
      }, {
        timeout: this.timeout
      });

      return this.cleanResponse(response.data.response);
    } catch (error) {
      console.error('Ollama API Error:', error.message);
      return this.getFallbackResponse();
    }
  }

  buildPrompt(userMessage, context) {
    return `You are an expert Income Tax Return (ITR) filing assistant in India. Provide accurate, helpful information.

CONTEXT: ${context}
QUESTION: "${userMessage}"

GUIDELINES:
- Provide factual information about Indian tax laws
- Keep responses concise (2-3 sentences)
- Direct to official sources if unsure
- Focus on educational guidance for ITR learning
- Be polite and professional

RESPONSE:`;
  }

  cleanResponse(response) {
    return response
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/```[\s\S]*?```/g, '')
      .trim();
  }

  getFallbackResponse() {
    return "I'm currently having trouble accessing detailed tax information. Please visit the official Income Tax e-Filing portal at incometax.gov.in for accurate guidance, or consult with a qualified tax professional.";
  }

  async testConnection() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`, {
        timeout: 5000
      });
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }
}

module.exports = { OllamaIntegration };