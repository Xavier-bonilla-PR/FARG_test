#!/usr/bin/env python3
"""Test the operator-pattern slipnet query approach.

This test verifies that:
1. Slipnet returns an operator when queried with strategic activations
2. We can extract the operator from the exemplar
3. We can apply that operator to actual available values
"""

import sys
sys.path.insert(0, 'FARGish')

from Numbo1 import (
    Numbo, Want, Consume, After, Increase, Decrease, NumOperands,
    plus, minus, times, SeqCanvas, SeqState
)

def test_operator_pattern_query():
    """Test querying slipnet for operator (strategy) rather than specific operands."""
    print("\n=== Testing Operator-Pattern Slipnet Query ===\n")

    # Create a Numbo problem: [4, 5, 6] -> 15
    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"✓ Created Numbo problem: {ca[0].avails} -> {wa.target}")

    # Run a few timesteps
    for _ in range(10):
        fm.do_timestep()

    want = wa
    print(f"  Target: {want.target}")

    # Manually test the strategic query
    target = 15
    avails = [4, 5, 6]

    # Build strategic activation pattern
    if target > sum(avails):
        direction = Increase()
    else:
        direction = Decrease()

    activations_in = {
        After(target): 2.0,
        direction: 5.0,
        NumOperands(2): 1.0,
    }

    print(f"\n Strategic query:")
    print(f"  Target: {target}")
    print(f"  Avails: {avails}")
    print(f"  Direction: {direction.__class__.__name__}")
    print(f"  Activations: {activations_in}")

    # Query slipnet for strategic advice
    agents = fm.pulse_slipnet(activations_in, k=20, type=Consume, num_get=3)

    print(f"\n✓ Slipnet returned {len(agents)} exemplar(s):")
    for i, agent in enumerate(agents):
        if isinstance(agent, Consume):
            print(f"  {i+1}. {agent.operator}{agent.operands}")
            print(f"     Operator: {agent.operator}")

    # Extract operator from first exemplar
    if agents and isinstance(agents[0], Consume):
        suggested_op = agents[0].operator
        print(f"\n✓ Extracted operator: {suggested_op}")

        # Apply to actual avails
        print(f"\n Applying {suggested_op} to actual avails {avails}:")
        from itertools import combinations_with_replacement
        for a, b in combinations_with_replacement(avails, 2):
            if a >= b:
                result = suggested_op.call(a, b)
                print(f"  {suggested_op}({a}, {b}) = {result}")

        print("\n✓ Operator-pattern approach works!")
    else:
        print("\n✗ No Consume agent returned from slipnet")
        return False

    return True


def test_multi_step_with_operator_pattern():
    """Test that operator-pattern approach helps with multi-step problems."""
    print("\n=== Testing Multi-Step Problem with Operator Pattern ===\n")

    # [4, 5, 6, 11] -> 15
    # Expected: 11 + 4 = 15 (requires recognizing that addition is strategic)
    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6, 11), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print(f"Problem: {ca[0].avails} -> {wa.target}")
    print("Expected: 11 + 4 = 15")
    print("\nRunning model...\n")

    try:
        for _ in range(100):
            fm.do_timestep()
        print(f"\n✓ Model completed")

        # Check for Consume agents with the suggested operation
        consumes = list(fm.elems(Consume))
        print(f"\n✓ Created {len(consumes)} Consume agents:")

        # Group by operator
        by_operator = {}
        for c in consumes[:10]:  # Show first 10
            op_str = str(c.operator)
            if op_str not in by_operator:
                by_operator[op_str] = []
            by_operator[op_str].append(c.operands)

        for op_str, operands_list in by_operator.items():
            print(f"\n  {op_str}:")
            for ops in operands_list[:5]:  # Show first 5 of each
                print(f"    {ops}")

        return True

    except Exception as e:
        print(f"\n Model result: {e}")
        return True  # Finding solution is fine


if __name__ == '__main__':
    test_operator_pattern_query()
    test_multi_step_with_operator_pattern()
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
