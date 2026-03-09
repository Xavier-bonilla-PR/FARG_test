#!/usr/bin/env python3
"""Test if the operator-pattern approach helps solve multi-step problems."""

import sys
sys.path.insert(0, 'FARGish')

from Numbo1 import (
    Numbo, Want, Consume, SeqCanvas, SeqState, SolvedNumble
)

def test_easy_solution():
    """Test a simple problem that should be solved easily."""
    print("\n=== Easy Problem: [4, 5, 6] -> 10 ===\n")

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(10, canvas=ca, addr=0))

    print(f"Problem: {ca[0].avails} -> {wa.target}")
    print("Expected: 4 + 6 = 10")

    try:
        for i in range(50):
            fm.do_timestep()
            if i % 10 == 0:
                print(f"  Timestep {i}...")
    except SolvedNumble as e:
        print(f"\n✓ SOLVED at timestep {i}!")
        print(f"  Solution: {e}")
        return True

    print("\n✗ Not solved within 50 timesteps")
    return False


def test_with_large_number():
    """Test problem with a large number: [4, 11] -> 15"""
    print("\n=== Large Number Problem: [4, 11] -> 15 ===\n")

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 11), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"Problem: {ca[0].avails} -> {wa.target}")
    print("Expected: 11 + 4 = 15")

    try:
        for i in range(100):
            fm.do_timestep()
            if i % 20 == 0:
                print(f"  Timestep {i}...")
    except SolvedNumble as e:
        print(f"\n✓ SOLVED at timestep {i}!")
        print(f"  Solution: {e}")
        return True

    print("\n✗ Not solved within 100 timesteps")

    # Show what Consume agents were created
    consumes = list(fm.elems(Consume))
    print(f"\nCreated {len(consumes)} Consume agents:")
    for c in consumes[:20]:
        print(f"  {c.operator}{c.operands}")

    return False


def test_multi_step_problem():
    """Test a problem requiring multiple steps: [4, 5, 6, 11] -> 15"""
    print("\n=== Multi-Step Problem: [4, 5, 6, 11] -> 15 ===\n")

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6, 11), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"Problem: {ca[0].avails} -> {wa.target}")
    print("Possible solutions:")
    print("  - 11 + 4 = 15 (direct)")
    print("  - 5 + 6 = 11, then find 4 somewhere (multi-step)")

    try:
        for i in range(200):
            fm.do_timestep()
            if i % 50 == 0:
                print(f"  Timestep {i}...")
    except SolvedNumble as e:
        print(f"\n✓ SOLVED at timestep {i}!")
        print(f"  Solution: {e}")
        return True

    print("\n✗ Not solved within 200 timesteps")

    # Show what Consume agents were created
    consumes = list(fm.elems(Consume))
    print(f"\nCreated {len(consumes)} Consume agents (showing first 30):")
    for c in consumes[:30]:
        print(f"  {c.operator}{c.operands} from {c.source}")

    return False


if __name__ == '__main__':
    results = []

    results.append(("Easy problem", test_easy_solution()))
    results.append(("Large number problem", test_with_large_number()))
    results.append(("Multi-step problem", test_multi_step_problem()))

    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    for name, solved in results:
        status = "✓ SOLVED" if solved else "✗ UNSOLVED"
        print(f"{status}: {name}")
    print("="*60)
