# ITR Filing Assistant Chatbot

A rule-based chatbot for Income Tax Return (ITR) filing assistance in India. This chatbot guides users through the ITR filing process based on their income sources and helps them choose the right ITR form.

## Features

- 🤖 **Rule-based conversational AI** following ITR filing flowchart
- 📋 **ITR Form Selection** (ITR-1, ITR-2, ITR-3, ITR-4, ITR-5, ITR-6, ITR-7)
- 💰 **Tax Regime Comparison** (Old vs New regime)
- 📄 **Document Checklist** for each ITR form
- 🔗 **Aadhaar-PAN Linking** guidance
- ✅ **Step-by-step filing process** guidance
- 📱 **Responsive web interface**
- 🎯 **Context-aware conversations**

## Project Structure

```
itr-chatbot/
├── app.py                 # Flask server with web interface
├── chatbot_logic.py       # Rule-based chatbot logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── static/               # Static files (if needed)
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 2. Clone/Download the Project
```bash
# Create project directory
mkdir itr-chatbot
cd itr-chatbot

# Copy the provided files:
# - app.py
# - chatbot_logic.py  
# - requirements.txt
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Start the Flask server
python app.py
```

### 5. Access the Chatbot
- Open your web browser
- Go to: `http://localhost:5000`
- Start chatting with the ITR Filing Assistant!

## Usage Guide

### Starting a Conversation
1. **Welcome Message**: The chatbot greets you with quick options
2. **Choose Action**: Click "Start Filing" or type your query
3. **Follow Prompts**: Answer questions about your income sources
4. **Get Guidance**: Receive personalized ITR form recommendations

### Sample Conversation Flow
```
User: "I want to file my ITR"
Bot: "Great! Is your Aadhaar linked with PAN?"
User: "Yes"
Bot: "Perfect! Are you an Individual taxpayer?"
User: "Yes, I have salary income"
Bot: "What's your annual income range?"
User: "Below 50 lakh"
Bot: "Do you have other income sources?"
User: "Only salary"
Bot: "ITR-1 is recommended for you! Ready to proceed?"
```

### Supported Queries
- ITR form selection guidance
- Tax regime comparison
- Document checklist requests
- Aadhaar-PAN linking help
- Step-by-step filing assistance
- Tax calculation guidance

## Chatbot Logic Overview

### Rule-Based Architecture
The chatbot follows a state machine approach:

1. **State Management**: Tracks conversation progress
2. **Keyword Matching**: Identifies user intents
3. **Context Awareness**: Maintains conversation context
4. **Dynamic Responses**: Provides relevant information
5. **Quick Options**: Suggests next actions

### Key Decision Points
- Aadhaar-PAN linking status
- Filer type identification
- Income source analysis
- Income amount thresholds
- Tax regime selection
- Document verification
- Filing completion

### ITR Form Recommendations

| Form | Use Case | Income Limit |
|------|----------|--------------|
| ITR-1 | Salary only | < ₹50 lakhs |
| ITR-2 | Salary + Capital gains/House property | Any amount |
| ITR-3 | Business/Professional (regular) | Any amount |
| ITR-4 | Business/Professional (presumptive) | < ₹2 crores |
| ITR-5 | AOP, BOI, LLP, Trust | Any amount |
| ITR-6 | Companies | Any amount |
| ITR-7 | Trust, Political parties | Any amount |

## Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **CORS**: Enabled for frontend communication
- **Sessions**: In-memory conversation state management
- **API Endpoints**:
  - `POST /chat` - Process chat messages
  - `GET /` - Serve web interface
  - `POST /reset` - Reset conversation
  - `GET /status` - Get conversation status

### Frontend (HTML/CSS/JS)
- **Interface**: Single-page chat application
- **Styling**: Modern, responsive design
- **Features**: 
  - Real-time messaging
  - Quick action buttons
  - Typing indicators
  - Mobile-friendly layout

### Conversation State
```python
{
    'step': 'current_step_name',
    'user_data': {
        'filer_type': 'individual',
        'income_type': 'salary',
        'final_form': 'ITR-1',
        # ... other user inputs
    },
    'context': {
        # Additional context information
    }
}
```

## Customization

### Adding New Rules
Edit `chatbot_logic.py` to add new conversation steps:

```python
elif current_step == 'new_step':
    if contains_keywords(message, ['keyword1', 'keyword2']):
        update_conversation_state(session_id, 'next_step')
        return "Response message", ['option1', 'option2']
```

### Modifying Responses
Update the helper functions to customize responses:

```python
def get_custom_response():
    return """
    Your custom response here with:
    • Bullet points
    • 📱 Emojis
    • **Bold formatting**
    """
```

### Adding New ITR Forms
Extend the logic to handle additional ITR forms or special cases.

## Testing

### Manual Testing
1. Start the application
2. Test different conversation paths
3. Verify state transitions
4. Check response accuracy

### Sample Test Cases
- Salary-only filer → ITR-1
- Salary + Capital gains → ITR-2  
- Business income → ITR-3/ITR-4
- Company filing → ITR-6
- Invalid inputs → Proper error handling

## API Testing with curl

```bash
# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "start filing", "session_id": "test123"}'

# Reset conversation
curl -X POST http://localhost:5000/reset \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test123"}'

# Get conversation status
curl "http://localhost:5000/status?session_id=test123"
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

3. **Conversation State Issues**
   - Use `/reset` endpoint to clear session
   - Check browser console for errors

4. **Response Not Loading**
   - Verify Flask server is running
   - Check network connectivity
   - Review server logs

### Debug Mode
Enable debug mode for development:
```python
app.run(debug=True)  # Shows detailed error messages
```

## Future Enhancements

### Planned Features
- 🔐 User authentication
- 💾 Database integration for conversation history
- 📊 Analytics dashboard
- 🤖 NLP integration for better intent recognition
- 📱 Mobile app version
- 🌐 Multi-language support

### Advanced Features
- Integration with IT portal APIs
- Automatic form pre-filling
- Tax calculation engine
- Document upload and processing
- Real-time ITR status tracking

## Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is created for educational purposes as part of a mini project. Feel free to use and modify as needed.

## Support

For questions or issues:
- Check this README first
- Review the code comments
- Test with provided examples
- Create an issue if problems persist

## Acknowledgments

- Based on ITR filing flowchart requirements
- Uses Indian Income Tax rules and forms
- Designed for educational and assistance purposes

---

**Note**: This chatbot is for guidance only. For official ITR filing, please refer to the Income Tax Department's official portal and consult with tax professionals when needed.
