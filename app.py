#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Minimal Yatzee Flask application, including useful error handlers.
"""
import traceback
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for
from src.trie import Trie
from src.file_manager import FileManager
from src.errors import SearchMiss


app = Flask(__name__)
app.debug = True
app.secret_key = "my_secret_key"


trie = Trie()
# check if tri is int empty initally / globally
# words = trie.get_all_words()
# print("words from trie DS:", trie)
# print("empty trie obj:", trie)
# current_file should be updated from the /select route and applied
# globaly so that initalize_ttrie used allwasy the files that is slected
current_file = "tiny_dictionary.txt"


def initialize_trie():
    global trie
    # trie = Trie()
    trie = Trie.create_from_file(current_file)
    # print(trie.get_all_words())
    # words_from_file = FileManager.load_words_from_file(current_file)
    # removed_words = session.get('removed_words', [])
    # for word in words_from_file:
    #     trie.insert(word)
    removed_words = session.get('removed_words', [])
    try:
        for word in removed_words:
            trie.remove(word)
    except SearchMiss as e:
        print(f"Error during Trie initialization: {e}")
    # for word in words_from_file:
    #     if word not in removed_words:
    #         trie.insert(word)


@app.route("/remove_word", methods=['GET', "POST"])
def remove_word():
    """
    Route to handle the word removal from the Trie.
    """
    if request.method == "POST":
        word_to_remove = request.form.get('remove_word')
        word_to_remove = word_to_remove.strip().lower()
        try:
            if trie.search(word_to_remove):

                removed_words = session.get('removed_words', [])
                removed_words.append(word_to_remove)
                session['removed_words'] = removed_words
                # print("Updated removed_words from seesh 1:",session.get('removed_words', []))
                trie.remove(word_to_remove)
                return redirect(url_for('words'))
            else:
                print(session)
                return render_template('remove_word.html', word_to_remove=word_to_remove)
        except SearchMiss as e:
            print(f"Error during word removal: {e}")
    # print("Updated removed_words from sesh 2:",session.get('removed_words', []))
    return render_template('remove_word.html')


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
    initialize_trie()
    search_result = None
    searched_word = ""
    if request.method == "POST":
        searched_word = request.form.get("word", "").strip()
        if searched_word:
            search_result = trie.search(searched_word)

    return render_template("check_word.html",
                           search_result=search_result,
                           searched_word=searched_word,
                           )



@app.route('/search', methods=['GET'])
def search():
    prefix = request.args.get('prefix', '')
    matched_words = trie.search_prefix(prefix) if prefix else []

    return render_template('search.html', matched_words=matched_words, prefix=prefix)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    """
    Reset the game session to start a new game.
    """
    global current_file
    current_file = "tiny_dictionary.txt"
    # re initiallize from start
    session.clear()
    initialize_trie()

    return redirect(url_for('main'))


@app.route("/select", methods=['GET', 'POST'])
def select():
    """
    Route for the select page
    """
    global current_file
    list_files = FileManager.get_available_files()
    prompt = None
    if request.method == 'POST':
        selected_file = request.form.get('file')

        if selected_file is None:
            prompt = "Please select a file. !!!"
            print(prompt)
        else:
            current_file = selected_file
            session.clear()
            initialize_trie()

    return render_template('select.html',
                           list_files=list_files,
                           current_file=current_file,
                           prompt=prompt
                           )


@app.route("/words", methods=['GET', 'POST'])
def words():
    """
    Route for the about page
    """
    global current_file
    # print("file name from words route gets global:", current_file)
    initialize_trie()
    # words_in_list = trie.get_all_words()
    # for word in words_in_list:
    # print(word)
    # print("the words returned:", words_in_list)
    total_nodes = trie.size()
    # all_words_list = trie.search_prefix('')
    words = trie.get_all_words()
    sorted_words = sorted(words)
    return render_template('all_words.html',
                           #    words=sorted_words,
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
