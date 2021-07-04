#!/usr/bin/env python3

"""A simple script does two things:
	1. Crawls lottery results from ketqua1.net
	2. Checks daily lottery as arguments win or not
	
	(2 last digit on lottery ticket). 
	If there is no argument then:
	Print all the winning numbers.

Usage:
	$ python3 lotto.py [NUMBER1] [NUMBER2] [...]
"""

import argparse
from typing import Any, List, Tuple

from bs4 import BeautifulSoup
import requests


def get_tree() -> Any:
    sess = requests.Session()
    with sess:
        resp = sess.get('https://ketqua1.net/', timeout=5)

    return BeautifulSoup(resp.text, 'html.parser')


def find_daily_drawings(tree: Any) -> Tuple[str, List[str]]:
    """
    Get the results of daily lottery
    - Crawl the drawing's day-date.
    - List all the div tags containing results.
    - With each div tag, collects all result's IDs.
      e.g. ['rs_8_0', 'rs_0_0', 'rs_1_0', 'rs_2_0',... ]
    - With each result's ID, scrape the drawings.

    :param tree: BeautifulSoup4 tree
    :rtype Tuple:
    """
    date = tree.find("tr", class_="title_row").text.strip("\n")
    div_tags = tree.find("table", id="result_tab_mb").find_all("div")
    rs_id = [div.get('id') for div in div_tags if div.get('id')]
    daily_drawings = [tree.find(id=i).text for i in rs_id]
    del daily_drawings[0]  # Delete the jackpot-characters

    return date, daily_drawings


def show_result(date: str, drawings: List[str]) -> str:
    result = """{}

    JACKPOT: {}

    1: {}
    2: {} - {}
    3: {} - {} - {}
       {} - {} - {}
    4: {} - {} - {} - {}
    5: {} - {} - {}
       {} - {} - {}
    6: {} - {} - {}
    7: {} - {} - {} - {}
    """.format(date, *drawings)

    return result


def check_user_ticket(tree: Any, user_numbers: List[str]) -> None:
    """Checks whether user win or not

    :param tree: BeautifulSoup4 tree
    :param user_numbers: user ticket numbers
    :rtype None:
    """
    date, drawings = find_daily_drawings(tree)
    if not user_numbers:
        # Without arguments
        print(show_result(date, drawings))
    else:
        # With arguments
        lotto = [number[-2:] for number in drawings]

        win = []
        for number in user_numbers:
            if number[-2:] in lotto:
                win.append(number[-2:])

        if not win:
            print("Good Luck Next Time!")
        else:
            print("Congratulation! You win: " + " - ".join(win))


def solve(tree: Any, user: List[str]) -> None:
    """Function `solve` for `test` purpose

    Return the same value in both `solve` and `check_user_ticket`

    :param tree: BeautifulSoup4 tree
    :param user: user ticket numbers
    :rtype None:
    """
    return check_user_ticket(tree, user)


def main() -> None:
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Check numbered tickets lotto"
    )
    parser.add_argument(
        "lotto_numbers",
        type=str,
        nargs="*",
        help="Numbers on your lottery ticket."
    )
    args = parser.parse_args()
    user = args.lotto_numbers

    # Show lottery results
    tree = get_tree()
    solve(tree, user)


if __name__ == "__main__":
    main()
