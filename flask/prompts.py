from flask import Flask, Blueprint, request
from plaintiff.plaintiffs import *

# url_prefix="prompts"
bp = Blueprint("prompts", __name__)

@bp.route('/')
def index():
    return "LIABILITY, DAMAGES, CREDIBILITY, PROBLEMS"

@bp.route('/liability')
def liability():
    return PLA_LIA_BP_PROMPT

@bp.route('/liability/summary')
def liability_summary():
    return PLA_LIA_BP_SUMMARY

@bp.route('/damages')
def damages():
    return PLA_DAM_BP_PROMPT

@bp.route('/damages/summary')
def damages_summary():
    return PLA_DAM_BP_SUMMARY

@bp.route('/credibility')
def credibility():
    return PLA_CRED_BP_PROMPT

@bp.route('/credibility/summary')
def credibility_summary():
    return PLA_CRED_BP_SUMMARY

@bp.route('/problems')
def problems():
    return PLA_PROB_BP_PROMPT

@bp.route('/problems/summary')
def problems_summary():
    return PLA_PROB_BP_SUMMARY
