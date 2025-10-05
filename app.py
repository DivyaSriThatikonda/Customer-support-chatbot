# from core_logic import setup_retriever_and_llm
#
# if __name__ == "__main__":
#     print("Setting up retriever and LLM... This might take a moment.")
#     retriever, llm = setup_retriever_and_llm()
#
#     query = "What's the refund policy?"
#     print(f"\nTesting with query: '{query}'")
#
#     # --- UPDATED LOGIC ---
#     # 1. Retrieve documents using the new .invoke() method
#     retrieved_docs = retriever.invoke(query)
#
#     # 2. Check if any documents were found
#     if not retrieved_docs:
#         answer = "I could not find any relevant documents to answer that question."
#     else:
#         # 3. Combine the context and call the model
#         context = "\n".join([doc.page_content for doc in retrieved_docs])
#         result = llm.pipeline(question=query, context=context)
#         answer = result.get('answer', 'No answer could be found.')
#
#     print(f"Response: {answer}")

import streamlit as st
from core_logic import setup_retriever_and_llm


# Use Streamlit's caching to load models only once
@st.cache_resource
def load_components():
    """
    Loads the retriever and LLM. The @st.cache_resource decorator
    ensures this function only runs once, saving time and resources.
    """
    return setup_retriever_and_llm()


def main():
    st.title("📄 Customer Support Bot")
    st.write("Ask a question about our policies, and I'll do my best to answer!")

    # Load the backend components from the cached function
    retriever, llm = load_components()

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("How can I help you?"):
        # Display the user's message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get and display the bot's response
        with st.spinner("Thinking..."):
            # 1. Retrieve relevant documents
            retrieved_docs = retriever.invoke(prompt)

            # 2. Check for results and call the model
            if not retrieved_docs:
                answer = "I could not find any relevant documents to answer that question."
            else:
                context = "\n".join([doc.page_content for doc in retrieved_docs])
                result = llm.pipeline(question=prompt, context=context)
                answer = result.get('answer', 'No answer could be found.')

            # Display the bot's answer
            with st.chat_message("assistant"):
                st.markdown(answer)
            # Add bot's answer to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()