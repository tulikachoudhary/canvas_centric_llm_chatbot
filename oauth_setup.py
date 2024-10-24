import requests

# Your personal access token
access_token = "11299~7r3vXW4xyUeJVuh4EnLhwnP4KYy3DBPhfPrmm6DmHn2MEu33LWCQ4D4TmaJ9cA7D"
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
        return {'error': f"Error fetching courses: {response.status_code}"}

# Function to get the syllabus for a course
def get_syllabus(course_id):
    url = f"https://canvas.instructure.com/api/v1/courses/{course_id}?include=syllabus_body"
    response = requests.get(url, headers=headers)
    
    # Ensure valid response and handle errors
    if response.status_code == 200:
        return response.json().get('syllabus_body', 'No syllabus found.')
    else:
        return f"Error fetching syllabus: {response.status_code}"

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

# Function to handle course information retrieval and return data
def handle_courses():
    courses = get_courses()

    if isinstance(courses, dict) and 'error' in courses:
        return courses['error']
    
    result = []
    
    for course in courses:
        if isinstance(course, dict):  # Ensure course is a dictionary
            name = course.get('name', None)
            course_id = course.get('id', None)
            
            # Skip the course if either the name or the course_id is missing
            if not name or not course_id:
                continue  # Move to the next course

            course_data = {'Course Name': name, 'Course ID': course_id}
            
            if 'access_restricted_by_date' in course and course['access_restricted_by_date']:
                course_data['Restricted'] = True
                course_data['Assignments'] = get_assignments(course_id)
                course_data['Files'] = get_course_files(course_id)
            else:
                course_data['Restricted'] = False
                course_data['Syllabus'] = get_syllabus_or_file(course_id)
                course_data['Assignments'] = get_assignments(course_id)
                course_data['Files'] = get_course_files(course_id)
            
            result.append(course_data)
        else:
            result.append({'error': 'Unexpected course format'})

    return result

# Example usage
courses_data = handle_courses()

# If you want to use `courses_data` further, you can print or log it
# For example, you can return it from a web API or log it to a file
