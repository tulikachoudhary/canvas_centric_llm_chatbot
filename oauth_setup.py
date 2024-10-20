import requests

# Your personal access token
access_token = "your-token"
# Headers for the request
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Function to retrieve list of courses
def get_courses():
    url = 'https://canvas.instructure.com/api/v1/users/self/courses'
    response = requests.get(url, headers=headers)
    
    # Ensure the response is valid and contains JSON data
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching courses: {response.status_code}")
        return []

# Function to get the syllabus for a course
def get_syllabus(course_id):
    url = f"https://canvas.instructure.com/api/v1/courses/{course_id}?include=syllabus_body"
    response = requests.get(url, headers=headers)
    
    # Ensure valid response and handle errors
    if response.status_code == 200:
        return response.json().get('syllabus_body', 'No syllabus found.')
    else:
        print(f"Error fetching syllabus: {response.status_code}")
        return 'No syllabus found.'

# Function to get assignments for a course, including metadata
def get_assignments(course_id):
    url = f"https://canvas.instructure.com/api/v1/courses/{course_id}/assignments"
    response = requests.get(url, headers=headers)
    
    # Ensure valid response and handle errors
    if response.status_code == 200:
        assignments = response.json()
        assignment_list = [
            f"Assignment: {assignment['name']} - Due: {assignment.get('due_at', 'No due date provided')} - Instructions: {assignment.get('description', 'No instructions provided')}"
            for assignment in assignments
        ]
        return '\n'.join(assignment_list)
    else:
        return f"Error fetching assignments: {response.status_code}"

# Function to get course files (e.g., PDFs)
def get_course_files(course_id):
    url = f"https://canvas.instructure.com/api/v1/courses/{course_id}/files"
    response = requests.get(url, headers=headers)
    
    # Ensure valid response and handle errors
    if response.status_code == 200:
        files = response.json()
        file_list = [f"File: {file['display_name']} - Download URL: {file['url']}" for file in files]
        return '\n'.join(file_list)
    else:
        return f"Error fetching course files: {response.status_code}"

# Combine both to check for syllabus in the section or in files
def get_syllabus_or_file(course_id):
    # First, check the syllabus section
    syllabus = get_syllabus(course_id)
    
    if syllabus and syllabus != 'No syllabus found.':
        return f"Here is the syllabus: {syllabus}"
    
    # If no syllabus in the section, check for syllabus file (e.g., PDFs)
    syllabus_file_url = get_course_files(course_id)
    if syllabus_file_url != 'No syllabus file found.':
        return f"Here is the syllabus file: {syllabus_file_url}"
    
    return "Sorry, no syllabus found in the course."

# Example usage
courses = get_courses()

# Loop through the courses and handle restricted courses and metadata
for course in courses:
    if isinstance(course, dict):  # Ensure course is a dictionary
        if 'access_restricted_by_date' in course and course['access_restricted_by_date']:
            print(f"Course ID: {course['id']} is restricted by date. Attempting to retrieve basic info.")
            
            # Attempt to retrieve restricted content: Assignments, Metadata
            course_id = course.get('id')
            print(f"Assignments for restricted course {course_id}:\n{get_assignments(course_id)}")
            print(f"Files for restricted course {course_id}:\n{get_course_files(course_id)}")
        else:
            name = course.get('name', 'No name available')
            course_id = course.get('id', 'No ID available')
            print(f"Course Name: {name}, Course ID: {course_id}")
            
            # Attempt to retrieve syllabus and assignments
            print(f"Syllabus for course {course_id}:\n{get_syllabus_or_file(course_id)}")
            print(f"Assignments for course {course_id}:\n{get_assignments(course_id)}")
            print(f"Files for course {course_id}:\n{get_course_files(course_id)}")
    else:
        print(f"Unexpected course format: {course}")

