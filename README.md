# Healthify - AI-Powered Mental Health Support Platform 🧠

Healthify is an interactive mental health support chatbot built with Streamlit and powered by the Groq AI platform. It provides users with empathetic conversations, emotional support, and mental health resources in a secure and private environment.

## 🌟 Features

- **Interactive Chat Interface**: Real-time conversations with an AI-powered mental health support assistant
- **Conversation History**: Save and access previous chat sessions
- **User Metrics**: Track engagement through session statistics
- **Responsive Design**: Modern, user-friendly interface that works across devices
- **Privacy-Focused**: Local conversation storage and secure handling of sensitive information
- **Professional Guidance**: Automatic recognition of serious issues with appropriate professional referrals

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key (Sign up at [Groq's website](https://groq.com))
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tirthgupta97/Groq-Chat-App.git
cd Groq-Chat-App
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Running Locally

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

- streamlit
- langchain
- langchain-groq
- python-dotenv
- json
- datetime

## 🚀 Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your Groq API key in Streamlit Cloud secrets:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

## 🔧 Configuration

The application can be configured through the following environment variables:

- `GROQ_API_KEY`: Your Groq API key
- Additional model parameters can be adjusted in the `create_conversation()` function

## 🎨 Customization

### Modifying the Chat Interface

The chat interface can be customized by editing the CSS in the `load_css()` function. Key customizable elements include:

- Color schemes
- Font styles
- Message bubble design
- Layout spacing
- Animation effects

### Adjusting the AI Model

The AI model's behavior can be modified by:

1. Updating the prompt template in the `TEMPLATE` variable
2. Adjusting the model parameters in `create_conversation()`
3. Modifying the conversation memory handling

## 📊 Features in Detail

### Conversation Management
- Real-time chat with timestamp tracking
- Session persistence
- Conversation history storage and retrieval

### User Interface
- Responsive design with modern aesthetics
- Clear message threading
- Intuitive navigation
- Session metrics display

### AI Capabilities
- Emotional support and empathy
- Crisis recognition and professional referral
- Personalized responses
- Context awareness

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## 🛟 Support

For support:
1. Open an issue on GitHub
2. Contact the development team
3. Check the documentation

## 🔒 Privacy & Security

- All conversations are stored locally
- No personal information is transmitted to external services
- API communications are encrypted
- Users can delete their conversation history at any time

## ⚠️ Disclaimer

Healthify is not a replacement for professional mental health care. It is designed to provide support and guidance but should not be used in place of professional medical advice, diagnosis, or treatment.

## 🙏 Acknowledgments

- Groq AI for providing the language model
- Streamlit for the web framework
- The open-source community for various dependencies

---

Built with ❤️ for mental health support
