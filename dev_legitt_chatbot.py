from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import random

tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")

model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")


# Load the question-answering model
# model = "deepset/roberta-base-squad2"
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)


greetings = ["Hello! How can I assist you?", "How can I help you?", "Welcome to Legitt. I am here to help you \nWhat do you want to do next?"]


# Define a function to interact with the chatbot
def chatbot():
    while True:
        # Get user input
        question = input("User: ")

        # Exit if user types 'exit'
        if question.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Provide answer using the question-answering model
        context = ""
        with open("./datasets/legitt_documents", "r") as f:
            context = f.read()

        answer = qa_pipeline(question=question, context=context)

        # Print the answer
        print("Chatbot:", answer['answer'])

# Start the chatbot
print("Chatbot: {}".format(greetings[random.randint(0, len(greetings))]))
chatbot()
