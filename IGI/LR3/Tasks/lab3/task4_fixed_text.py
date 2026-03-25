"""Task 4: analysis of a fixed text line."""

from lab3.decorators import log_call

SOURCE_TEXT = (
    "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy "
    "and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and "
    "picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
)

VOWELS = set("aeiouy")


def normalize_word(word: str) -> str:
    """Return lowercased word without edge punctuation."""
    return word.strip(".,!?;:\"'()[]{}").lower()


def split_words(text: str) -> list[str]:
    """Split text by spaces and commas, then normalize words."""
    text_with_spaces = text.replace(",", " ")
    parts = text_with_spaces.split()

    normalized_words = []
    for part in parts:
        word = normalize_word(part)
        normalized_words.append(word)

    result = [word for word in normalized_words if word]
    return result

def starts_with_consonant(word: str) -> bool:
    """Return True if word starts with an English consonant letter."""
    if not word:
        return False
    first = word[0]
    return first.isalpha() and first not in VOWELS


def has_double_letter(word: str) -> bool:
    """Return True if word contains two same neighboring letters."""
    lower_word = word.lower()
    return any(lower_word[i] == lower_word[i + 1] for i in range(len(lower_word) - 1))


def analyze_text(text: str) -> tuple[int, list[tuple[int, str]], list[str]]:
    """Return answer for the task"""
    words = split_words(text)
    consonant_start_count = sum(1 for w in words if starts_with_consonant(w))
    words_with_double = [(idx, word) for idx, word in enumerate(words, start=1) if has_double_letter(word)]
    sorted_words = sorted(words)
    return consonant_start_count, words_with_double, sorted_words


@log_call
def run_task_4() -> None:
    """Run task 4 for fixed text and print analysis."""
    print("Задание 4: анализ фиксированной строки.")
    print(f"\nИсходная строка:\n{SOURCE_TEXT}\n")
    count, repeated_pairs, alphabetical_words = analyze_text(SOURCE_TEXT)
    print(f"а) Количество слов, начинающихся с согласной: {count}")
    print("б) Слова с двумя одинаковыми буквами подряд и их номера:")
    if repeated_pairs:
        for index, word in repeated_pairs:
            print(f"   {index}: {word}")
    else:
        print("   Таких слов нет.")
    print("в) Слова в алфавитном порядке:")
    print(", ".join(alphabetical_words))
