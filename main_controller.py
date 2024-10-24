from openai_integration import query_openai
from oauth_setup import get_courses, get_syllabus_or_file, get_assignments, get_course_files
import os

# Define the output file path
output_file_path = "output_log.txt"

# Function to log messages to both console and file
def log_message(message):
    if "403" in message or "restricted" in message:  # Skip 403 errors and restricted access
        return  # Do not log this message

    with open(output_file_path, "a") as log_file:
        log_file.write(message + "\n")

# Function to process courses and fetch data using Canvas API first
def process_courses():
    # Check if the output file already exists, and remove it for fresh logging
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    
    # Fetching the list of courses from Canvas
    courses = get_courses()

    for course in courses:
        if isinstance(course, dict):  # Ensure the course is a dictionary
            name = course.get('name', 'No name available')
            course_id = course.get('id', 'No ID available')
            
            log_message(f"Course Name: {name}, Course ID: {course_id}")

            # Get the syllabus from Canvas
            syllabus = get_syllabus_or_file(course_id)
            if syllabus != "Sorry, no syllabus found in the course.":
                log_message(f"Original Syllabus:\n{syllabus}")
            else:
                log_message(f"Syllabus for course {course_id}: {syllabus}")

            # Get the assignments from Canvas
            assignments = get_assignments(course_id)
            if assignments:
                log_message(f"Assignments for course {course_id}:\n{assignments}")
            else:
                log_message(f"No assignments found for course {course_id}")

            # Get the files from Canvas
            files = get_course_files(course_id)
            if files:
                log_message(f"Files for course {course_id}:\n{files}")
            else:
                log_message(f"No files found for course {course_id}")

# Improved OpenAI prompt processing
def process_with_openai(user_prompt):
    # Read the output log (course data from Canvas) and summarize it using OpenAI
    if not os.path.exists(output_file_path):
        return "No course data available to summarize. Please refresh or fetch the data."

    with open(output_file_path, "r") as log_file:
        log_content = log_file.read()

    if log_content:
        # Summarize the course data (which includes the syllabus)
        prompt = f"{user_prompt}\n\n{log_content}"
        summary = query_openai(prompt)
        
        # Log the OpenAI result
        log_message("\n===== OpenAI Summary =====\n")
        log_message(summary)
        return summary
    else:
        return "No course data available to summarize."

# Function to extract and print relevant information from the log file
def extract_relevant_info():
    if not os.path.exists(output_file_path):
        return "The output log file does not exist."

    # Open the output log file and process line by line
    relevant_info = []
    with open(output_file_path, "r") as log_file:
        for line in log_file:
            # Skip lines with 403 errors or any reference to restricted access
            if "403" in line or "restricted" in line:
                continue

            # Capture course information and relevant data
            relevant_info.append(line.strip())

    # Return the relevant info as a string
    return "\n".join(relevant_info)

# Main interactive chatbot function
def chatbot():
    print("Welcome to the Canvas GPT Chatbot!")
    first_run = True

    while True:
        user_prompt = input("\nEnter a prompt for OpenAI (e.g., 'Summarize the course data') or '/refresh' to re-fetch data from Canvas, or '/exit' to quit:\n")

        if user_prompt.lower() == "/exit":
            print("Goodbye!")
            break
        
        if user_prompt.lower() == "/refresh":
            print("Re-fetching data from Canvas...")
            process_courses()
            print("Data has been refreshed!")
            first_run = False  # Reset after refreshing
        elif first_run:
            print("Fetching data from Canvas for the first time...")
            process_courses()
            first_run = False  # Prevent refetching in future unless asked
            print("Data has been fetched!")
        else:
            print("Using cached data from the output log file...")

        # Process the user prompt with OpenAI
        summary = process_with_openai(user_prompt)
        print("\n===== OpenAI Response =====\n")
        print(summary)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
