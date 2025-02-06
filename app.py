from flask import Flask, render_template, request
from Model import SpellCheckerModule

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST'])
def spell():
    text = request.form.get('text', '')
    corrections, mistakes_count, real_word_errors = spell_checker_module.correct_grammar(text)
    print(f"Corrections List: {corrections}")

    # Convert corrections list to a dictionary
    corrections_dict = {}
    for original, suggestions in corrections:
        corrections_dict[original] = suggestions

    # Initialize the highlighted_text as the original text
    highlighted_text = text

    # If there are mistakes, generate HTML for crossed-out text
    if mistakes_count > 0:
        for original, _ in corrections:
            highlighted_text = highlighted_text.replace(original, f"<del>{original}</del>")
        # Concatenate real_word_errors only when there are mistakes
        highlighted_text += real_word_errors
    print(mistakes_count)

    return render_template(
        'index.html',
        original_text=text,
        highlighted_text=highlighted_text if mistakes_count > 0 else None,  # Pass None if no mistakes
        corrections=corrections_dict,
        mistakes_count=mistakes_count
    )

@app.route('/apply_corrections', methods=['POST'])
def apply_corrections():
    original_text = request.form.get('original_text', '')
    corrections = {key: value for key, value in request.form.items() if key.startswith('correction_') and value}

    final_text = original_text
    for key, value in corrections.items():
        original_word = key.split('_')[1]
        final_text = final_text.replace(original_word, value, 1)

    return render_template(
        'index.html',
        original_text=final_text,  # Update text editor with the corrected text
        corrections={},  # Clear corrections after applying
        mistakes_count=None  # Optionally, provide information about mistakes
    )


# Route to handle search chemistry-related functionality
@app.route('/search_dictionary', methods=['GET'])
def search_dictionary():
    word = request.args.get('word', '')
    if not word:
        return render_template(
            'index.html',
            corrections={},
            original_text=''
        )

    # Get chemistry-related suggestions
    filtered_suggestions = spell_checker_module.get_chemistry_suggestions(word)

    # Convert the suggestions list to a dictionary format (if needed for compatibility)
    corrections_dict = {word: filtered_suggestions}

    return render_template(
        'index.html',
        corrections=corrections_dict,  # Display the suggestions for the searched word
        original_text=''
    )

if __name__ == "__main__":
    app.run(debug=True)
