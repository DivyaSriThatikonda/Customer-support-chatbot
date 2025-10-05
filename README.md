# Customer-support-chatbot
# Customer Support Bot with Agentic Workflow

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project, developed for an assignment from Serri, is a smart customer support bot built in Python. It leverages modern NLP models to read and understand a provided document, answer user questions based on its content, and refine its responses through a simulated feedback mechanism. The entire application is presented through a clean, interactive web interface built with Streamlit.

---
## 🚀 Live Demo

The application is deployed and publicly accessible.

[**--> Access the Deployed App Here <--**](YOUR_DEPLOYMENT_LINK_HERE)

---
## ✨ Key Features

**Document-Based Q&A**: The bot ingests a text document (e.g., a company FAQ) and uses it as its sole knowledge base to answer questions.
**Semantic Search**: It uses `sentence-transformer` embeddings to understand the semantic meaning of a user's query and find the most relevant section in the knowledge base, rather than just matching keywords.
**Adaptive Response Refinement**: The core agentic logic allows the bot to evaluate its own answers based on simulated feedback (e.g., "too vague," "not helpful") and adjust its strategy to provide a better response. 
**Graceful Fallbacks**: The bot can recognize when a query is outside the scope of the provided document and will inform the user gracefully.
**Transparent Logging**: Every major action and decision the bot makes is recorded in a log file for transparency and debugging. 
**Interactive Web UI**: A simple and intuitive chat interface built with Streamlit allows for easy interaction with the bot.

---
## 🛠️ How It Works

The bot operates through a multi-step pipeline:

1.  **Initialization**: Upon starting, the agent loads the pre-trained NLP models (a question-answering model and a sentence-embedding model) from Hugging Face.
2.  **Document Processing**: It reads the `faq.txt` file, splits it into logical sections (paragraphs), and creates a numerical vector embedding for each section. These embeddings are stored for efficient searching.
3.  **Query Handling**:
    * A user submits a query through the Streamlit interface.
    * The agent creates an embedding for the user's query.
    * It calculates the cosine similarity between the query embedding and all the document section embeddings to find the most relevant context.
4.  **Answer Generation**: The identified context and the original query are passed to the question-answering model, which extracts the most likely answer from the text.
5.  **Display**: The final answer is displayed to the user in the chat interface.

---
## 💻 Technologies Used

* **Language**: Python 3.9+
* **Web Framework**: Streamlit
* **NLP Models**: Hugging Face `transformers`
* **Semantic Search**: `sentence-transformers`
* **Core Backend**: PyTorch

---
## ⚙️ Setup and Local Installation

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone <YOUR_GITHUB_REPO_URL>
    cd <YOUR_PROJECT_DIRECTORY>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```
    Your web browser should automatically open to the application's local URL.

---
## 📁 Project Structure
├── app.py                  # Main Streamlit application script
├── faq.txt                 # Source document for the bot
├── requirements.txt        # Python dependencies
├── sample_support_bot_log.txt  # Example log output of the bot's actions
├── .gitignore              # Specifies files for Git to ignore
└── README.md               # This file


---
## 📝 Logging

[cite_start]The application logs key events, decisions, and errors to a file named `support_bot_log.txt`. [cite: 26, 54] This provides transparency into the bot's internal workings. [cite_start]A sample log file, `sample_support_bot_log.txt`, is included in this repository to demonstrate the output. [cite: 54]

---
## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
