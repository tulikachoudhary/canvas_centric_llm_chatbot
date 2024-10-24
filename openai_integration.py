import openai
import os

# Your OpenAI API Key
openai.api_key = 'sk-zmOMBtL4d_hXos-APZqoM86wPuvM-eE6ZyLWk9e_1PT3BlbkFJUdZZAE4wHaesffeQ05YkdOwZVAs1pxwOwd68ifF7UA'

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
            max_tokens=1000,  # Adjust this based on your needs and token limit
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
    
    # Formulate the prompt combining the question and log content
    combined_prompt = f"{question}\n\nHere is the log content:\n{log_content}"
    
    # Query OpenAI with the combined prompt
    openai_response = query_openai(combined_prompt)
    
    # Save the response to a file
    write_response_to_file(openai_response)
    
    return openai_response

# Example usage
if __name__ == "__main__":
    question = "give me all the assignment names"
    response = ask_openai_based_on_log(question)
    print(response)  # Display the response
