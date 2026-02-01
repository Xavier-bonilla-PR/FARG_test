#!/usr/bin/env python3
"""
Simplified Numbo Visualizer - Makes the output easier to understand

This runs Numbo step-by-step and shows key information at each timestep.
"""

from dataclasses import dataclass
from typing import List, Dict
import sys

# Import from Numbo1.py
from Numbo1 import Numbo, SeqCanvas, SeqState, Want, Consume, ImCell
from FARGish2 import FARGModel

def clear_screen():
    """Clear terminal screen"""
    print('\033[2J\033[H', end='')

def print_header(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def show_workspace(fm: FARGModel):
    """Show the current workspace state"""
    print_header("WORKSPACE STATE")

    # Show canvas states
    canvases = list(fm.elems(SeqCanvas))
    for i, canvas in enumerate(canvases):
        print(f"\nCanvas {i}: {canvas}")

    # Show what operations have been performed
    cells = list(fm.elems(ImCell))
    if cells:
        print("\nOperations performed:")
        for cell in cells:
            print(f"  • {cell}")
    else:
        print("\nNo operations yet")

def show_goal(fm: FARGModel):
    """Show the goal"""
    wants = list(fm.elems(Want))
    if wants:
        print_header(f"GOAL: Reach {wants[0].target}")

def show_top_agents(fm: FARGModel, n=5):
    """Show the most active agents"""
    print_header(f"TOP {n} ACTIVE AGENTS")

    # Get all Consume agents with their activation
    agents = []
    for agent in fm.elems(Consume):
        activation = fm.a(agent)
        agents.append((activation, agent))

    # Sort by activation and show top N
    agents.sort(reverse=True, key=lambda x: x[0])

    if agents:
        print("\nActivation | Agent")
        print("-" * 60)
        for activation, agent in agents[:n]:
            print(f"  {activation:6.3f}   | {agent}")
    else:
        print("\nNo agents yet")

def show_summary(fm: FARGModel):
    """Show a summary of the current state"""
    print_header(f"TIMESTEP {fm.t} SUMMARY")

    # Count different types of elements
    n_consume = len(list(fm.elems(Consume)))
    n_cells = len(list(fm.elems(ImCell)))
    n_canvas = len(list(fm.elems(SeqCanvas)))

    print(f"\nTotal Consume agents: {n_consume}")
    print(f"Operations completed: {n_cells}")
    print(f"Canvas states: {n_canvas}")

def run_interactive():
    """Run Numbo step-by-step interactively"""
    print_header("NUMBO INTERACTIVE VISUALIZER")
    print("\nProblem: Use (4, 5, 6) to make 15")
    print("\nCommands:")
    print("  [Enter] = next timestep")
    print("  'r' = run to completion")
    print("  'q' = quit")

    # Create the model
    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    running = False

    while fm.t < 40:  # Max timesteps
        if not running:
            print("\n" + "="*60)
            input("\nPress Enter for next step (or 'r' to run, 'q' to quit)> ")

        # Do one timestep
        fm.do_timestep()

        # Show current state
        clear_screen()
        show_goal(fm)
        show_workspace(fm)
        show_top_agents(fm, n=8)
        show_summary(fm)

        # Check if solved
        cells = list(fm.elems(ImCell))
        for cell in cells:
            if hasattr(cell, 'result') and cell.result == 15:
                print_header("SOLUTION FOUND!")
                print(f"\n{cell}")
                return

        if not running:
            cmd = input("\nNext command> ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 'r':
                running = True

def run_simplified(seed=None):
    """Run with simplified output"""
    print_header("NUMBO SIMPLIFIED RUN")
    print("\nProblem: Use (4, 5, 6) to make 15\n")

    # Create the model
    fm = Numbo(seed=seed)
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print("Running...\n")

    for step in range(40):
        fm.do_timestep()

        # Show only when something interesting happens
        cells = list(fm.elems(ImCell))
        if len(cells) > step:  # New operation performed
            latest = cells[-1]
            print(f"t={fm.t:3d}: {latest}")

            # Check if solved
            if hasattr(latest, 'result') and latest.result == 15:
                print_header("SOLUTION FOUND!")
                return

    print("\nReached max timesteps without solution")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        run_interactive()
    else:
        run_simplified(seed=23686273699696067)
