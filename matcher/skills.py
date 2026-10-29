
import re


def load_skills(path="data/skills_list.txt"):
    # Open the skills file and read each line
    with open(path, encoding="utf-8") as f:
        return [
            line.strip().lower()
            for line in f
            if line.strip()
        ]


def extract_skills(text: str, skills: list[str]) -> set[str]:
    # Convert the input text to lowercase
    text = text.lower()

    # Store the skills found in the text
    found = set()

    # Check each skill against the input text
    for skill in skills:
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        # Add the skill if it matches
        if re.search(pattern, text):
            found.add(skill)

    # Return all matched skills
    return found
