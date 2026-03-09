#!/usr/bin/env python3
"""Debug: Check what Consume agents are actually built."""

import sys
sys.path.insert(0, 'FARGish')

from Numbo1 import (
    Numbo, Want, Consume, SeqCanvas, SeqState
)

def test_consume_creation():
    """Check if (4, 11) Consume agents are built."""
    print("\n=== Debugging Consume Agent Creation ===\n")

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 11), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"Problem: {ca[0].avails} -> {wa.target}\n")

    # Run for a bit
    for i in range(20):
        fm.do_timestep()

    # Check all Consume agents
    consumes = list(fm.elems(Consume))
    print(f"Total Consume agents: {len(consumes)}\n")

    # Group by operands
    by_operands = {}
    for c in consumes:
        ops = c.operands
        if ops not in by_operands:
            by_operands[ops] = []
        by_operands[ops].append((c.operator, c.source))

    print("Grouped by operands:")
    for ops in sorted(by_operands.keys(), key=lambda x: (x is None, str(x))):
        agents = by_operands[ops]
        print(f"\n  Operands {ops}: {len(agents)} agents")
        for op, src in agents[:3]:  # Show first 3
            print(f"    {op} from {src}")

    # Specifically check for (4, 11)
    has_4_11 = any(c.operands == (4, 11) for c in consumes)
    has_11_4 = any(c.operands == (11, 4) for c in consumes)

    print(f"\n✓ Has Consume with (4, 11): {has_4_11}")
    print(f"✓ Has Consume with (11, 4): {has_11_4}")

    # Show all (4, 11) agents if they exist
    for c in consumes:
        if c.operands in [(4, 11), (11, 4)]:
            print(f"  Found: {c.operator}{c.operands} from {c.source}")


if __name__ == '__main__':
    test_consume_creation()
