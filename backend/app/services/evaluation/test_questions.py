"""
A small, curated set of test questions used to evaluate RAG quality,
each paired with a hand-verified reference answer (needed for the
ContextPrecision metric, which checks retrieved context against a
known-correct answer).
"""

EVAL_QUESTIONS = [
    {
        "question": "What was Apple's total revenue in fiscal year 2025?",
        "reference": "Apple's total net sales in fiscal year 2025 were $416,161 million.",
    },
    {
        "question": "What are Microsoft's main risk factors related to cloud computing?",
        "reference": "Microsoft's cloud computing risk factors include the highly competitive and dynamic market, the need for continuous investment in cloud and AI infrastructure which may increase costs, and dependence on data center resources like land, energy, networking supplies, and servers including GPUs.",
    },
    {
        "question": "Compare Apple and Microsoft's approach to risk factors.",
        "reference": "Apple's risk factors focus on external threats such as natural disasters, supply chain risks, and cybersecurity attacks. Microsoft's risk factors emphasize cybersecurity through initiatives like the Secure Future Initiative, along with environmental sustainability commitments.",
    },
    {
        "question": "What was Amazon's net income in the most recent fiscal year?",
        "reference": "Amazon's net income for fiscal year 2025 (ended December 31, 2025) was $77,670 million, up from $59,248 million in fiscal year 2024.",
    },
    {
        "question": "What cybersecurity measures has Microsoft implemented?",
        "reference": "Microsoft has implemented the Secure Future Initiative (SFI) to improve cybersecurity protection, and operates a cybersecurity program and governance framework to identify, manage, and mitigate cybersecurity threats.",
    },
]