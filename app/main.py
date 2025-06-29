import os
from app.sections.experience import (
    extract_experiences_with_ai,
    generate_experience_questions,
    improve_experience_with_answers,
)
from app.utils.file_loader import load_resume_text

data_dir = "data"
files = [f for f in os.listdir(data_dir) if f.endswith(".txt") or f.endswith(".pdf")]

if not files:
    print("❌ No .txt or .pdf file found in the 'data/' folder.")
    exit(1)

resume_file = os.path.join(data_dir, files[0])
print(f"📄 Resume loaded: {resume_file}")

resume_text = load_resume_text(resume_file)

experiences = extract_experiences_with_ai(resume_text)

if not experiences:
    print("❌ No experiences could be extracted from the resume.")
    exit(1)

print("\n📝 Detected experiences:\n")
for i, exp in enumerate(experiences, 1):
    print(f"{i}. {exp[:150].replace(chr(10), ' ')}...\n")

while True:
    choice = input(f"Enter the number of the experience you want to improve (1-{len(experiences)}): ")
    if choice.isdigit() and 1 <= int(choice) <= len(experiences):
        selected_idx = int(choice) - 1
        break
    print("Invalid choice. Please try again.")

selected_experience = experiences[selected_idx]

print("\n📌 Selected experience:")
print(selected_experience)

questions = generate_experience_questions(selected_experience)
print("\n❓ Please answer the following questions to help improve this experience:\n")
print(questions)

print("\nEnter your answers (in plain text):")
user_answers = input("> ")

improved_description = improve_experience_with_answers(selected_experience, user_answers)

print("\n✅ Improved description:\n")
print(improved_description)
