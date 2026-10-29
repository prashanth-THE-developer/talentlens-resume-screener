from matcher.score import text_similarity
from matcher.skills import extract_skills
def test_identical_text():
assert text_similarity("python sql react", "python sql react") > 0.99
def test_empty_text():
assert text_similarity("", "python") == 0.0
def test_java_not_javascript():
found = extract_skills("I know javascript", ["java", "javascript"])
assert found == {"javascript"}