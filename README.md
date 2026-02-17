🌟OVERVIEW

The University Course & Enrollment Management System is a console-based Python application that:

📚 Manages university courses

🔗 Handles prerequisite relationships

🚫 Prevents circular dependencies

✅ Checks student enrollment eligibility

🧠 Demonstrates real-world graph traversal (DFS)

This project models courses as a Directed Graph and uses Depth First Search (DFS) for dependency management.

TECHNICAL DESIGN

Graph Representation

> Each course is represented as a node

> Each prerequisite is represented as a directed edge

> The system maintains a Directed Acyclic Graph (DAG)

Data structures used:

courses = {}          # course_id → course_name

prerequisites = {}    # course_id → set of prerequisite_ids


Using dictionaries and sets ensures:

> O(1) average lookup time

> Efficient dependency traversal

> No duplicate prerequisites

CORE ALGORITHMS

1. Cycle Detection (Iterative DFS)
Before adding a prerequisite, the system performs an iterative DFS traversal to ensure no circular dependency is introduced.

Time Complexity:

O(V + E)

Where:

V = number of courses

E = number of prerequisite relationships

This ensures the graph always remains acyclic.

2. Prerequisite Expansion

The system computes the full dependency chain (direct + indirect prerequisites) using DFS traversal.
Example:

CS301 → CS201 → CS101

Calling:

list_prerequisites("CS301")

Returns:

["CS101", "CS201"]

3. Enrollment Validation
Enrollment eligibility is verified by:

> Expanding the full prerequisite chain

> Checking membership using a set for O(1) lookups

> all(prereq in completed_set for prereq in required_prereqs)


🛡 Defensive Programming Highlights

✔ Prevents empty inputs

✔ Prevents duplicate courses

✔ Limits maximum courses (1000)

✔ Limits prerequisites per course (10)

✔ Prevents circular dependencies

✔ Handles invalid menu selections

✔ Handles type safety checks



🔮 FUTURE IMPROVEMENTS

🌐 Web-based interface (Flask/Django)

💾 Persistent storage (Database/File system)

📊 Visual graph representation

👨‍🎓 Student profile management

📑 Topological sorting for course order

🔐 Authentication system
