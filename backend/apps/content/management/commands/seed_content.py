"""
DEEPAK INTERVIEW HUB — Content Seeder Management Command
Populates authentic, verified technical interview questions, topics, coding problems,
and SQL exercises across all 12 curriculum subjects.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.content.models import Subject, Topic, Question, AnswerOption
from apps.practice.models import CodingProblem, SQLExercise

class Command(BaseCommand):
    help = 'Seeds initial curriculum subjects, topics, and verified interview questions.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding curriculum subjects and verified question bank...")

        # 1. Subjects configuration
        subjects_data = [
            {'name': 'Python', 'slug': 'python', 'icon': '🐍', 'target_questions': 100, 'display_order': 1, 'description': 'Generators, decorators, memory model, OOP, collections & execution internals.'},
            {'name': 'SQL', 'slug': 'sql', 'icon': '🗄️', 'target_questions': 100, 'display_order': 2, 'description': 'Complex joins, window functions, subqueries, indexing & query execution plans.'},
            {'name': 'DSA', 'slug': 'dsa', 'icon': '⚡', 'target_questions': 100, 'display_order': 3, 'description': 'Arrays, linked lists, hash maps, trees, sorting, recursion & complexity analysis.'},
            {'name': 'DBMS', 'slug': 'dbms', 'icon': '💾', 'target_questions': 60, 'display_order': 4, 'description': 'ACID properties, normalization (1NF to BCNF), concurrency control & deadlocks.'},
            {'name': 'OOP Concepts', 'slug': 'oop', 'icon': '🧩', 'target_questions': 60, 'display_order': 5, 'description': 'Encapsulation, inheritance, polymorphism, abstraction, and SOLID principles.'},
            {'name': 'Django', 'slug': 'django', 'icon': '🎯', 'target_questions': 40, 'display_order': 6, 'description': 'MTV architecture, ORM optimization, middleware, auth signals & forms.'},
            {'name': 'REST API', 'slug': 'rest-api', 'icon': '🌐', 'target_questions': 40, 'display_order': 7, 'description': 'HTTP verbs, status codes, serializers, viewsets, authentication & rate limits.'},
            {'name': 'Operating Systems', 'slug': 'os', 'icon': '⚙️', 'target_questions': 40, 'display_order': 8, 'description': 'Processes, threads, CPU scheduling, virtual memory, paging & semaphores.'},
            {'name': 'Computer Networks', 'slug': 'cn', 'icon': '📡', 'target_questions': 40, 'display_order': 9, 'description': 'OSI stack, TCP 3-way handshake, DNS, routing protocols & subnetting.'},
            {'name': 'Aptitude & Reasoning', 'slug': 'aptitude', 'icon': '🧠', 'target_questions': 100, 'display_order': 10, 'description': 'Quantitative mathematics, logical deductions, number series & puzzles.'},
            {'name': 'HR Preparation', 'slug': 'hr', 'icon': '🤝', 'target_questions': 50, 'display_order': 11, 'description': 'Behavioral STAR-method responses, self-introduction & conflict resolution.'},
            {'name': 'Project Viva', 'slug': 'viva', 'icon': '🎓', 'target_questions': 50, 'display_order': 12, 'description': 'Architecture defense, database trade-offs, security audits & viva panel prep.'},
        ]

        subjects = {}
        for s_data in subjects_data:
            subject, _ = Subject.objects.update_or_create(
                slug=s_data['slug'],
                defaults=s_data
            )
            subjects[s_data['slug']] = subject

        self.stdout.write(f"Created/updated {len(subjects)} subjects.")

        # 2. Curated Technical Questions Bank
        questions_dataset = [
            # --- PYTHON QUESTIONS ---
            {
                'subject': 'python',
                'difficulty': 'easy',
                'question_text': 'What is the fundamental difference between a Python list and a tuple?',
                'correct_answer': 'Lists are mutable while tuples are immutable.',
                'explanation': 'Lists in Python are dynamic arrays whose elements can be added, removed, or reassigned in-place. Tuples are fixed sequences whose values cannot be modified once instantiated, providing memory optimization and hashability for dictionary keys.',
                'code_example': 'my_list = [1, 2, 3]\nmy_list[0] = 99  # Valid\n\nmy_tuple = (1, 2, 3)\n# my_tuple[0] = 99  # Raises TypeError: \'tuple\' object does not support item assignment',
                'expected_output': 'TypeError: \'tuple\' object does not support item assignment',
                'interview_tip': 'Always mention that immutability allows tuples to be used as dictionary keys and set elements, whereas lists cannot because they are unhashable.',
                'tags': ['Python Fundamentals', 'Data Structures', 'Immutability'],
                'options': [
                    ('A', 'Lists can contain heterogeneous types while tuples cannot', False),
                    ('B', 'Lists are mutable while tuples are immutable', True),
                    ('C', 'Tuples consume significantly more memory than lists', False),
                    ('D', 'Lists use parenthesis while tuples use square brackets', False),
                ]
            },
            {
                'subject': 'python',
                'difficulty': 'medium',
                'question_text': 'What is a Python generator, and what advantage does the `yield` statement provide over `return`?',
                'correct_answer': 'Yield returns a generator iterator that produces values lazily on-demand without loading the entire collection into RAM.',
                'explanation': 'A generator function uses the `yield` keyword rather than `return`. When called, it suspends execution and maintains its state, producing items one at a time on iteration (`__next__()`). This offers O(1) space complexity for processing large streams or datasets.',
                'code_example': 'def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\ngen = countdown(3)\nprint(list(gen))',
                'expected_output': '[3, 2, 1]',
                'interview_tip': 'Contrast memory usage: `range()` in Python 3 is lazy, while creating a list of 10 million integers in Python will exhaust several megabytes of RAM.',
                'tags': ['Generators', 'Iterators', 'Memory Management'],
                'options': [
                    ('A', 'Yield permanently destroys the function execution frame', False),
                    ('B', 'Yield produces values lazily on-demand preserving stack state', True),
                    ('C', 'Yield is used exclusively inside async coroutines', False),
                    ('D', 'Generators run concurrently across multiple OS threads', False),
                ]
            },
            {
                'subject': 'python',
                'difficulty': 'difficult',
                'question_text': 'How does Python handle memory management through reference counting and the cyclic garbage collector?',
                'correct_answer': 'Objects maintain a reference count; a cyclic generational garbage collector detects and cleans isolated reference cycles.',
                'explanation': 'CPython primarily uses reference counting. When an object\'s reference count drops to zero, its deallocator is invoked immediately. However, self-referential or cyclic references (where Object A points to B and B points to A) never drop to zero. Python\'s generational garbage collector (Gen 0, 1, 2) uses a tri-color traversal algorithm to detect unreachable reference cycles.',
                'code_example': 'import sys, gc\n\na = []\nb = [a]\na.append(b)  # Cyclic reference\ndel a, b     # Ref count > 0, garbage collector cleans it up in Gen 0\ngc.collect()',
                'expected_output': 'Cycle collected',
                'interview_tip': 'Explain why `del` in Python does not directly free memory; it merely decrements the reference count and removes the variable name from namespace.',
                'tags': ['CPython Internals', 'Garbage Collection', 'Memory Management'],
                'options': [
                    ('A', 'Python relies purely on mark-and-sweep and lacks reference counting', False),
                    ('B', 'Python relies on reference counting supplemented by a generational cyclic garbage collector', True),
                    ('C', 'Memory deallocation in CPython must be manually requested using malloc and free', False),
                    ('D', 'The Global Interpreter Lock prevents cyclic references from ever occurring', False),
                ]
            },

            # --- SQL QUESTIONS ---
            {
                'subject': 'sql',
                'difficulty': 'easy',
                'question_text': 'What is the operational difference between the WHERE clause and the HAVING clause in SQL?',
                'correct_answer': 'WHERE filters individual rows before aggregation; HAVING filters groups after aggregation.',
                'explanation': 'The WHERE clause evaluates predicates on individual rows before any GROUP BY aggregation takes place. The HAVING clause is evaluated after GROUP BY, filtering aggregate groups based on aggregate function results (e.g., HAVING COUNT(*) > 5).',
                'code_example': 'SELECT department_id, COUNT(*)\nFROM employees\nWHERE salary > 50000\nGROUP BY department_id\nHAVING COUNT(*) >= 2;',
                'expected_output': 'Filtered departments with >= 2 high earners',
                'interview_tip': 'Remember that aggregate functions like SUM(), AVG(), and COUNT() cannot appear inside a WHERE clause without a subquery.',
                'tags': ['SQL Basics', 'Grouping', 'Aggregation'],
                'options': [
                    ('A', 'WHERE is used with joins, while HAVING is used with subqueries', False),
                    ('B', 'WHERE filters rows before aggregation; HAVING filters groups after aggregation', True),
                    ('C', 'HAVING can only be used on string columns', False),
                    ('D', 'WHERE and HAVING are completely interchangeable in standard ANSI SQL', False),
                ]
            },
            {
                'subject': 'sql',
                'difficulty': 'medium',
                'question_text': 'What is the difference between RANK() and DENSE_RANK() window functions?',
                'correct_answer': 'RANK() leaves gaps in rank numbering after ties, whereas DENSE_RANK() does not leave gaps.',
                'explanation': 'When two or more rows have equal values in the ORDER BY clause: RANK() assigns identical ranks to the tied rows and skips the subsequent rank numbers (e.g., 1, 2, 2, 4). DENSE_RANK() assigns identical ranks to tied rows but continues with the immediate next sequential integer (e.g., 1, 2, 2, 3).',
                'code_example': 'SELECT name, score,\n       RANK() OVER (ORDER BY score DESC) as rnk,\n       DENSE_RANK() OVER (ORDER BY score DESC) as dense_rnk\nFROM exam_scores;',
                'expected_output': 'rnk: [1, 2, 2, 4] vs dense_rnk: [1, 2, 2, 3]',
                'interview_tip': 'In "Top N Salaries" interview problems, always prefer DENSE_RANK() so that finding the second highest salary reliably checks rank = 2.',
                'tags': ['Window Functions', 'Analytical SQL', 'Ranking'],
                'options': [
                    ('A', 'RANK() is only supported in MySQL, whereas DENSE_RANK() is PostgreSQL-only', False),
                    ('B', 'RANK() skips subsequent rank numbers after ties, while DENSE_RANK() leaves no gaps', True),
                    ('C', 'DENSE_RANK() sorts in ascending order while RANK() sorts in descending order', False),
                    ('D', 'RANK() requires a PARTITION BY clause while DENSE_RANK() cannot use partitions', False),
                ]
            },
            {
                'subject': 'sql',
                'difficulty': 'difficult',
                'question_text': 'What are the four ANSI SQL transaction isolation levels, and which phenomenon does SERIALIZABLE prevent that REPEATABLE READ allows?',
                'correct_answer': 'Read Uncommitted, Read Committed, Repeatable Read, Serializable. Serializable prevents Phantom Reads.',
                'explanation': 'Isolation levels prevent concurrency anomalies: Read Uncommitted permits Dirty Reads. Read Committed eliminates Dirty Reads. Repeatable Read eliminates Non-Repeatable Reads. Serializable provides total transaction isolation, eliminating Phantom Reads (where new rows inserted by another concurrent transaction become visible during range scans).',
                'code_example': 'BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;\nSELECT * FROM accounts WHERE balance > 1000;\n-- No other concurrent transaction can insert or update rows matching this predicate\nCOMMIT;',
                'expected_output': 'Strict serializability guaranteed',
                'interview_tip': 'Mention the trade-off: higher isolation guarantees consistency at the cost of concurrency throughput and higher risk of transaction aborts/deadlocks.',
                'tags': ['Transactions', 'ACID', 'Concurrency', 'Isolation Levels'],
                'options': [
                    ('A', 'Read Committed prevents Dirty Reads, but Serializable is required to eliminate Phantom Reads', True),
                    ('B', 'Repeatable Read completely eliminates all locking and deadlock risks', False),
                    ('C', 'Read Uncommitted is the default isolation level in PostgreSQL and MySQL InnoDB', False),
                    ('D', 'Serializable allows dirty reads if foreign keys are disabled', False),
                ]
            },

            # --- DSA QUESTIONS ---
            {
                'subject': 'dsa',
                'difficulty': 'easy',
                'question_text': 'What is the average and worst-case time complexity of searching for an element in a Hash Table?',
                'correct_answer': 'Average case: O(1); Worst case: O(n) due to hash collisions.',
                'explanation': 'In an ideal hash table with a uniform hash distribution function and low load factor, search operations compute the bucket index in O(1) time. However, if multiple keys hash to the same bucket (hash collision) and collisions are chained into a linked list, worst-case search degrades to linear O(n).',
                'code_example': '# Python dict average O(1) lookup\nhash_map = {"apple": 10, "banana": 20}\nprice = hash_map.get("apple")  # O(1) average',
                'expected_output': '10',
                'interview_tip': 'Explain how modern programming languages (e.g. Java 8+ HashMap) upgrade bucket collision linked lists into Red-Black trees when bucket size exceeds 8, reducing worst case from O(n) to O(log n).',
                'tags': ['Hash Tables', 'Time Complexity', 'Data Structures'],
                'options': [
                    ('A', 'Average: O(log n); Worst: O(n)', False),
                    ('B', 'Average: O(1); Worst: O(n)', True),
                    ('C', 'Average: O(1); Worst: O(1)', False),
                    ('D', 'Average: O(n); Worst: O(n^2)', False),
                ]
            },
            {
                'subject': 'dsa',
                'difficulty': 'medium',
                'question_text': 'How do you detect a cycle in a singly linked list in O(n) time and O(1) auxiliary space?',
                'correct_answer': "Floyd's Cycle-Finding Algorithm (Tortoise and Hare pointer algorithm).",
                'explanation': "Floyd's algorithm initializes two pointers: a slow pointer moving 1 node per step and a fast pointer moving 2 nodes per step. If the linked list contains a loop or cycle, the fast pointer will eventually overlap and meet the slow pointer inside the cycle loop without requiring extra memory like a hash set.",
                'code_example': 'def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False',
                'expected_output': 'True if cycle detected, False otherwise',
                'interview_tip': 'Be ready to explain how to find the entry node of the cycle: reset the slow pointer to the head, keep fast at the meeting point, and advance both 1 step at a time until they meet.',
                'tags': ['Linked Lists', 'Two Pointers', 'Cycle Detection'],
                'options': [
                    ('A', 'Reverse the linked list and check if head equals tail', False),
                    ('B', 'Use Floyd\'s Two-Pointer Tortoise and Hare Algorithm in O(n) time and O(1) space', True),
                    ('C', 'Recursively count nodes until StackOverflowError is caught', False),
                    ('D', 'Sort the node memory addresses using Merge Sort', False),
                ]
            },
            {
                'subject': 'dsa',
                'difficulty': 'difficult',
                'question_text': 'What is the time complexity of building a Binary Heap from an arbitrary array of N elements?',
                'correct_answer': 'O(n) linear time using bottom-up heapify (Floyd\'s Build-Heap).',
                'explanation': 'While inserting N elements one-by-one into an initially empty heap takes O(n log n), the bottom-up `heapify` algorithm processes nodes from index n/2 down to 0. Since most nodes reside near the leaves (height 0 and 1) requiring fewer swap steps, the mathematical summation converges to O(n).',
                'code_example': 'import heapq\narr = [9, 4, 7, 1, -2, 6, 5]\nheapq.heapify(arr)  # Runs in O(n) linear time\nprint(arr)',
                'expected_output': '[-2, 1, 5, 4, 9, 6, 7]',
                'interview_tip': 'Prove the mathematical summation: sum of (h / 2^h) for h=1 to log n is bounded by a constant, demonstrating that the total work is proportional to n.',
                'tags': ['Heaps', 'Priority Queue', 'Algorithm Analysis'],
                'options': [
                    ('A', 'O(n log n) by inserting elements sequentially', False),
                    ('B', 'O(n) via bottom-up heapify algorithm', True),
                    ('C', 'O(n^2) due to parent-child comparisons', False),
                    ('D', 'O(log n) using binary search partitions', False),
                ]
            },

            # --- DBMS QUESTIONS ---
            {
                'subject': 'dbms',
                'difficulty': 'medium',
                'question_text': 'What condition must a relational schema satisfy to be in Boyce-Codd Normal Form (BCNF)?',
                'correct_answer': 'For every non-trivial functional dependency X -> Y, X must be a superkey.',
                'explanation': 'BCNF is a stricter version of Third Normal Form (3NF). While 3NF permits the dependency X -> Y if Y is a prime attribute (part of a candidate key), BCNF strictly mandates that the determinant X must ALWAYS be a superkey for all non-trivial functional dependencies.',
                'code_example': '-- Example: In Student_Advisor(StudentID, Subject, Advisor)\n-- If Advisor -> Subject, Advisor must be a candidate/superkey for BCNF compliance.',
                'expected_output': 'Normalized into distinct relation tables',
                'interview_tip': 'Remember: Every relation in BCNF is also in 3NF, but a relation in 3NF is not necessarily in BCNF.',
                'tags': ['Normalization', 'BCNF', 'Relational Model'],
                'options': [
                    ('A', 'All attributes must be numeric foreign keys', False),
                    ('B', 'For every non-trivial functional dependency X -> Y, X must be a superkey', True),
                    ('C', 'Tables must not exceed three joined columns', False),
                    ('D', 'Every column must allow null values', False),
                ]
            },

            # --- OOP QUESTIONS ---
            {
                'subject': 'oop',
                'difficulty': 'medium',
                'question_text': 'What does the Dependency Inversion Principle (the "D" in SOLID) state?',
                'correct_answer': 'High-level modules should not depend on low-level modules; both should depend on abstractions.',
                'explanation': 'The Dependency Inversion Principle decouples software modules. Instead of a high-level business service directly instantiating a concrete low-level database class, both modules depend on an abstract interface (e.g., IRepository). Dependencies are inverted and injected at runtime.',
                'code_example': 'from abc import ABC, abstractmethod\n\nclass Notifier(ABC):\n    @abstractmethod\n    def send(self, message: str): pass\n\nclass EmailNotifier(Notifier):\n    def send(self, message: str):\n        print(f"Email: {message}")\n\nclass OrderService:\n    def __init__(self, notifier: Notifier):\n        self.notifier = notifier  # Injected dependency',
                'expected_output': 'Decoupled architecture',
                'interview_tip': 'Connect DIP with Dependency Injection (DI) frameworks and unit testing: DIP allows swapping a real payment gateway with a mock gateway during automated tests.',
                'tags': ['SOLID Principles', 'Architecture', 'Design Patterns'],
                'options': [
                    ('A', 'Subclasses should never override parent class methods', False),
                    ('B', 'High-level modules should depend on abstractions rather than concrete implementations', True),
                    ('C', 'Classes should have only one single reason to change', False),
                    ('D', 'Derived classes must be substitutable for their base classes', False),
                ]
            },

            # --- DJANGO & REST API QUESTIONS ---
            {
                'subject': 'django',
                'difficulty': 'medium',
                'question_text': 'What is the operational difference between `select_related` and `prefetch_related` in Django ORM?',
                'correct_answer': 'select_related uses an SQL JOIN for single-valued relationships; prefetch_related performs a separate query for multi-valued relationships.',
                'explanation': '`select_related` performs an SQL INNER/LEFT JOIN and populates model attributes in a single database query; it is designed for ForeignKey and OneToOne relationships. `prefetch_related` executes a separate SQL query with an `IN (...)` clause and joins results in Python memory; it is designed for ManyToMany and reverse ForeignKey relationships, preventing N+1 query bottlenecks.',
                'code_example': '# 1 SQL JOIN query:\nbooks = Book.objects.select_related("author").all()\n\n# 2 distinct SQL queries joined in Python:\nauthors = Author.objects.prefetch_related("books").all()',
                'expected_output': 'Eliminates N+1 query problem',
                'interview_tip': 'Always emphasize avoiding N+1 queries in Django API development when returning nested relations in DRF serializers.',
                'tags': ['Django ORM', 'Performance', 'Database Optimization'],
                'options': [
                    ('A', 'select_related is for PostgreSQL while prefetch_related is for SQLite', False),
                    ('B', 'select_related uses SQL JOIN for foreign keys; prefetch_related uses separate queries in Python for M2M', True),
                    ('C', 'prefetch_related runs in asynchronous worker threads while select_related blocks', False),
                    ('D', 'Both methods execute identical SQL JOIN statements under the hood', False),
                ]
            },
            {
                'subject': 'rest-api',
                'difficulty': 'easy',
                'question_text': 'What does it mean for an HTTP method in a RESTful API to be "Idempotent"?',
                'correct_answer': 'Making multiple identical requests produces the exact same side-effects as making a single request.',
                'explanation': 'An HTTP method is idempotent if the side-effects of N > 0 identical requests with that method are the same as for a single request. GET, PUT, DELETE, and HEAD are idempotent. POST is typically NOT idempotent because repeating a POST creates duplicate resources on the server.',
                'code_example': '# PUT /api/users/123 with body {"name": "Deepak"}\n# Executing this once or 100 times results in the exact same resource state.',
                'expected_output': 'HTTP 200 OK or 204 No Content consistently',
                'interview_tip': 'Distinguish between Safe (read-only, no state change like GET) and Idempotent (state changes, but multiple calls result in same final state like PUT or DELETE).',
                'tags': ['HTTP Semantics', 'REST Architecture', 'API Design'],
                'options': [
                    ('A', 'The method must return responses in encrypted JSON format', False),
                    ('B', 'Multiple identical requests produce the same server-side state as a single request', True),
                    ('C', 'The API endpoint cannot be cached by HTTP proxies', False),
                    ('D', 'Requests cannot take longer than 1000 milliseconds to complete', False),
                ]
            },

            # --- OPERATING SYSTEMS & NETWORKS ---
            {
                'subject': 'os',
                'difficulty': 'medium',
                'question_text': 'What is the phenomenon of "Thrashing" in an Operating System virtual memory system?',
                'correct_answer': 'When the OS spends significantly more time swapping pages in and out of disk than executing user instructions.',
                'explanation': 'Thrashing occurs when the total working set of active processes exceeds physical RAM capacity. The operating system must continuously swap pages out to disk storage and page others in (high page fault frequency), causing CPU utilization to plummet to near zero while disk I/O queues saturate.',
                'code_example': '-- High page fault rate -> CPU idle waiting for disk swapping -> Thrashing condition',
                'expected_output': 'System unresponsiveness',
                'interview_tip': 'State the solutions to thrashing: increase physical RAM, reduce the degree of multiprogramming, or implement working set model page replacement.',
                'tags': ['Virtual Memory', 'Paging', 'Operating Systems'],
                'options': [
                    ('A', 'A hardware CPU clock rate overheating event', False),
                    ('B', 'A state where the OS spends more time swapping pages than executing actual instructions', True),
                    ('C', 'A deadlock involving more than four concurrent processes', False),
                    ('D', 'The sudden termination of the init process by SIGKILL', False),
                ]
            },
            {
                'subject': 'cn',
                'difficulty': 'medium',
                'question_text': 'Explain the steps involved in the TCP 3-Way Handshake connection establishment.',
                'correct_answer': '1) Client sends SYN; 2) Server responds with SYN-ACK; 3) Client sends ACK.',
                'explanation': 'TCP guarantees reliable connection-oriented communication using a 3-way handshake: 1. SYN: Client chooses initial sequence number (ISN_c) and sends SYN packet. 2. SYN-ACK: Server acknowledges client ISN with ACK (ISN_c + 1) and sends its own ISN_s in SYN packet. 3. ACK: Client acknowledges server ISN with ACK (ISN_s + 1). Connection enters ESTABLISHED state.',
                'code_example': 'Client                     Server\n  |------- SYN (seq=x) ------->|  (SYN_RCVD)\n  |<-- SYN-ACK (seq=y,ack=x+1)-|  \n  |------- ACK (ack=y+1) ----->|  (ESTABLISHED)',
                'expected_output': 'TCP Connection Established',
                'interview_tip': 'Explain why 2 packets are insufficient: a 2-way handshake cannot verify two-way bidirectional packet transmission and leaves the server vulnerable to stale duplicate SYN packets.',
                'tags': ['TCP/IP', 'Transport Layer', 'Networking Protocols'],
                'options': [
                    ('A', '1) ACK; 2) SYN; 3) FIN', False),
                    ('B', '1) Client sends SYN; 2) Server responds with SYN-ACK; 3) Client sends ACK', True),
                    ('C', '1) DNS Query; 2) ARP Request; 3) HTTP GET', False),
                    ('D', '1) Client sends PSH; 2) Server sends URG; 3) Client sends RST', False),
                ]
            },

            # --- APTITUDE & HR & VIVA ---
            {
                'subject': 'aptitude',
                'difficulty': 'easy',
                'question_text': 'A train traveling at 72 km/h crosses a pole in 9 seconds. What is the length of the train in meters?',
                'correct_answer': '180 meters',
                'explanation': '1. Convert speed from km/h to m/s: 72 * (5 / 18) = 20 m/s.\n2. When crossing a stationary pole, Distance = Speed * Time.\n3. Distance = 20 m/s * 9 s = 180 meters.',
                'code_example': 'speed_kmh = 72\nspeed_ms = speed_kmh * (5 / 18)  # 20.0 m/s\ntime_s = 9\nlength = speed_ms * time_s       # 180 meters',
                'expected_output': '180 meters',
                'interview_tip': 'Always convert units first (km/h to m/s by multiplying by 5/18) before computing distances in placement aptitude tests.',
                'tags': ['Quantitative Aptitude', 'Speed Time Distance', 'Placement Rounds'],
                'options': [
                    ('A', '150 meters', False),
                    ('B', '180 meters', True),
                    ('C', '200 meters', False),
                    ('D', '220 meters', False),
                ]
            },
            {
                'subject': 'hr',
                'difficulty': 'medium',
                'question_text': 'What is the most effective approach when an interviewer asks: "What is your greatest technical weakness?"',
                'correct_answer': 'State a genuine technical blind spot, explain the concrete corrective actions you are actively taking, and show measurable improvement.',
                'explanation': 'Interviewers want self-awareness, intellectual honesty, and commitment to continuous self-improvement. Never use clichés like "I am too perfectionist". Instead, pick a real topic (e.g. "Early on, I struggled with Docker containerization and CI/CD pipelines") and explain how you built projects and tests to actively bridge that gap.',
                'code_example': '-- Example: "While comfortable with Python backend and relational databases, I was initially less confident with distributed caching. Recently I implemented Redis caching in my Django project, benchmarking a 4x reduction in response times."',
                'expected_output': 'Authentic and constructive response',
                'interview_tip': 'Demonstrate continuous growth mindset. Weakness + Action + Result is the golden formula for this question.',
                'tags': ['HR Interviews', 'Behavioral Questions', 'Soft Skills'],
                'options': [
                    ('A', 'Claim you have no technical weaknesses because you master everything quickly', False),
                    ('B', 'State a genuine technical area, explain concrete steps you take to improve, and show progress', True),
                    ('C', 'Blame your college faculty for not teaching advanced tools', False),
                    ('D', 'Say that your only weakness is working too hard without taking breaks', False),
                ]
            },
            {
                'subject': 'viva',
                'difficulty': 'medium',
                'question_text': 'In a project viva examination, how should you defend your choice between SQL and NoSQL for your application?',
                'correct_answer': 'By analyzing your data access patterns: relational integrity and ACID constraints require SQL, while unstructured horizontal scalability fits NoSQL.',
                'explanation': 'Examiners look for trade-off evaluation rather than buzzwords. Defend SQL by highlighting structured tabular schemas, transactional consistency (ACID), strict foreign key referential integrity, and complex relational query needs. Defend NoSQL if dealing with unstructured polymorphic documents, write-heavy streaming telemetry, or distributed horizontal partitioning.',
                'code_example': '-- Defense summary:\n-- "Our interview hub processes relational entities: Users, Questions, Options, and Attempts.\n-- Because student scoring and attempts require atomic consistency, PostgreSQL/SQLite is objectively superior to a document store."',
                'expected_output': 'Clear trade-off defense',
                'interview_tip': 'Never say "I used SQL because it was easy" or "because tutorials used it". Always frame it in terms of ACID requirements, data schema predictability, and referential integrity.',
                'tags': ['Project Viva', 'Architecture Justification', 'Database Selection'],
                'options': [
                    ('A', 'Argue that SQL is obsolete and NoSQL should always be chosen for all web apps', False),
                    ('B', 'Frame the decision around data structure, ACID transactional consistency, and access pattern trade-offs', True),
                    ('C', 'State that the database choice was made arbitrarily by your teammate', False),
                    ('D', 'Claim that NoSQL does not support primary keys or indexes', False),
                ]
            }
        ]

        question_count = 0
        for q_data in questions_dataset:
            subject = subjects[q_data['subject']]
            options_data = q_data.pop('options', [])
            q_data_clean = {k: v for k, v in q_data.items() if k != 'subject'}

            question, created = Question.objects.update_or_create(
                subject=subject,
                question_text=q_data['question_text'],
                defaults={
                    **q_data_clean,
                    'review_status': 'published',
                    'is_active': True
                }
            )

            # Recreate options
            AnswerOption.objects.filter(question=question).delete()
            for opt_label, opt_text, is_corr in options_data:
                AnswerOption.objects.create(
                    question=question,
                    option_label=opt_label,
                    option_text=opt_text,
                    is_correct=is_corr
                )

            question_count += 1

        self.stdout.write(f"Successfully seeded {question_count} verified questions with MCQ answer options.")

        # 3. Seed Coding Problems
        coding_problems = [
            {
                'title': 'Reverse a String',
                'slug': 'reverse-a-string',
                'difficulty': 'easy',
                'problem_statement': 'Write a function that reverses an input string using two pointers in Python without using built-in reverse helpers.',
                'sample_input': '"hello"',
                'sample_output': '"olleh"',
                'reference_solution': 'def reverse_string(s: str) -> str:\n    chars = list(s)\n    left, right = 0, len(chars) - 1\n    while left < right:\n        chars[left], chars[right] = chars[right], chars[left]\n        left += 1\n        right -= 1\n    return "".join(chars)',
                'algorithm_explanation': 'Two-pointer technique swapping characters in-place from outer boundaries inward until pointers meet.',
                'time_complexity': 'O(n)',
                'space_complexity': 'O(n)',
                'edge_cases': ['Empty string', 'Single character', 'Even vs odd length strings']
            },
            {
                'title': 'Valid Palindrome',
                'slug': 'valid-palindrome',
                'difficulty': 'easy',
                'problem_statement': 'Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.',
                'sample_input': '"A man, a plan, a canal: Panama"',
                'sample_output': 'True',
                'reference_solution': 'def is_palindrome(s: str) -> bool:\n    left, right = 0, len(s) - 1\n    while left < right:\n        while left < right and not s[left].isalnum():\n            left += 1\n        while left < right and not s[right].isalnum():\n            right -= 1\n        if s[left].lower() != s[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True',
                'algorithm_explanation': 'Pointers skip non-alphanumeric characters and compare normalized lowercase characters.',
                'time_complexity': 'O(n)',
                'space_complexity': 'O(1)',
                'edge_cases': ['All non-alphanumeric characters', 'Case-insensitive matching']
            },
            {
                'title': 'Binary Search',
                'slug': 'binary-search',
                'difficulty': 'medium',
                'problem_statement': 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.',
                'sample_input': 'nums = [-1,0,3,5,9,12], target = 9',
                'sample_output': '4',
                'reference_solution': 'def binary_search(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1',
                'algorithm_explanation': 'Divide-and-conquer on sorted sequence, halving search space on each iteration in logarithmic time.',
                'time_complexity': 'O(log n)',
                'space_complexity': 'O(1)',
                'edge_cases': ['Target not in array', 'Single element array', 'Target at boundaries']
            }
        ]

        for cp in coding_problems:
            CodingProblem.objects.update_or_create(slug=cp['slug'], defaults=cp)

        self.stdout.write(f"Successfully seeded {len(coding_problems)} coding problems.")

        # 4. Seed SQL Exercises
        sql_exercises = [
            {
                'title': 'Second Highest Salary',
                'slug': 'second-highest-salary',
                'difficulty': 'medium',
                'database_schema': 'Table: Employee (id INT, salary INT)',
                'sample_records': '1: 100, 2: 200, 3: 300',
                'query_requirement': 'Find the second highest distinct salary from the Employee table. Return NULL if fewer than two distinct salaries exist.',
                'correct_sql': 'SELECT (\n    SELECT DISTINCT salary\n    FROM Employee\n    ORDER BY salary DESC\n    OFFSET 1 LIMIT 1\n) AS SecondHighestSalary;',
                'expected_output': '+---------------------+\n| SecondHighestSalary |\n+---------------------+\n| 200                 |\n+---------------------+ ',
                'explanation': 'Scalar subquery wrapping OFFSET 1 LIMIT 1 guarantees a NULL result when row count is insufficient.'
            },
            {
                'title': 'Department Highest Salary',
                'slug': 'department-highest-salary',
                'difficulty': 'medium',
                'database_schema': 'Table: Employee (id INT, name VARCHAR, salary INT, departmentId INT)\nTable: Department (id INT, name VARCHAR)',
                'sample_records': 'Employee: (1, Joe, 70000, 1), (2, Jim, 90000, 1)\nDepartment: (1, IT)',
                'query_requirement': 'Find employees who have the highest salary in each of the departments.',
                'correct_sql': 'SELECT d.name AS Department, e.name AS Employee, e.salary AS Salary\nFROM Employee e\nJOIN Department d ON e.departmentId = d.id\nWHERE (e.departmentId, e.salary) IN (\n    SELECT departmentId, MAX(salary)\n    FROM Employee\n    GROUP BY departmentId\n);',
                'expected_output': '+------------+----------+--------+\n| Department | Employee | Salary |\n+------------+----------+--------+\n| IT         | Jim      | 90000  |\n+------------+----------+--------+',
                'explanation': 'Correlated tuple comparison using (departmentId, salary) IN aggregate subquery.'
            }
        ]

        for se in sql_exercises:
            SQLExercise.objects.update_or_create(slug=se['slug'], defaults=se)

        self.stdout.write(f"Successfully seeded {len(sql_exercises)} SQL exercises.")
        self.stdout.write(self.style.SUCCESS("All seed data created successfully!"))

