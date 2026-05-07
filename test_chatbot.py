from chatbot import movie_assistant

print("Movie Assistant is running. Type 'exit' to stop.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    reply = movie_assistant(user_input)
    print("\nBot:", reply)
    print()