import json
import re
import random_responses


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


def get_response(input_string, user_name):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return f"{user_name}, please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()


def chat():
    print("Welcome to the chatbot! Type 'exit' at any time to end the chat.")
    user_name = input("What's your name? ").strip().capitalize()
    print(f"Nice to meet you, {user_name}! Let's chat.\n")

    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() == "exit":
            print(f"Goodbye, {user_name}! It was great chatting with you.")
            break
        print("Bot:", get_response(user_input, user_name))


if __name__ == "__main__":
    chat()
