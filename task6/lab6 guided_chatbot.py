from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQs
questions = [
    "How do I reset my password?",
    "How do I submit an assignment?"
]

answers = [
    "Use the recovery link on the login page. [Source: it_help.txt]",
    "Upload your assignment through the course portal. [Source: student_handbook.txt]"
]

# TF-IDF model
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(questions)

print("Simple FAQ Chatbot")
print("Type exit to stop.")

while True:

    user = input("\nYou: ")

    if user.lower() == "exit":
        break

    if user.strip() == "":
        print("Bot: Please enter a question.")
        continue

    # Exact question check
    if user.lower() in [q.lower() for q in questions]:
        index = [q.lower() for q in questions].index(user.lower())
        print("Bot:", answers[index])
        continue

    # Search using TF-IDF
    user_vector = vectorizer.transform([user])

    if user_vector.nnz == 0:
        print("Bot: No matching FAQ found.")
        continue

    scores = cosine_similarity(user_vector, faq_vectors)[0]

    best_index = scores.argmax()

    if scores[best_index] > 0:
        print("Bot: Possible question:")
        print(questions[best_index])
        print("Please confirm by entering the exact question.")
    else:
        print("Bot: No matching FAQ found.")