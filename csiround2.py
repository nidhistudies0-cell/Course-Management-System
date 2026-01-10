courses = {}  # Keeps a track of all the registered courses
prerequisites = {}  # Keeps a track of which courses to complete before taking another course(course_id : set of prerequisites)

def add_course(course_id, name): #Function definition to add a new course to the system
    if not course_id or not name: #Makes sure that course id and name are provided as input
        return "Error: Course ID and Name cannot be empty"
    if course_id in courses:      #Prevents adding duplicate courses
        return f"Error: Course {course_id} already exists"
    if len(courses) >= 1000:
        return "Error: Maximum number of courses (1000) reached"

    courses[course_id] = name      #Adds the course id with course name
    prerequisites[course_id] = set()    #Creates an empty set to store the course prerequisites.
    return f"Success: Course {course_id} ({name}) added."

def add_prerequisite(course_id, prerequisite_id):  #Links one course as prerequisite for another.
    if course_id not in courses:
        return f"Error: Course {course_id} does not exist"
    if prerequisite_id not in courses:
        return f"Error: Prerequisite course {prerequisite_id} does not exist"
    if course_id == prerequisite_id:
        return "Error: A course cannot be its own prerequisite"

    # Iterative cycle check for performance/safety
    if creates_cycle(course_id, prerequisite_id):
        return "Error: This would create a circular dependency (cycle)."

    if len(prerequisites[course_id]) >= 10:
        return f"Error: Course {course_id} already has maximum prerequisites (10)"

    prerequisites[course_id].add(prerequisite_id)
    return f"Success: {prerequisite_id} is now a prerequisite for {course_id}."

def creates_cycle(course_id, new_prerequisite_id): #Checks whether adding a course as a prerequisite to another can lead back to that course creating a cycle
    '''A circular dependency (cycle) happens when courses depend on each other in a loop.
    For example,
    To take CS101, you must finish CS301
    To finish CS301, you must finish CS201
    To finish CS201, you must finish CS101
    > Impossible to start any course
    So before adding a prerequisite, we must check for cycles'''
    stack = [new_prerequisite_id]   #Stores the courses that we need to check
    visited = {new_prerequisite_id}  #Stores the courses already checked to prevent infinite loops
    while stack:
        current = stack.pop()      #Take one course at a time
        current_prereqs = prerequisites.get(current, set())   #Get the courses that the prerequisite depends upon
        for prereq in current_prereqs:
            if prereq == course_id:    #Checks all the dependencies to avoid a cycle
                return True
            if prereq not in visited:   # Add it to visited
                visited.add(prereq)
                stack.append(prereq)    #Check further to explore dependency of the prerequisite on the given course
    return False

def remove_course(course_id):
    if course_id not in courses:
        return f"Error: Course {course_id} does not exist"
    
    del courses[course_id]
    del prerequisites[course_id]
    for prereq_set in prerequisites.values():
        prereq_set.discard(course_id)            #Discard the course as a prerequisite for other courses.
    return f"Success: Course {course_id} removed."

def list_prerequisites(course_id):
    #Returns the full chain of prerequisites (direct and indirect).
    if course_id not in courses:
        return f"Error: Course {course_id} does not exist"

    all_prereqs = set()
    stack = [course_id]
    visited = {course_id}
    while stack:
        current = stack.pop()
        for prereq in prerequisites.get(current, set()):
            if prereq not in visited:
                all_prereqs.add(prereq)
                visited.add(prereq)
                stack.append(prereq)
                
    return sorted(list(all_prereqs))

def can_enroll(course_id, completed_courses):
    """
    Check if a student can enroll in a course.
    Verifies if all courses in the dependency chain are completed.
    """
    if course_id not in courses:
        return False

    required_prereqs = list_prerequisites(course_id)
    
    # Handle the case where list_prerequisites returns an error string in case an invalid course is returned to list_prerequisites
    if isinstance(required_prereqs, str):
        return False

    completed_set = set(completed_courses)

    # All prerequisites (the whole chain) must be in the completed set
    return all(prereq in completed_set for prereq in required_prereqs)

# --- INTERACTIVE INTERFACE ---

def main():
    print("=== University Course & Enrollment System ===")
    
    while True:
        print("\n--- Menu ---")
        print("1. Add Course")
        print("2. Add Prerequisite")
        print("3. Remove Course")
        print("4. List Prerequisite Chain")
        print("5. View All Courses")
        print("6. Check Enrollment Eligibility")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            cid = input("Enter Course ID (e.g., CS101): ").strip().upper()
            name = input("Enter Course Name: ").strip()
            print(add_course(cid, name))

        elif choice == "2":
            cid = input("Enter Target Course ID: ").strip().upper()
            pid = input("Enter Prerequisite Course ID: ").strip().upper()
            print(add_prerequisite(cid, pid))

        elif choice == "3":
            cid = input("Enter Course ID to remove: ").strip().upper()
            print(remove_course(cid))

        elif choice == "4":
            cid = input("Enter Course ID to check: ").strip().upper()
            prereqs = list_prerequisites(cid)
            if isinstance(prereqs, list):
                print(f"Full chain for {cid}: {', '.join(prereqs) if prereqs else 'None'}")
            else:
                print(prereqs)

        elif choice == "5":
            if not courses:
                print("No courses available.")
            else:
                for cid, name in courses.items():
                    direct = prerequisites.get(cid, set())
                    print(f"- {cid}: {name} (Direct: {', '.join(direct) if direct else 'None'})")

        elif choice == "6":
            cid = input("Which course do you want to take? ").strip().upper()
            completed_input = input("Enter your completed courses (separated by commas): ").strip().upper()
            # Convert string input "CS101, CS201" into a list ["CS101", "CS201"]
            completed_list = [c.strip() for c in completed_input.split(",") if c.strip()]
            
            if can_enroll(cid, completed_list):
                print(f"SUCCESS: You have met all requirements for {cid}.")
            else:
                missing = [p for p in list_prerequisites(cid) if p not in completed_list]
                print(f"DENIED: You are missing prerequisites for {cid}: {', '.join(missing)}")

        elif choice == "7":
            print("EXITING. Thank you for using the Course Management System!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()