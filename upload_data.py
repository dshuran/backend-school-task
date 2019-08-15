from flask import request, abort


def main():
    if not request.json:
        abort(400)
