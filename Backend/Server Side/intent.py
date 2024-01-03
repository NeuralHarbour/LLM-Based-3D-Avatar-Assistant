import spacy

# Load the saved model
loaded_nlp = spacy.load("./Intclass")

# Continuously prompt the user for input
while True:
    # Get user input
    user_input = input("Enter a text to classify intent (or 'exit' to stop): ")

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        break

    # Classify intent for user input
    doc = loaded_nlp(user_input)
    intent = max(doc.cats, key=doc.cats.get)
    confidence = doc.cats[intent]

    # Print the result
    print(f"Predicted Intent: {intent} - Confidence: {confidence}")
