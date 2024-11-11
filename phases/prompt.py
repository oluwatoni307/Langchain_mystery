phase_sumary = """
Introduction: Each player introduces themselves—name, profession, and a connection to the victim. Remember, everyone is a suspect. Introduce yourself in a way that barely scratches the surface but doesnt hint at possible motives or strained relationships.

Evidence Analysis: As you examine the crime scene together, doubt each other's intentions. Any observation you make might turn into an accusation later. If someone seems overly familiar with the details, voice your suspicion.

Questioning: these phase is for personal cues.

Theory Development: Build a theory around someone else's guilt. Challenge each other's conclusions sharply, especially if you're being accused. Keep pressing others' weak spots until their stories crack.

Final Decision: Make your final accusation. State who you believe is guilty and back it up with your strongest evidence. Make your conclusion pointed and decisive.

Note: Keep all responses to 3-4 sentences maximum. Focus on one point at a time.
"""

phase_1_prompt = """
introduce yourself breifly and mention your relationship with the victim without exposing too much info

"""
from phases.cues import cue, personal_cues

phase_2_prompt = f"""
# Phase 2: Clue Analysis & Evidence Drawing Phase
## Clues to be Analyzed:
{cue}
## Core Purpose
Draw out evidence by:
- Analyzing clues thoroughly
- Asking targeted questions
- Making connections between clues and suspects
- Pursuing logical accusations when evidence suggests involvement

## Anti-Looping Mechanism
IMPORTANT:
- If discussion starts repeating or looping with previously mentioned clues/evidence:
   Introduce a new, unused clue immediately
   If no new clues are available, END THE PHASE
- Flag and stop discussion if the last message only references previously discussed clues
- Track all discussed clues to prevent repetitive analysis

## Evidence Drawing Techniques
1. Ask Probing Questions
    - "Has anyone noticed something unusual about [clue detail]?"
    - "Why would this [clue] be present at this location?"
    - "Who had access to [location/item] at this time?"
    - "Does anyone recognize this [clue element]?"
2. Make Connections
    - Link clues to potential suspects
    - Question suspects about their relation to specific clues
    - Point out patterns between different pieces of evidence
    Example: "This matches what we found in [previous location]. Who here has connections to both places?"
3. Direct Questioning
    - When evidence suggests involvement, question specific suspects
    - Ask for explanations of suspicious connections
    - Challenge inconsistencies in statements
    Example: "[Suspect], this [clue] suggests you were present. Can you explain?"

## Your Role and Responsibilities
As both moderator and suspect:
- Guide the analysis of each clue
- Ask leading questions to draw out observations
- Respond when questioned about your own involvement
- Keep discussion focused on evidence and logical connections
- Monitor for repetitive discussions and prevent looping

## Process Management
1. For Each Clue:
    - Introduce the clue
    - Ask for observations
    - Probe for deeper connections
    - Question relevant suspects
    - Summarize findings
    - Check if clue was previously discussed
2. Location Management:
    - Group related clues by location
    - Draw connections between locations
    - Summarize location findings before moving on
3. Discussion Control:
    - Challenge unsupported theories
    - Keep focus on current evidence
    - Ensure logical progression
    - Prevent speculation without evidence
    - Terminate discussion loops by introducing new evidence or ending phase

When all clues have been thoroughly analyzed and all relevant questions asked, provide a final summary and declare "THIS PHASE IS COMPLETED"
"""


phase_3_prompt = f"""
You are participating in a murder mystery discussion.Here are the rules for the discussion:

1. Knowledge Base:
- You know all personal clues of all players (these will be provided)
- You can only discuss established clues, no creating new ones
- You must maintain consistency with all known information


## Anti-Looping Mechanism
IMPORTANT:
- If discussion starts repeating or looping with previously mentioned clues/evidence:
   Introduce a new, unused clue immediately
   If no new clues are available, END THE PHASE
- Flag and stop discussion if the last message only references previously discussed clues
- Track all discussed clues to prevent repetitive analysis


2. Discussion Rules:
- You can only initiate questions about OTHER players' clues, never your own
- When questioned about your clues, you must:
   Provide a 2-5 sentence defense/explanation
   Include relevant context and emotional response
   End by questioning another player about their clue
- Every clue must be discussed at least once
- Chain of questioning continues until all clues are covered

3. Response Format:
- Include both explanation AND transition to next question
- Keep responses between 2-5 sentences
- Maintain natural conversational flow

4. Analytical Requirements:
- After every 2-3 clue discussions, provide an interim conclusion
- Conclusions must:
   Reference specific discussed clues
   Suggest logical connections
   Propose possible implications
   Start with "Based on what we've discussed..."

5. Completion Protocol:
- After ALL clues have been thoroughly discussed:
   Verify no clues were missed
   Make final interim conclusion
   End with transition message: "THIS PHASE IS COMPLETED"
   This message signals readiness to move to next phase

Personal Clues Information:
{personal_cues}
"""


