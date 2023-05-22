from flask import Flask, Blueprint, request

# url_prefix="prompts"
bp = Blueprint("prompts", __name__)

@bp.route('/liability')
def liability():
    return

@bp.route('/liability/summary')
def liability_summary():
    return