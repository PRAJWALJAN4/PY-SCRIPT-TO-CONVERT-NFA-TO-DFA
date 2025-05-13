# PY-SCRIPT-TO-CONVERT-NFA-TO-DFA
A Python tool to convert NFAs (Non-deterministic Finite Automata) to DFAs (Deterministic Finite Automata) and visualize them interactively.

📌 Aim of the Project
Core Objective:

Convert NFAs (with ε-transitions) to equivalent DFAs using subset construction.

Provide an intuitive GUI for step-by-step exploration of automata transitions.

Key Features:

📊 Visualize NFA/DFA graphs using networkx and matplotlib.

📂 Parse NFA definitions from CSV files.

🔍 Step-through mode for DFA transition debugging.

🛠️ Robust error handling for invalid inputs.

🚀 Steps to Use the Tool
1. Installation
bash
git clone https://github.com/your-username/nfa-dfa-converter.git
cd nfa-dfa-converter
pip install -r requirements.txt  # pandas networkx matplotlib
2. Run the GUI
bash
python nfa_dfa_converter.py
3. Load an NFA Definition
Click Upload NFA CSV and select a file (e.g., examples/nfa_1.csv).

CSV Format:

csv
current_state,input_symbol,next_states
q₀,0,"q₀,q₁"  # Non-deterministic transition
q₁,1,"q₁"     # Deterministic transition
q₁,0,""       # Dead state
4. Visualize Automata
Button	Action
Plot NFA	Renders the NFA graph with labeled edges.
Plot DFA	Generates and displays the equivalent DFA.
Show Transitions	Step through DFA transitions one at a time.
Reset Steps	Reset the transition walkthrough.
⚙️ Error Handling Techniques
The tool validates inputs and handles errors gracefully:

Error Type	Handling Mechanism
Missing CSV Columns	Checks for current_state, input_symbol, and next_states; raises ValueError.
Malformed CSV	Uses pandas.read_csv(quotechar='"') to handle quoted multi-state transitions.
Invalid States	Validates that all states in next_states exist in the NFA definition.
Empty Inputs	Treats empty next_states as dead states (∅ in DFA).
Example Error Message:

plaintext
Error: CSV is missing required columns: ['input_symbol']
