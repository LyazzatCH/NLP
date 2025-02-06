from textblob import TextBlob
import language_tool_python
import nltk
import string
from nltk.metrics import edit_distance
from nltk import bigrams, word_tokenize
from nltk.corpus import words, wordnet

nltk.download('words')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')  # Open Multilingual Wordnet, helpful for extended synonyms

CORPUS_PATH = 'Chemistry_Corpus.txt' #Constant to store Corpus

class SpellCheckerModule:
    # THE GENERAL SPELL CHECKER AND CORRECTION BLOCK
    def __init__(self):
        self.spell_check = TextBlob("")
        self.grammar_check = language_tool_python.LanguageTool('en-US')
        self.english_words = set(words.words())

    def correct_grammar(self, text):
        # Grammar correction
        matches = self.grammar_check.check(text)
        corrections = []
        for match in matches:
            corrections.append((match.matchedText, match.replacements))
        found_mistakes_count = len(matches)

        # Sort corrections alphabetically by the matched text
        corrections.sort(key=lambda x: x[0])

        # Real-word error detection
        real_word_errors = self.detect_real_word_errors(text)

        return corrections, found_mistakes_count, real_word_errors

    def detect_real_word_errors(self, text):
        tokens = word_tokenize(text)
        bigram_list = list(bigrams(tokens))

        errors = []
        for bigram in bigram_list:
            word1, word2 = bigram
            if word1 not in self.english_words and word2 in self.english_words:
                errors.append((word1, word2))

        # Convert the list of errors to a formatted string
        if errors:
            error_strings = [f"  (Wrong context: '{word1}' followed by '{word2}')" for word1, word2 in errors]
            return "\n".join(error_strings)
        else:
            return "No real-word errors detected."

    # THE BLOCK TO SEARCH MECHANISM, SPELL CHECKER AND SUGGESTIONS FOR CHEMISTRY WORDS
    def is_chemistry_related(self, word):
        """Check if a word is related to chemistry."""
        word = word.lower()
        synsets = wordnet.synsets(word)
        chemistry_related_lexnames = {'noun.acid',
                                      'noun.atom',
                                      'noun.carbohydrate',
                                      'noun.catalyst',
                                      'noun.chemical',
                                      'noun.electron',
                                      'noun.element',
                                      'noun.enzyme',
                                      'noun.ion',
                                      'noun.isotope',
                                      'noun.lipid',
                                      'noun.mixture',
                                      'noun.molecule',
                                      'noun.neutron',
                                      'noun.nonmetal',
                                      'noun.metal',
                                      'noun.polymer',
                                      'noun.protein',
                                      'noun.proton',
                                      'noun.radiation',
                                      'noun.reaction',
                                      'noun.salt',
                                      'noun.substance'}

        for synset in synsets:
            #print(f"Debugging Synset: {synset.name()} - Definition: {synset.definition()} - Lexname: {synset.lexname()}")
            if synset.lexname() in chemistry_related_lexnames:
                return True

        return False

    def get_synonyms(self, word):
        """Get synonyms for a given word from WordNet."""
        synonyms = set()
        synsets = wordnet.synsets(word)
        for synset in synsets:
            for lemma in synset.lemmas():
                synonyms.add(lemma.name().lower())
        return synonyms
    
    def get_chemistry_suggestions(self, misspelled_word):
        """Load the chemistry corpus from a text file, clean it, and generate a list of suggested correct words."""
        # Load the chemistry corpus
        with open(CORPUS_PATH, 'r', encoding='utf-8') as file:
            text = file.read()

        # Create a translation table for removing punctuation
        translator = str.maketrans('', '', string.punctuation)

        # Split text into words while removing punctuation
        cleaned_words = [word.translate(translator) for word in text.split()]

        # Create a set to store unique words
        corpus_words = set()

        for word in cleaned_words:
            # Add words to corpus, keeping uppercase abbreviations
            if word.isupper():
                corpus_words.add(word)
            else:
                corpus_words.add(word.lower())

        # Generate suggestions based on edit distance
        suggestions = []
        for word in corpus_words:
            if word.isupper():
                if edit_distance(misspelled_word.lower(), word.lower()) <= 2:
                    suggestions.append(word)
            else:
                if edit_distance(misspelled_word.lower(), word) <= 2:
                    suggestions.append(word)

        # Add synonyms to suggestions
        extended_suggestions = set(suggestions)
        for word in suggestions:
            synonyms = self.get_synonyms(word)
            for synonym in synonyms:
                if synonym in corpus_words:
                    extended_suggestions.add(synonym)

        # Filter suggestions to include only chemistry-related words
        filtered_suggestions = []
        for word in extended_suggestions:
            if self.is_chemistry_related(word):
                filtered_suggestions.append(word)

        # Check if filtered_suggestions is empty and return appropriate message
        if not filtered_suggestions:
            return ['NON-CHEMISTRY_WORD_IN_SEARCH!']

        # Remove duplicates and sort alphabetically
        sorted_suggestions = sorted(set(filtered_suggestions), key=lambda x: x.upper())

        return sorted_suggestions


