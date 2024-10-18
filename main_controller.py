# Importing functions from both OpenAI integration and Canvas OAuth integration files
from openai_integration import query_openai
from oauth_setup import get_courses, get_syllabus_or_file, get_assignments, get_course_files

def process_courses_with_openai():
    # Fetching the list of courses from Canvas
    courses = get_courses()

    for course in courses:
        if isinstance(course, dict):  # Ensure the course is a dictionary
            name = course.get('name', 'No name available')
            course_id = course.get('id', 'No ID available')
            
            print(f"Course Name: {name}, Course ID: {course_id}")

            # Get the syllabus from Canvas and summarize it with OpenAI
            syllabus = get_syllabus_or_file(course_id)
            if syllabus != "Sorry, no syllabus found in the course.":
                print(f"Original Syllabus:\n{syllabus}")
                
                # Summarize the syllabus using OpenAI's API
                summary = query_openai(f"Summarize the following syllabus:\n{syllabus}")
                print(f"OpenAI Summary:\n{summary}")

            # Get the assignments and files from Canvas
            assignments = get_assignments(course_id)
            print(f"Assignments:\n{assignments}")

            files = get_course_files(course_id)
            print(f"Course Files:\n{files}")

if __name__ == "__main__":
    process_courses_with_openai()
