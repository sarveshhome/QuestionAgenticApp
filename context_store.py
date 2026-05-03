"""
Predefined context store for subjects and exam types.
Contains sample questions, patterns, and difficulty metadata used
by the agent to ground LLM responses.
"""

CONTEXT_STORE: dict = {
    "mathematics": {
        "jee": {
            "difficulty": "Hard",
            "pattern": "Multiple choice, assertion-reason, integer answer, matrix match",
            "sample_questions": [
                "If f(x) = x³ - 3x + 2, find the local minima and maxima.",
                "Evaluate the definite integral ∫₀^π sin²(x) dx.",
                "The sum of roots of the equation 2x² - 5x + 3 = 0 is?",
                "Find the area enclosed by y = x² and y = x + 2.",
                "If P and Q are two matrices such that PQ = P and QP = Q, then Q² is equal to?"
            ]
        },
        "sat": {
            "difficulty": "Medium",
            "pattern": "Multiple choice, grid-in, no calculator section",
            "sample_questions": [
                "If 3x + 7 = 22, what is the value of x?",
                "A circle has a radius of 5. What is its area in terms of π?",
                "What is the slope of the line passing through (2, 3) and (4, 7)?",
                "Simplify: (x² - 9) / (x - 3)",
                "If f(x) = 2x - 1, what is f(f(3))?"
            ]
        },
        "gate": {
            "difficulty": "Very Hard",
            "pattern": "MCQ, multiple select, numerical answer type",
            "sample_questions": [
                "Find the eigenvalues of the matrix [[2, 1], [1, 2]].",
                "Solve the differential equation dy/dx + 2y = e^(-x).",
                "Evaluate the Laplace transform of f(t) = t·e^(2t).",
                "What is the rank of the matrix [[1,2,3],[4,5,6],[7,8,9]]?",
                "Compute ∬ (x² + y²) dA over the region x² + y² ≤ 4."
            ]
        }
    },
    "physics": {
        "jee": {
            "difficulty": "Hard",
            "pattern": "Conceptual MCQ, numerical, passage-based",
            "sample_questions": [
                "A body is thrown vertically upward with velocity 20 m/s. Find maximum height (g = 10 m/s²).",
                "Two charges +q and -q are placed at distance d. Find electric field at midpoint.",
                "A capacitor of 4μF is charged to 100V. Find energy stored.",
                "An ideal gas expands adiabatically. What happens to its temperature?",
                "Find the de Broglie wavelength of an electron moving at 10⁶ m/s."
            ]
        },
        "neet": {
            "difficulty": "Medium-Hard",
            "pattern": "Concept-based MCQ, theory + numericals",
            "sample_questions": [
                "What is the unit of electric field intensity?",
                "A projectile is thrown at 45°. Find the range in terms of initial velocity.",
                "State and explain Newton's second law of motion.",
                "The work done in moving a charge in an equipotential surface is?",
                "Find the focal length of a concave mirror with radius of curvature 30 cm."
            ]
        },
        "gate": {
            "difficulty": "Very Hard",
            "pattern": "Numerical answer type, advanced derivations",
            "sample_questions": [
                "Determine the Poynting vector for a plane wave in free space.",
                "Calculate the magnetic flux density for a long straight conductor carrying 10A at 0.5m distance.",
                "Derive the expression for the time period of a simple pendulum.",
                "State and prove Gauss's law in differential form.",
                "Compute the transmission coefficient for a particle tunneling through a potential barrier."
            ]
        }
    },
    "chemistry": {
        "jee": {
            "difficulty": "Hard",
            "pattern": "MCQ, assertion-reason, linked comprehension",
            "sample_questions": [
                "Write the IUPAC name of CH₃-CH(OH)-CH₂-COOH.",
                "Calculate the molarity of a solution containing 4g of NaOH in 500mL.",
                "What is the hybridization and geometry of SF₄?",
                "Which of the following is NOT a characteristic of ionic compounds?",
                "Explain SN1 vs SN2 reaction mechanism with examples."
            ]
        },
        "neet": {
            "difficulty": "Medium",
            "pattern": "Concept-based theory + numerical MCQ",
            "sample_questions": [
                "What is the electron configuration of Fe²⁺?",
                "Name the functional group present in acetic acid.",
                "Balance the equation: Fe + H₂O → Fe₃O₄ + H₂",
                "What is pH of a 0.01M HCl solution?",
                "Explain why noble gases are chemically inert."
            ]
        }
    },
    "biology": {
        "neet": {
            "difficulty": "Medium",
            "pattern": "Diagram-based MCQ, assertion-reason, conceptual",
            "sample_questions": [
                "What is the role of the mitochondria in eukaryotic cells?",
                "Describe the process of DNA replication with key enzymes.",
                "What is the difference between mitosis and meiosis?",
                "Name the hormone responsible for regulating blood glucose levels.",
                "Explain the mechanism of muscle contraction at the molecular level."
            ]
        },
        "upsc": {
            "difficulty": "Medium",
            "pattern": "Descriptive, short answer, fact-based",
            "sample_questions": [
                "What is CRISPR-Cas9 and what are its applications?",
                "Describe the significance of biodiversity hotspots in India.",
                "Explain the concept of ecological succession.",
                "What are zoonotic diseases? Give examples.",
                "Describe the food web in a tropical rainforest ecosystem."
            ]
        }
    },
    "computer science": {
        "gate": {
            "difficulty": "Very Hard",
            "pattern": "MCQ, numerical, code-trace, algorithm analysis",
            "sample_questions": [
                "What is the time complexity of merge sort?",
                "Explain the difference between process and thread.",
                "Given a BFS traversal, identify the graph structure.",
                "Write a dynamic programming solution for the 0/1 Knapsack problem.",
                "What is the difference between deadlock and starvation in OS?"
            ]
        },
        "sat": {
            "difficulty": "Easy-Medium",
            "pattern": "Logical reasoning, basic computational thinking",
            "sample_questions": [
                "What does CPU stand for and what is its primary function?",
                "Describe the difference between RAM and ROM.",
                "What is the binary representation of decimal 25?",
                "What is an algorithm? Give a real-life example.",
                "How does the internet use IP addresses?"
            ]
        }
    }
}


def get_context(subject: str, exam_type: str) -> dict:
    """
    Retrieve context for a given subject and exam type.
    Falls back gracefully if no exact match found.
    """
    subj = subject.lower().strip()
    exam = exam_type.lower().strip()

    subject_data = CONTEXT_STORE.get(subj)
    if not subject_data:
        # Try partial match
        for key in CONTEXT_STORE:
            if key in subj or subj in key:
                subject_data = CONTEXT_STORE[key]
                break

    if not subject_data:
        return _default_context(subject, exam_type)

    exam_data = subject_data.get(exam)
    if not exam_data:
        # Fallback to first available exam type for that subject
        first_exam = next(iter(subject_data.values()))
        exam_data = first_exam

    return exam_data


def _default_context(subject: str, exam_type: str) -> dict:
    return {
        "difficulty": "Medium",
        "pattern": "Mixed MCQ and descriptive questions",
        "sample_questions": [
            f"Explain a fundamental concept in {subject}.",
            f"What is the most important topic in {subject} for {exam_type}?",
            f"Solve a typical {exam_type} problem related to {subject}.",
            f"Describe the application of {subject} in real life.",
            f"Give an example of a difficult {exam_type} question on {subject}."
        ]
    }
