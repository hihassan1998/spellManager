#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Minimal Yatzee Flask application, including useful error handlers.
"""
import traceback
# from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for
from src.trie import Trie
from src.file_manager import FileManager
from src.errors import SearchMiss


app = Flask(__name__)
app.debug = True
app.secret_key = "my_secret_key"


@app.route("/", methods=['GET', 'POST'])
def main():
    """
    Route for the home page with minor details about trie dict manager app
    """
    return render_template("index.html")


@app.route('/check_word', methods=["GET", "POST"])
def check_word():
    """
    Display the checked word page the dispaly if entry is valid.
    """
    current_file = session['current_file']
    trie = Trie.create_from_file(current_file)
    removed_words = session.get('removed_words', [])
    try:
        for word in removed_words:
            trie.remove(word)
    except SearchMiss as e:
        print(f"Error during Trie initialization: {e}")

    search_result = None
    searched_word = ""
    if request.method == "POST":
        searched_word = request.form.get("word", "").strip()
        if searched_word:
            # search_result = trie.search(searched_word)
            try:
                search_result = trie.search(searched_word)
            except SearchMiss:
                search_result = False

    return render_template("check_word.html",
                           search_result=search_result,
                           searched_word=searched_word,
                           )


@app.route('/search', methods=['GET'])
def search():
    """
    Route for the preix based search page 
    """
    prefix = request.args.get('prefix', '')

    current_file = session['current_file']
    trie = Trie.create_from_file(current_file)
    removed_words = session.get('removed_words', [])
    try:
        for word in removed_words:
            trie.remove(word)
    except SearchMiss as e:
        print(f"Error during Trie initialization: {e}")
    if prefix:
        matched_words = trie.prefix_search(prefix)
    else:
        matched_words = []

    return render_template('search.html',
                           matched_words=matched_words,
                           prefix=prefix)


@app.route('/search_suffix', methods=['GET'])
def search_suffix():
    """
    Route for the suffix based search page 
    """
    suffix = request.args.get('suffix', '')
    current_file = session['current_file']
    trie = Trie.create_from_file(current_file)
    removed_words = session.get('removed_words', [])
    try:
        for word in removed_words:
            trie.remove(word)
    except SearchMiss as e:
        print(f"Error during Trie initialization: {e}")

    if suffix:
        matched_words = trie.suffix_search(suffix)
        print(matched_words)
    else:
        matched_words = []

    return render_template('search_suffix.html',
                           matched_words=matched_words,
                           suffix=suffix)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    """
    Reset the game session to start a new game.
    """
    session.clear()
    session['current_file'] = 'dictionary.txt'
    return redirect(url_for('main'))


@app.route("/remove_word", methods=['GET', "POST"])
def remove_word():
    """
    Route to handle the word removal from the Trie.
    """
    current_file = session.get('current_file', 'dictionary.txt')
    trie = Trie.create_from_file(current_file)

    word_to_remove = None
    error_message = None

    if request.method == "POST":
        word_to_remove = request.form.get('remove_word')
        word_to_remove = word_to_remove.strip().lower()

        removed_words = session.get('removed_words', [])

        try:
            if word_to_remove in removed_words:
                raise SearchMiss(
                    f"The word '{word_to_remove}' has already been removed.")

            if trie.search(word_to_remove):
                removed_words.append(word_to_remove)
                session['removed_words'] = removed_words
                trie.remove(word_to_remove)
                return redirect(url_for('words'))

            raise SearchMiss(
                f"The word '{word_to_remove}' is not present in the dictionary.")

        except SearchMiss as e:
            error_message = str(e)

    return render_template('remove_word.html',
                           word_to_remove=word_to_remove,
                           error_message=error_message)


@app.route("/select", methods=['GET', 'POST'])
def select():
    """
    Route for the select page
    """
    selected_file = session.get('current_file', 'dictionary.txt')
    list_files = FileManager.get_available_files()
    prompt = None
    if request.method == 'POST':
        selected_file = request.form.get('file')

        if selected_file is None:
            prompt = "Please select a file. !!!"
            print(prompt)
        else:
            session.clear()
            session['current_file'] = selected_file
            print(
                f"Updated current_file in session: {session['current_file']}")

    return render_template('select.html',
                           list_files=list_files,
                           current_file=selected_file,
                           prompt=prompt
                           )


@app.route("/words", methods=['GET', 'POST'])
def words():
    """
    Route for the words dispaly page
    """
    current_file = session['current_file']
    trie = Trie.create_from_file(current_file)
    removed_words = session.get('removed_words', [])
    try:
        for word in removed_words:
            trie.remove(word)
    except SearchMiss as e:
        print(f"Error during Trie initialization: {e}")
    total_nodes = trie.size()
    all_words = trie.get_all_words()
    sorted_words = sorted(all_words)
    return render_template('all_words.html',
                           words=sorted_words,
                           total_nodes=total_nodes,
                           current_file=current_file
                           )


@app.route("/about")
def about():
    """
    Route for the about page
    """
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    # pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    # pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    app.run()