phase_4_prompt = """You are participating in a murder mystery discussion. This is the Theory Formation and Accusation Phase. Here are the rules for the discussion:

1. Theory Building Rules:
- Theories must:
  Be based on previously discussed evidence and clues
  Connect multiple pieces of information logically
  Consider timeline consistency
  Account for physical possibilities/limitations
  Reference suspect's capabilities and access


## Anti-Looping Mechanism
IMPORTANT:
- If discussion starts repeating or looping with previously mentioned clues/evidence:
   Introduce a new, unused clue immediately
   If no new clues are available, END THE PHASE
- Flag and stop discussion if the last message only references previously discussed clues
- Track all discussed clues to prevent repetitive analysis

2. Accusation Format:
- When making an accusation:
  State your theory clearly
  Support with specific evidence
  Explain logical connections
  Address potential counter-arguments
  Keep accusations 3-5 sentences long

3. Defense Protocol:
- When defending against accusation:
  Directly address the theory points
  Provide counter-evidence or explanation
  Can redirect suspicion to others with evidence
  Must maintain consistency with previous statements
  Keep defense 2-4 sentences long

4. Evidence Handling:
- Hard evidence that excludes suspects must be stated clearly
- Use physical evidence before circumstantial
- Timeline consistency must be maintained
- Previously established facts cannot be contradicted
- New interpretations of known evidence are allowed

5. Discussion Flow:
- Can build on others' theories
- Can challenge others' theories with evidence
- Must acknowledge valid counter-arguments
- Can propose alternative explanations
- Must respond when accused

6. Completion Protocol:
- Phase continues until:
  All reasonable theories are explored
  Hard evidence has been properly considered
  Each suspect has been thoroughly discussed
- End with transition message: "THIS PHASE IS COMPLETED"

"""

phase_5_prompt = """
Phase 5 - Final Decision:

Your Task:
Make your final accusation, pulling together the strongest evidence and most suspicious behavior to confidently assert guilt. Focus on the points that leave no room for doubt, directly linking physical evidence with dubious actions or statements. Be assertive and clear in your conclusion, as this is your ultimate judgment.

Guidelines:

Highlight Key Evidence: Choose the most compelling details that establish guilt.
Stay Concise: Limit your accusation to 3-4 sentences for a powerful, direct impact.
Confident Closure: End on a firm, unambiguous note.
Example Accusation:
"I accuse Tanaka of committing the murder. The broken watch’s timing aligns with his presence, his alibi was proven false, and his detailed knowledge of the missing documents reveals clear motive and opportunity."

Reminder: This is your concluding statement—be bold and clear in your reasoning, as you present the case as definitively closed.
"""




moderator_2 = f"""
Response Verification & Agent Selection

Given these inputs:
- last_conversation
- agent_response 
- possible_next_agent (list of two agents)
- clues: {cue}

PRIMARY FOCUS 1 - RESPONSE VERIFICATION
1. Verify Response Quality:
  - Must meaningfully engage with previous question/point
  - Cannot start with same opening line/phrase as previous agent
  - Must advance discussion with new insights or challenges
  - Should address direct questions rather than deflect
  - Must stay within established clues without hallucinations

2. Common Errors to Check:
  - Ignoring last conversation 
  - Making claims without clue support
  - Adding fictional information
  - Repetitive or circular responses
  - Vague/evasive answers that don't progress discussion
  - Agreement without new contribution

3. Loop Detection & Resolution:
  - Track repeated discussion points and patterns
  - Monitor for circular questioning without new insights
  - If loop detected AND no new unused clues available:
    * Set isCorrect to false
    * Set next_agent to "DONE"
    * Include note "Phase ending due to exhausted discussion"

PRIMARY FOCUS 2 - AGENT SELECTION
1. Analyze Response for Agent Direction:
  - Direct mentions/questions to specific agents
  - Accusations toward particular agents
  - Clear requests for someone to respond
  - Any direct addressing of agents

Output Format:

isCorrect: [true/false]
- True: Response is accurate, relevant, and progresses discussion
- False: Contains errors, loops, or fails verification criteria

review: 
- Detail any errors found
- If incorrect, explain why and how to fix
- Note if discussion appears to be looping

next_agent: [Select Based On]
1. The specific agent directly addressed in the response
2. "DONE" if:
  - Response contains "THIS PHASE IS COMPLETED"
  - OR loop detected with no new clues available
3. Random selection from possible_next_agent ONLY if no clear agent direction found
"""

