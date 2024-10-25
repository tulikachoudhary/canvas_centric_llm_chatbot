import openai
import os

# Your OpenAI API Key
openai.api_key = 'sk-AHxzOeF5w4sTwj-ePmMklfmcMUAbhUR_pAVyE1W3DfT3BlbkFJQQiLORnGV9Iv29oOVlB58E2ib9j-Ilx2ai8eKz18UA'

# Path to the input log file
output_file_path = "output_log.txt"

# Path to the file where the OpenAI response will be saved
response_output_file_path = "openai_response_log.txt"

# Function to read from output log file
def read_output_log():
    if not os.path.exists(output_file_path):
        return None
    
    with open(output_file_path, "r") as log_file:
        return log_file.read()

# Function to query OpenAI with a user prompt using the newer ChatCompletion API
def query_openai(prompt, model="gpt-4"):
    try:
        response = openai.ChatCompletion.create(
            model=model,  # Switch to "gpt-4" or "gpt-4-32k"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,  # Adjust this based on your needs and token limit
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error querying OpenAI: {e}"

# Function to write OpenAI response to a new file
def write_response_to_file(response):
    with open(response_output_file_path, "w") as response_file:
        response_file.write(response + "\n")

# Function to process the log file and ask OpenAI based on its content
def ask_openai_based_on_log(question):
    log_content = read_output_log()
    
    if log_content is None:
        return "Log file is empty or doesn't exist."

    # Conditionally append log content only if the question is related to course data
    if "assignment" in question.lower() or "course" in question.lower() or "file" in question.lower():
        # Formulate the prompt combining the question and log content
        combined_prompt = f"{question}\n\nHere is the log content:\n{log_content}"
    else:
        # If it's a general question like "hi", use only the question
        combined_prompt = question

    # Query OpenAI with the combined prompt
    openai_response = query_openai(combined_prompt)
    
    # Save the response to a file
    write_response_to_file(openai_response)
    
    return openai_response

# Example chatbot function to handle interaction
def chatbot():
    print("Welcome to the Canvas GPT Chatbot!")
    
    while True:
        user_prompt = input("\nEnter a prompt for OpenAI (or type '/exit' to quit):\n")

        if user_prompt.lower() == "/exit":
            print("Goodbye!")
            break
        
        # Get the response from OpenAI based on the user prompt
        response = ask_openai_based_on_log(user_prompt)
        
        # Display the response
        print("\n===== OpenAI Response =====\n")
        print(response)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
