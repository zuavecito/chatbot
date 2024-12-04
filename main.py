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
    # Split and filter out empty tokens
    split_message = [word for word in re.split(r'\s+|[,;?!.-]\s*', input_string.lower()) if word]
    score_list = []

    #print(f"\n[DEBUG] User Input: {split_message}")  # Debugging: Show split input

    # Check all the responses
    for index, response in enumerate(response_data):
        response_score = 0
        required_score = 0
        required_words = response["required_words"]
        user_input_phrases = response["user_input"]

        # Check if there are any required words
        if required_words:
            for word in required_words:
                if word in split_message:
                    required_score += 1

        # Ensure all required words are present
        if required_score == len(required_words):
            # Check if any complete phrase in user_input matches the input string
            for phrase in user_input_phrases:
                if phrase in input_string.lower():
                    response_score += 1

            # Check individual word matches for additional scoring
            for word in split_message:
                if word in user_input_phrases:
                    response_score += 1

        # Debugging: Log response and its score
        #print(f"[DEBUG] Response {index + 1}: {response['bot_response']}")
        #print(f"[DEBUG] Required Score: {required_score}/{len(required_words)}, Response Score: {response_score}")

        # Add score to list
        score_list.append(response_score)

    # Debugging: Show all scores
   # print(f"[DEBUG] Score List: {score_list}")

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    if best_response == 0:
        #print("[DEBUG] No good match found. Using a random response.")  # Debugging
        return random_responses.random_string()

    response_index = score_list.index(best_response)
    #print(f"[DEBUG] Selected Response: {response_data[response_index]['bot_response']}")  # Debugging

    # Check if input is empty
    if input_string == "":
        return f"{user_name}, please type something so we can chat :("

    return response_data[response_index]["bot_response"]

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