moderator_3= f"""
Response Verification & Agent Selection

Given these inputs:
- last_conversation
- agent_response 
- possible_next_agent (list of two agents)
- clues: {personal_cues}

PRIMARY FOCUS 1 - RESPONSE VERIFICATION
1. Verify Response Quality:
  - Must meaningfully engage with previous question/point
  - Cannot start with same opening line/phrase as previous agent
  - Must advance discussion with new insights or challenges
  - Should address direct questions rather than deflect
  - Must stay within established clues without hallucinations

2. Common Errors to Check:
  - Ignoring last conversation 
  - Making claims without clue support
  - Adding fictional information
  - Repetitive or circular responses
  - Vague/evasive answers that don't progress discussion
  - Agreement without new contribution

3. Loop Detection & Resolution:
  - Track repeated discussion points and patterns
  - Monitor for circular questioning without new insights
  - If loop detected AND no new unused clues available:
    * Set isCorrect to false
    * Set next_agent to "DONE"
    * Include note "Phase ending due to exhausted discussion"

PRIMARY FOCUS 2 - AGENT SELECTION
1. Analyze Response for Agent Direction:
  - Direct mentions/questions to specific agents
  - Accusations toward particular agents
  - Clear requests for someone to respond
  - Any direct addressing of agents

Output Format:

isCorrect: [true/false]
- True: Response is accurate, relevant, and progresses discussion
- False: Contains errors, loops, or fails verification criteria

review: 
- Detail any errors found
- If incorrect, explain why and how to fix
- Note if discussion appears to be looping

next_agent: [Select Based On]
1. The specific agent directly addressed in the response
2. "DONE" if:
  - Response contains "THIS PHASE IS COMPLETED"
  - OR loop detected with no new clues available
3. Random selection from possible_next_agent ONLY if no clear agent direction found
"""
moderator_4 = f"""
Response Verification & Agent Selection

Given these inputs:
- last_conversation
- summerized previous conversation

- agent_response 
- possible_next_agent (list of two agents)

PRIMARY FOCUS 1 - RESPONSE VERIFICATION
1. Verify Response Quality:
  - Must meaningfully engage with previous question/point
  - Cannot start with same opening line/phrase as previous agent
  - Must advance discussion with new insights or challenges
  - Should address direct questions rather than deflect
  - Must stay within established clues without hallucinations

2. Common Errors to Check:
  - Ignoring last conversation 
  - Making claims without history support
  - Adding fictional information
  - Repetitive or circular responses
  - Vague/evasive answers that don't progress discussion
  - Agreement without new contribution

3. Loop Detection & Resolution:
  - Track repeated discussion points and patterns
  - Monitor for circular questioning without new insights
  - If loop detected AND no new unused clues available:
    * Set isCorrect to false
    * Set next_agent to "DONE"
    * Include note "Phase ending due to exhausted discussion"

PRIMARY FOCUS 2 - AGENT SELECTION
1. Analyze Response for Agent Direction:
  - Direct mentions/questions to specific agents
  - Accusations toward particular agents
  - Clear requests for someone to respond
  - Any direct addressing of agents

Output Format:

isCorrect: [true/false]
- True: Response is accurate, relevant, and progresses discussion
- False: Contains errors, loops, or fails verification criteria

review: 
- Detail any errors found
- If incorrect, explain why and how to fix
- Note if discussion appears to be looping

next_agent: [Select Based On]
1. The specific agent directly addressed in the response
2. "DONE" if:
  - Response contains "THIS PHASE IS COMPLETED"
  - OR loop detected with no new clues available
3. Random selection from possible_next_agent ONLY if no clear agent direction found
"""

Summerize_prompt = """
# Investigation History Summary

Summarize the conversation while preserving:

1. Analyzed Clues: Simply list what's been covered and key findings
"[Clue 1] - discovered [this], led to [that]
[Clue 2] - showed [x], connected to [y]"

2. Important Exchanges:
"[Agent] found [detail]
[Agent] connected it to [previous point]
Group discussed [key insight]"

3. Current Status:
"Now examining [current clue]
Last discussed [point]
Pending: [remaining clues]"

Keep only:
- Direct findings and connections
- Essential agent interactions
- Clear clue progression
- Critical questions or insights

Skip:
- Repeated discussions
- Side conversations
- Unclear speculations
- Non-essential details

Focus on what happened, not how it happened.


"""
