import openai

# Your OpenAI API Key
openai.api_key = 'your_openai_key'


# Function to query OpenAI with a user prompt using the newer ChatCompletion API
def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can switch to "gpt-4" if available
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error querying OpenAI: {e}"

# Example usage
if __name__ == "__main__":
    example_prompt = "Summarize the course syllabus for CSC 244."
    openai_response = query_openai(example_prompt)
    print(f"OpenAI Response: {openai_response}")