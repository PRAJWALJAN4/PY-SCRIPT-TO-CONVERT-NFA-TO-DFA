import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class NFA_DFA_GUI:
    def __init__(self, master):
        self.master = master
        master.title("NFA & DFA Visualizer")
        master.geometry("700x600")

        # GUI Elements
        ttk.Label(master, text="NFA & DFA Visualizer", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        self.upload_btn = ttk.Button(master, text="Upload NFA CSV", command=self.load_csv)
        self.upload_btn.pack(pady=5)
        
        self.plot_nfa_btn = ttk.Button(master, text="Plot NFA", command=self.plot_nfa, state="disabled")
        self.plot_nfa_btn.pack(pady=5)
        
        self.plot_dfa_btn = ttk.Button(master, text="Plot DFA", command=self.plot_dfa, state="disabled")
        self.plot_dfa_btn.pack(pady=5)
        
        self.step_btn = ttk.Button(master, text="Show DFA Transitions", command=self.next_step, state="disabled")
        self.step_btn.pack(pady=5)
        
        self.reset_btn = ttk.Button(master, text="Reset Steps", command=self.reset_steps, state="disabled")
        self.reset_btn.pack(pady=5)
        
        self.status = ttk.Label(master, text="Upload CSV file to begin", foreground="blue")
        self.status.pack(pady=15)

        # Data storage
        self.file_path = None
        self.nfa = None
        self.dfa = None
        self.dfa_accept_states = set()
        self.steps = []
        self.current_step = 0

    def load_csv(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            try:
                self.nfa = self.load_nfa_from_csv(self.file_path)
                self.dfa, self.dfa_accept_states = self.convert_nfa_to_dfa()
                self.steps = self.get_dfa_steps()
                self.current_step = 0
                self.update_ui_state(True)
                self.status.config(text="CSV loaded successfully!", foreground="green")
            except Exception as e:
                self.status.config(text=f"Error: {str(e)}", foreground="red")
                self.update_ui_state(False)

    def load_nfa_from_csv(self, csv_path):
        try:
            # Read CSV with proper formatting
            df = pd.read_csv(
                csv_path,
                delimiter=",",
                quotechar='"',
                skipinitialspace=True,
                dtype=str,
                keep_default_na=False
            )
            
            # Validate columns
            required = ['current_state', 'input_symbol', 'next_states']
            missing = [col for col in required if col not in df.columns]
            if missing:
                raise ValueError(f"Missing columns: {missing}")

            # Process transitions
            transitions = {}
            all_states = set()
            alphabet = set()
            
            for _, row in df.iterrows():
                src = row['current_state'].strip()
                symbol = row['input_symbol'].strip()
                dests = [s.strip() for s in row['next_states'].split(',') if s.strip()]
                
                transitions.setdefault(src, {}).setdefault(symbol, set()).update(dests)
                all_states.update([src] + dests)
                if symbol != 'ε':
                    alphabet.add(symbol)

            # Validate start state
            start_state = df['current_state'].iloc[0].strip()
            if start_state not in all_states:
                raise ValueError("Start state not found in transitions")

            return {
                'states': all_states,
                'alphabet': alphabet,
                'transitions': transitions,
                'start_state': start_state,
                'accept_states': {'q₁'}  # Update according to your CSV
            }
            
        except Exception as e:
            raise ValueError(f"CSV Error: {str(e)}")

    def epsilon_closure(self, states):
        closure = set(states)
        queue = deque(states)
        
        while queue:
            state = queue.popleft()
            epsilon_trans = self.nfa['transitions'].get(state, {}).get('ε', set())
            for s in epsilon_trans:
                if s not in closure:
                    closure.add(s)
                    queue.append(s)
        return closure

    def convert_nfa_to_dfa(self):
        dfa_trans = {}
        dfa_accept = set()
        initial = self.epsilon_closure({self.nfa['start_state']})
        queue = deque([frozenset(initial)])
        seen = {frozenset(initial)}

        while queue:
            current = queue.popleft()
            dfa_trans[current] = {}

            # Check if any state is accepting
            if any(s in self.nfa['accept_states'] for s in current):
                dfa_accept.add(frozenset(current))

            for symbol in self.nfa['alphabet']:
                move = set()
                for state in current:
                    move.update(self.nfa['transitions'].get(state, {}).get(symbol, set()))
                closure = self.epsilon_closure(move)
                closure_frozen = frozenset(closure)
                
                dfa_trans[current][symbol] = closure_frozen
                
                if closure_frozen not in seen:
                    seen.add(closure_frozen)
                    queue.append(closure_frozen)

        return dfa_trans, dfa_accept

    def format_state(self, state):
        if not state:
            return "∅"
        return "{" + ", ".join(sorted(state)) + "}"

    def plot_nfa(self):
        G = nx.DiGraph()
        for src, trans in self.nfa['transitions'].items():
            for symbol, dests in trans.items():
                for dest in dests:
                    G.add_edge(src, dest, label=symbol)
        
        self.draw_graph(G, "NFA Graph", 'lightblue')

    def plot_dfa(self):
        G = nx.DiGraph()
        for state, trans in self.dfa.items():
            src = self.format_state(state)
            for symbol, dest in trans.items():
                dest_str = self.format_state(dest)
                G.add_edge(src, dest_str, label=symbol)
        
        self.draw_graph(G, "DFA Graph", 'lightgreen')

    def draw_graph(self, graph, title, color):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=2500,
                node_color=color, font_size=12, arrows=True)
        nx.draw_networkx_edge_labels(graph, pos, 
                                    edge_labels=nx.get_edge_attributes(graph, 'label'),
                                    font_color='darkred')
        plt.title(title)
        plt.show()

    def get_dfa_steps(self):
        steps = []
        for state, trans in self.dfa.items():
            for symbol, dest in trans.items():
                steps.append(
                    f"{self.format_state(state)} --{symbol}--> {self.format_state(dest)}"
                )
        return steps

    def next_step(self):
        if self.current_step < len(self.steps):
            self.status.config(text=self.steps[self.current_step])
            self.current_step += 1
        else:
            self.status.config(text="End of transitions list")

    def reset_steps(self):
        self.current_step = 0
        self.status.config(text="Steps reset to beginning")

    def update_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.plot_nfa_btn.config(state=state)
        self.plot_dfa_btn.config(state=state)
        self.step_btn.config(state=state)
        self.reset_btn.config(state=state)

if __name__ == "__main__":
    root = tk.Tk()
    app = NFA_DFA_GUI(root)
    root.mainloop()