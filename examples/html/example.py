import nixeval
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_comments_html(comments):
    return nixeval.loads(f"import {dir_path}/default.nix {nixeval.dumps(comments)}")

mock_comments = [
    { "user": "Carol",   "date": "2025-05-14", "content": "First mock comment!" },
    { "user": "Dave",    "date": "2025-05-15", "content": "Another one here." },
    { "user": "Eve",     "date": "2025-05-16", "content": "Loving this demo." },
    { "user": "Frank",   "date": "2025-05-17", "content": "Can't wait to see more!" },
    { "user": "Grace",   "date": "2025-05-18", "content": "This is the fifth comment." },
]

print(get_comments_html(mock_comments))