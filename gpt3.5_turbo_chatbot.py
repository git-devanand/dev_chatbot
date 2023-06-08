import openai

# Set up your OpenAI API credentials
openai.api_key = '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'


def ask_chatbot(question, conversation_history):
    # Format the conversation input
    conversation = [{'role': 'system', 'content': conversation_history},
                    {'role': 'user', 'content': question}]


    # Generate a model response
    response = openai.Completion.create(
        engine='text-davinci-003',  # Use ChatGPT-3.5 Turbo engine
        prompt=context,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and return the model's reply
    answer = response.choices[0].text.strip().split('\n')[0]
    return answer

# Conversation history to provide context
context = ""
with open("./datasets/legitt_documents", "r") as f:
    context = f.read()

# Ask a question
question = input("Ask a question: ")
answer = ask_chatbot(question, context)
print("Chatbot's response:", answer)
