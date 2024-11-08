# Calmora - Your Compassionate Conversational AI

<p align="center">
  <img src="logo.jpg" alt="Calmora Logo" width="300" height="300">
  <style>
    img {
      border-radius: 50%;
    }
  </style>
</p>

## Overview

**Calmora** addresses mental health by providing an empathetic conversational AI that listens and responds in real time. It offers a non-judgmental space, helping users feel heard, reducing loneliness, and making mental health support more accessible to everyone.

---

## Project Description

### Context and Problem Statement

In today’s fast-paced, digitally connected world, more people are feeling isolated than ever before. Social media often replaces real connection, and many individuals live far from family or lack close friends they can trust. As a result, people may struggle with mental health challenges, carrying their burdens in silence because they lack a safe space to share and process their feelings.

**Calmora** aims to bridge this emotional gap by providing a compassionate conversational AI designed to listen without judgment. It serves as a trusted friend who is always available, helping users process their thoughts and emotions. By simply being heard, individuals can experience relief from stress, loneliness, and isolation. Calmora offers an emotionally supportive environment, enabling people to unburden themselves and feel acknowledged.

---

## Key Features

- **Empathetic Conversational AI**: Calmora creates an accessible, always-available presence that feels like a caring friend. Unlike traditional AI, Calmora is designed with empathy in mind—it listens, understands, and responds just like a real friend would, without judgment.
  
- **Mental and Emotional Well-being**: Calmora offers a safe space for users to express themselves openly, supporting mental wellness through conversation. It helps people feel emotionally supported in a world where meaningful conversations can be hard to find.
  
- **Real-World Use Case**: Imagine coming home after a stressful day at work, feeling demotivated or isolated. Calmora greets you with warmth, helping you process your emotions by asking how your day was and allowing you to express yourself freely without fear of judgment.

- **Natural Language Processing (NLP) & Realistic Voice**: Calmora uses advanced NLP and text-to-speech technology to create realistic, warm, and empathetic voice interactions, making users feel truly heard and understood.

---

## Technologies Used

**Calmora** is built with Python and integrates cloud-based APIs to enhance the language understanding and voice generation. The following technologies are used:

- **Cohere API**: For advanced natural language processing, allowing Calmora to understand user inputs and respond meaningfully.
- **Eleven Labs API**: Provides realistic, human-like voice synthesis to ensure that Calmora's responses feel warm, genuine, and emotionally supportive.

---

## Project Architecture

### File Structure

```plaintext
calmora/
│
├── config/
│   ├── config.py  # Configuration file containing API keys and DB credentials
│   └── example.config.py  # Example configuration file
│
├── main_utility/
│   ├── ai_model_conversation.py  # AI model for conversation logic
│   ├── chatHistory.py  # Handles chat history storage and retrieval
│   ├── database.py  # Database interactions and management
│   ├── languase.py  # Language processing utilities
│   ├── listening.py  # Handles listening and speech recognition
│   └── speaking.py  # Handles text-to-speech and voice responses
│
├── utils/
│   └── AI_Response.py  # Utility functions for AI responses
│
├── main.py  # Main application logic and conversational AI implementation
│
└── requirements.txt  # List of required Python packages
```

## Key Configuration Details

- **Cohere API Key**: Used for natural language understanding and processing.
- **Eleven Labs API Key**: Used for generating realistic, empathetic speech responses.
- **Database Configuration**: Stores application data such as logs, user interactions, etc. The database used is MySQL.

## How to Use

### Prerequisites

Before using Calmora, ensure you have the following installed:

- Python 3.7 or higher
- Basic knowledge of python and using cloud apis
- Access to the Cohere API (for NLP) and Eleven Labs API (for voice synthesis)

### Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/your-username/calmora.git
cd calmora
```

### Configure API Keys

Create a file named `config.py` in the `config` directory (use `config.example.py` as a template).  
Add your Cohere API Key, Eleven Labs API Key, and other relevant credentials into the `config.py` file.

### Install Dependencies

You may need to install the necessary Python libraries:

```bash
pip install -r requirements.txt
```

### Run the Application

To start interacting with Calmora, run the following:

```bash
python main.py
```

### Interact with Calmora

Calmora will start and ask you questions to guide a friendly, empathetic conversation. You can input your thoughts and receive supportive responses.

## Future Enhancements

While Calmora is designed to be an empathetic companion, future iterations will explore:

- Expanding the range of emotional responses and tone detection.
- Integrating more advanced mental health resources, such as mood tracking and personalized self-care tips.
- Making Calmora available on mobile devices to provide accessibility anytime, anywhere.

## Vision and Impact

Calmora's vision is to make mental and emotional support more accessible to everyone, providing a compassionate presence whenever needed. By promoting open communication, Calmora helps individuals feel supported and less alone in their daily lives.

## Contributing

If you'd like to contribute to Calmora, feel free to fork the repository, create a pull request, and share any ideas or improvements you have. We welcome contributions that can help improve the project and expand its capabilities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About the Author

**Tarun Kumar**  
Founder & Developer of Calmora  
[LinkedIn Profile](https://www.linkedin.com/in/tarunkumar8278)  
[GitHub Profile](https://github.com/tarunkumar2005)  

Feel free to reach out via email or through LinkedIn for any questions, collaboration, or feedback!

## Contact Information

Email: [tarunkumar6258278@gmail.com](mailto:tarunkumar6258278@gmail.com)  
LinkedIn: [Tarun Kumar LinkedIn](https://www.linkedin.com/in/tarunkumar8278)

## Learn More

To see Calmora in action and learn more about how it works, check out the following resources:

- [YouTube Video Overview](https://www.youtube.com/watch?v=CGk3eAJ-a5s)
- [LinkedIn Post: Calmora's Development Journey](https://www.linkedin.com/posts/tarunkumar8278_aiinnovation-conversationalai-microsoftcopilot-activity-7258030659460374528-Pqx7/?utm_source=share&utm_medium=member_desktop)

Thank you for exploring Calmora—a compassionate AI for mental wellness!