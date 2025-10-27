// src/lib/ollama-integration.ts

export interface OllamaResponse {
  response: string;
  done: boolean;
  model: string;
  created_at: string;
}

export interface OllamaError {
  error: string;
}

export class OllamaIntegration {
  private baseURL = 'http://localhost:11434';
  private model = 'llama3';

  async generateResponse(userMessage: string, context: string = 'ITR filing assistance'): Promise<string> {
    try {
      const prompt = this.buildPrompt(userMessage, context);
      
      const response = await fetch(`${this.baseURL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: this.model,
          prompt: prompt,
          stream: false,
          options: {
            temperature: 0.2,
            top_p: 0.9,
            top_k: 40,
            num_ctx: 4096
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Ollama API error: ${response.statusText}`);
      }

      const data: OllamaResponse = await response.json();
      return this.cleanResponse(data.response);
    } catch (error) {
      console.error('Ollama API Error:', error);
      return this.getFallbackResponse();
    }
  }

  private buildPrompt(userMessage: string, context: string): string {
    return `You are an expert Income Tax Return (ITR) filing assistant in India. Your role is to provide accurate, helpful information about tax filing, forms, deadlines, and procedures.

IMPORTANT CONTEXT: ${context}
USER QUESTION: "${userMessage}"

CRITICAL GUIDELINES:
1. Provide clear, factual information about Indian tax laws only
2. If unsure about specific details, direct users to official sources like incometax.gov.in
3. Keep responses concise and actionable (2-3 sentences maximum)
4. Mention important deadlines and procedures when relevant
5. Be polite, professional, and educational
6. Focus on helping users understand ITR filing process
7. Do not provide financial advice - only educational guidance

RESPONSE:`;
  }

  private cleanResponse(response: string): string {
    return response
      .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold markdown
      .replace(/\*(.*?)\*/g, '$1')     // Remove italic markdown
      .replace(/```[\s\S]*?```/g, '')  // Remove code blocks
      .replace(/\[.*?\]/g, '')         // Remove citations
      .trim();
  }

  private getFallbackResponse(): string {
    return "I'm currently having trouble accessing detailed tax information. For accurate and personalized assistance, please visit the official Income Tax e-Filing portal at incometax.gov.in or consult with a qualified tax professional.";
  }

  // Test connection to Ollama
  async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/api/tags`);
      return response.ok;
    } catch (error) {
      console.warn('Ollama connection test failed:', error);
      return false;
    }
  }

  // Get available models
  async getAvailableModels(): Promise<string[]> {
    try {
      const response = await fetch(`${this.baseURL}/api/tags`);
      if (response.ok) {
        const data = await response.json();
        return data.models?.map((model: any) => model.name) || [];
      }
      return [];
    } catch (error) {
      return [];
    }
  }
}

// Singleton instance
export const ollamaIntegration = new OllamaIntegration();