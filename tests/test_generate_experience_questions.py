from app.sections.experience import parse_numbered_questions

def test_parse_numbered_questions():
    example_output = """
    1. What was your main responsibility in this role?
    2. What were the key results or metrics achieved?
    3. Which tools or technologies did you use?
    """
    expected = [
        "What was your main responsibility in this role?",
        "What were the key results or metrics achieved?",
        "Which tools or technologies did you use?"
    ]
    parsed = parse_numbered_questions(example_output)
    assert parsed == expected
