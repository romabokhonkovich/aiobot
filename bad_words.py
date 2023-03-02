with open('words.txt', 'r', encoding='utf-8') as file:
    bad_words = [word.strip().lower() for word in file if word.strip()]

pattern = '|'.join(bad_words)
# Создайте регулярное выражение для поиска матерных слов
bad_words_pattern = re.compile(pattern, re.IGNORECASE)
