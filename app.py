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


app = Flask(__name__)
app.debug = True
app.secret_key = "my_secret_key"


trie = Trie()
current_file = "tiny_dictionary.txt"


def initialize_trie():
    global trie
    trie = Trie()
    words_from_file = FileManager.load_words_from_file(current_file)
    for word in words_from_file:
        trie.insert(word)


@app.route("/", methods=['GET', 'POST'])
def main():
    """
    Route for the home page with minor details about tri dict manager app
    """
    return render_template("index.html")


@app.route('/search', methods=['GET'])
def search():
    prefix = request.args.get('prefix', '')
    matched_words = trie.search_prefix(prefix) if prefix else []

    return render_template('search.html', words=matched_words, prefix=prefix)


@app.route("/reset", methods=['GET', 'POST'])
def reset():
    """
    Reset the game session to start a new game.
    """
    session.clear()
    # return redirect("/~hahi24/dbwebb-kurser/oopython/me/kmom04/yahtzee3/app.cgi")
    return redirect(url_for('main'))


@app.route("/words", methods=['GET'])
def words():
    """
    Route for the about page
    """
    initialize_trie()
    words_in_list = trie.get_all_words()
    for word in words_in_list:
        print(word)
    # print("the words returned:", words_in_list)
    total_nodes = trie.size()
    # all_words_list = trie.search_prefix('')
    words = trie.get_all_words()
    sorted_words = sorted(words)
    return render_template('all_words.html', 
                        #    words=sorted_words,
                           words=sorted_words,
                           total_nodes=total_nodes)

@app.route("/about")
def about():
    """
    Route for the about page
    """
    return render_template("about.html")


@app.route('/check_word', methods=["GET", "POST"])
def check_word():
    """
    Display the leaderboard page with the current entries and total points.
    """
    initialize_trie()
    search_result = None
    searched_word = ""
    if request.method == "POST":
        searched_word = request.form.get("word", "").strip().lower()
        if searched_word:
            search_result = trie.search(searched_word)
            print("reply from class:", search_result)

    return render_template("check_word.html",
                           search_result=search_result,
                           searched_word=searched_word,
                           )


@app.route('/delete_mode', methods=['POST'])
def delete_mode():
    """
    Toggle the delete mode on the leaderboard page.
    """
    session['delete_mode'] = not session.get('delete_mode', False)
    return redirect(url_for('leaderboard'))


@app.route('/check_word', methods=['POST'])
def add_entry():
    """
    Add a new entry to the leaderboard with the player's name and score.
    """
    # filename = Path("leaderboard.txt")

    player_name = request.form['player_name']

    session['player_name_submitted'] = True

    return redirect(url_for('check_word'))


@app.route('/leaderboard/<int:index>', methods=['POST'])
def delete_entry(index):
    """
    Delete a specific leaderboard entry at its index.
    """
    # leaderboard_obj = Leaderboard.load("leaderboard.txt")
    # leaderboard_obj.remove_entry(index)

    return redirect(url_for('leaderboard'))


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
