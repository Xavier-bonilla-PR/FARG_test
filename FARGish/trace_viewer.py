#!/usr/bin/env python3
"""
Trace Viewer - Parses and displays Numbo output in a cleaner format

This helps understand what's happening in the verbose output.
"""

import re
from collections import defaultdict

class NumboTrace:
    """Parse and format Numbo trace output"""

    def __init__(self):
        self.timestep = 0
        self.operations = []  # List of (timestep, operation, result)
        self.agents_created = []  # List of (timestep, agent, activation)

    def parse_line(self, line):
        """Parse a single line of output"""
        line = line.strip()
        if not line:
            return None

        # Look for completed operations (ImCell)
        if 'ImCell' in line:
            match = re.search(r'ImCell\((.*?)\)', line)
            if match:
                operation = match.group(1)
                return ('operation', operation)

        # Look for agent creation
        match = re.match(r'(\d+\.\d+)\s+(\w+\([^)]+\))', line)
        if match:
            activation = float(match.group(1))
            agent = match.group(2)
            return ('agent', activation, agent)

        # Look for goal
        if 'Want(' in line:
            match = re.search(r'Want\((\d+)\)', line)
            if match:
                target = int(match.group(1))
                return ('goal', target)

        # Look for solution
        if 'SolvedNumble' in line or 'SOLUTION' in line:
            return ('solution',)

        return None

    def format_summary(self):
        """Create a formatted summary"""
        lines = []
        lines.append("\n" + "="*60)
        lines.append("  NUMBO EXECUTION TRACE - SUMMARY")
        lines.append("="*60)

        if self.operations:
            lines.append("\n📊 OPERATIONS PERFORMED:")
            for i, op in enumerate(self.operations, 1):
                lines.append(f"  {i}. {op}")
        else:
            lines.append("\n📊 No operations completed yet")

        if self.agents_created:
            lines.append("\n🤖 TOP AGENTS BY ACTIVATION:")
            # Sort by activation
            top_agents = sorted(self.agents_created,
                              key=lambda x: x[1], reverse=True)[:10]
            for activation, agent in top_agents:
                lines.append(f"  {activation:6.3f} - {agent}")

        return "\n".join(lines)

def simple_trace(verbose=False):
    """
    Run Numbo with a simplified trace showing only key events.
    """
    from Numbo1 import Numbo, SeqCanvas, SeqState, Want, ImCell, Consume

    print("="*60)
    print("  NUMBO SIMPLE TRACE")
    print("="*60)
    print("\nProblem: Use (4, 5, 6) with +, -, × to make 15")
    print("-"*60)

    fm = Numbo(seed=23686273699696067)
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    prev_ops = 0

    for step in range(40):
        fm.do_timestep()

        # Check for new operations
        cells = list(fm.elems(ImCell))
        if len(cells) > prev_ops:
            for cell in cells[prev_ops:]:
                print(f"\n⚡ t={fm.t:2d}: {cell}")

                # Show activation level
                activation = fm.a(cell)
                print(f"   Activation: {activation:.3f}")

                # Check if this solves it
                if hasattr(cell, 'result'):
                    if cell.result == 15:
                        print("\n" + "="*60)
                        print("  ✅ SOLUTION FOUND!")
                        print("="*60)
                        print(f"\nAnswer: {cell}")
                        return
                    else:
                        distance = abs(cell.result - 15)
                        print(f"   Distance from goal: {distance}")

            prev_ops = len(cells)

        if verbose and step % 5 == 0:
            n_agents = len(list(fm.elems(Consume)))
            print(f"\nt={fm.t:2d}: {n_agents} active agents")

    print("\n⏸️  Reached max timesteps")

if __name__ == '__main__':
    import sys

    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    simple_trace(verbose=verbose)
