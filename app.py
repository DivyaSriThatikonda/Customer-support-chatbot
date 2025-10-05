

# import streamlit as st
# from core_logic import setup_retriever_and_llm


# # Use Streamlit's caching to load models only once
# @st.cache_resource
# def load_components():
#     """
#     Loads the retriever and LLM. The @st.cache_resource decorator
#     ensures this function only runs once, saving time and resources.
#     """
#     return setup_retriever_and_llm()


# def main():
#     st.title("📄 Customer Support Bot")
#     st.write("Ask a question about our policies, and I'll do my best to answer!")

#     # Load the backend components from the cached function
#     retriever, llm = load_components()

#     # Initialize chat history in session state
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display past messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Handle new user input
#     if prompt := st.chat_input("How can I help you?"):
#         # Display the user's message
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Get and display the bot's response
#         with st.spinner("Thinking..."):
#             # 1. Retrieve relevant documents
#             retrieved_docs = retriever.invoke(prompt)

#             # 2. Check for results and call the model
#             if not retrieved_docs:
#                 answer = "I could not find any relevant documents to answer that question."
#             else:
#                 context = "\n".join([doc.page_content for doc in retrieved_docs])
#                 result = llm.pipeline(question=prompt, context=context)
#                 answer = result.get('answer', 'No answer could be found.')

#             # Display the bot's answer
#             with st.chat_message("assistant"):
#                 st.markdown(answer)
#             # Add bot's answer to chat history
#             st.session_state.messages.append({"role": "assistant", "content": answer})


# if __name__ == "__main__":

#     main()







import streamlit as st
import logging
import random
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# --- The SupportBotAgent Class (Contains all the core logic) ---
class SupportBotAgent:
    def __init__(self, document_path):
        """
        Initializes the agent, loads models, and processes the document.
        """
        logging.info("Initializing SupportBotAgent...")
        
        # [cite_start]Load a pre-trained model for question-answering [cite: 17]
        self.qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        
        # [cite_start]Load a model to create embeddings for semantic search [cite: 18]
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        logging.info("AI models loaded successfully.")
        
        # [cite_start]Load and process the document [cite: 7]
        self.document_text = self._load_document(document_path)
        
        # [cite_start]Split the document into sections (paragraphs) for easier retrieval [cite: 34]
        self.sections = self.document_text.strip().split('\n\n')
        
        # [cite_start]Create embeddings for each section of the document [cite: 35]
        self.section_embeddings = self.embedder.encode(self.sections, convert_to_tensor=True)
        logging.info(f"Document '{document_path}' loaded and processed.")

    def _load_document(self, path):
        """
        [cite_start]A helper method to load text from a .txt file. [cite: 16]
        """
        logging.info(f"Loading document from {path}...")
        try:
            with open(path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            logging.error(f"Error: Document not found at {path}. Please check the file path.")
            return ""

    def _find_relevant_section(self, query):
        """
        [cite_start]Finds the most relevant document section for a given query using cosine similarity. [cite: 18]
        """
        if not self.sections:
            return None
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = util.cos_sim(query_embedding, self.section_embeddings)[0]
        best_idx = similarities.argmax()
        if similarities[best_idx] > 0.5:
            return self.sections[best_idx]
        else:
            return None
    
    def answer_query(self, query):
        """
        [cite_start]Generates an answer to a query based on the document. [cite: 8]
        """
        context = self._find_relevant_section(query)
        # [cite_start]Handles cases where the query isn't covered by the document gracefully. [cite: 12]
        if not context:
            return "I don't have enough information to answer that. Please try rephrasing your question."
        result = self.qa_model(question=query, context=context)
        return result['answer']

    def _adjust_response(self, query, original_response, feedback):
        """
        [cite_start]Adjusts the response based on the simulated feedback. [cite: 9, 10]
        """
        if feedback == "too vague":
            context = self._find_relevant_section(query)
            if context:
                return f"{original_response} (For more context: {context})"
        elif feedback == "not helpful":
            new_query = f"Can you give me more details about {query.lower().replace('how do i', '')}?"
            return self.answer_query(new_query)
        return original_response

# --- Streamlit App Code ---

# Use caching to load the bot only once
@st.cache_resource
def load_bot():
    return SupportBotAgent("faq.txt")

# Load the bot
bot = load_bot()

# Set up the title of the web page
st.title("🤖 Customer Support Bot")
st.write("This bot uses a document to answer questions. Ask anything about our policies or services.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from the chat interface
if prompt := st.chat_input("How can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display bot response
    with st.chat_message("assistant"):
        response = bot.answer_query(prompt)
        st.write(response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
