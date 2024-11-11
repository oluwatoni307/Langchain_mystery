from flask import Blueprint, request, jsonify
from phases.Kouhei import kouhei_backstory
from phases.susumu import susumu_backstory
from phases.masami import masami_backstory
from phases.cues import *

from phases.prompt  import *
# Create a Blueprint for the update API
update_api = Blueprint('api', __name__)

# Initial values for backstory, summary, and current_phase


# Route to update the backstory
@update_api.route('/Kouhei_backstory', methods=['POST'])
def Kouhei_backstory():
    global kouhei_backstory
    kouhei_backstory = request.json.get('backstory', kouhei_backstory)
    return jsonify({"status": "success", "message": "Backstory updated successfully"})

@update_api.route('/susumu_backstory', methods=['POST'])
def Susumu_backstory():
    global susumu_backstory
    susumu_backstory = request.json.get('backstory', susumu_backstory)
    return jsonify({"status": "success", "message": "Backstory updated successfully"})

@update_api.route('/masami_backstory', methods=['POST'])
def Masami_backstory():
    global masami_backstory
    masami_backstory = request.json.get('backstory', masami_backstory)
    return jsonify({"status": "success", "message": "Backstory updated successfully"})

# clues
@update_api.route('/general_clues', methods=['POST'])
def update_clues():
    global cue
    cue = request.json.get('cue', cue)
    return jsonify({"status": "success", "message": "cue updated successfully"})

@update_api.route('/personal_clues', methods=['POST'])
def update_personal_cues():
    global personal_cues
    personal_cues = request.json.get('personal_cues', personal_cues)
    return jsonify({"status": "success", "message": "personal_cues updated successfully"})























# Phase prompt
# Route to update the phase_1_prompt
@update_api.route('/phase_1_prompt', methods=['POST'])
def phase_1_prompt():
    global phase_1_prompt
    phase_1_prompt = request.json.get('phase_1_prompt', phase_1_prompt)
    return jsonify({"status": "success", "message": "phase_1_prompt updated successfully"})

# Route to update the phase_2_prompt
@update_api.route('/phase_2_prompt', methods=['POST'])
def phase_2_prompt():
    global phase_2_prompt
    phase_2_prompt = request.json.get('phase_2_prompt', phase_2_prompt)
    return jsonify({"status": "success", "message": "phase_2_prompt updated successfully"})

# Route to update the phase_3_prompt
@update_api.route('/phase_3_prompt', methods=['POST'])
def phase_3_prompt():
    global phase_3_prompt
    phase_3_prompt = request.json.get('phase_3_prompt', phase_3_prompt)
    return jsonify({"status": "success", "message": "phase_3_prompt updated successfully"})

# Route to update the phase_4_prompt
@update_api.route('/phase_4_prompt', methods=['POST'])
def phase_4_prompt():
    global phase_4_prompt
    phase_4_prompt = request.json.get('phase_4_prompt', phase_4_prompt)
    return jsonify({"status": "success", "message": "phase_4_prompt updated successfully"})

# Route to update the phase_2_prompt
@update_api.route('/phase_5_prompt', methods=['POST'])
def phase_5_prompt():
    global phase_5_prompt
    phase_5_prompt = request.json.get('phase_5_prompt', phase_5_prompt)
    return jsonify({"status": "success", "message": "phase_5_prompt updated successfully"})
