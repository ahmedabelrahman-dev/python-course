import random
import time

# word pairs => (prompt: related words)
word_pairs = {
    "sky": ["blue", "cloud", "bird", "fly", "sun"],
    "water": ["drink", "ocean", "swim", "fish", "boat"],
    "food": ["eat", "cook", "tasty", "meal", "restaurant"],
    "music": ["song", "dance", "listen", "band", "rhythm"],
    "book": ["read", "story", "page", "author", "library"],
    "tree": ["leaf", "green", "forest", "wood", "shade"],
    "car": ["drive", "road", "wheel", "travel", "speed"],
    "dog": ["pet", "bark", "walk", "loyal", "puppy"]
}

print("\n=== 🔄 WORD ASSOCIATION GAME 🔄 ===")
print("✨ Respond with a related word quickly! ✨")

score = 0
rounds = 0

while True:
    # Select a random word prompt
    prompt = random.choice(list(word_pairs.keys()))
    related_words = word_pairs[prompt]

    print(f"\n🔤 Prompt word: {prompt.upper()}")
    print("Quick! Type a word related to this prompt!")

    # Time the player's response
    start_time = time.time()
    # if the user types "  hello  " it will be converted to "hello"
    response = input("> ").lower().strip()
    response_time = time.time() - start_time

    print("response time", response_time)  # example output: 2.46475887298584

    # Check if response is related
    if response in related_words:
        # Calculate points based on response time
        points = max(1, 5 - int(response_time))
        score += points
        print(
            f"✅ Good association! +{points} points (answered in {response_time:.1f}s)")
    else:
        print(
            f"❌ Not a common association. Related words included: {', '.join(related_words)}")

    rounds += 1
    print(f"Score: {score}/{rounds * 5} possible points")

    # Ask to play again
    if input("\n🔄 Play again? (yes/no): ").lower().startswith('n'):
        print(f"Final score: {score}. Thanks for playing! 👋")
        break
