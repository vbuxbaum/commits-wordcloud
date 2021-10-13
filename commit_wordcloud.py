from wordcloud import WordCloud
import requests
from parsel import Selector
from time import sleep
import sys

from PIL import Image
import numpy as np


GITHUB_BASE_URL = "https://github.com/"


def main():
    repo_path = sys.argv[1]
    pr_list_url = GITHUB_BASE_URL + repo_path + "/pulls"

    pr_name_list = []
    while pr_list_url:
        pr_list_html = fetch(pr_list_url)
        pr_name_list.extend(get_pull_names(pr_list_html))
        pr_list_url = get_next_pulls_page(pr_list_html)
        pr_list_url = GITHUB_BASE_URL + pr_list_url if pr_list_url else None

    output_file = (
        sys.argv[2] if len(sys.argv) > 2 else process_repo_name(repo_path)
    )

    generate_wordcloud(" ".join(pr_name_list), output_file)


def fetch(url):
    response = requests.get(url)
    sleep(1)
    return response.text


def get_pull_names(html_content):
    selector = Selector(text=html_content)
    found_names = selector.css(
        ".Link--primary.js-navigation-open.markdown-title ::text"
    ).getall()
    return found_names


def get_next_pulls_page(html_content):
    selector = Selector(text=html_content)
    return selector.css(
        "div.paginate-container.d-none.d-sm-flex.flex-sm-justify-center "
        "> div > a.next_page ::attr(href)"
    ).get()


def generate_wordcloud(input_string, output_file="pr_names_wordcloud.png"):
    mask = np.array(Image.open("mask.png"))

    result = WordCloud(width=1600, height=800, mask=mask).generate(
        input_string
    )

    result.to_file(output_file)


def process_repo_name(repo_path):
    return repo_path.replace("/", "_") + ".png"


if __name__ == "__main__":
    main()
