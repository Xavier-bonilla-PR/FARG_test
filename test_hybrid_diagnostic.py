#!/usr/bin/env python3
"""Diagnostic to verify hybrid slipnet construction."""

import sys
sys.path.insert(0, '/home/user/FARG_test/FARGish')

from Numbo1 import Numbo, Want, Consume, GettingCloser
from FARGish2 import ImCell, SeqCanvas, SeqState, Halt

def test_hybrid_construction():
    """Test that large-number operations are constructed directly."""
    print("=" * 60)
    print("HYBRID SLIPNET DIAGNOSTIC")
    print("=" * 60)

    # Problem: (4, 5, 6) -> 15
    # Should imagine 5+6=11 or 5+4=9, tag with GettingCloser,
    # then directly construct operations like 11+4=15 or 9+6=15

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    print("\n1. Initial state")
    print(f"   Canvas: {ca[0].avails}")
    print(f"   Target: 15")

    # Run a few timesteps to let agents build
    for i in range(10):
        fm.do_timestep()

    # Check if ImCells exist
    imcells = list(fm.elems(ImCell))
    print(f"\n2. After 10 timesteps:")
    print(f"   ImCells created: {len(imcells)}")

    if imcells:
        for ic in imcells[:5]:  # Show first 5
            if hasattr(ic, 'contents') and hasattr(ic.contents, 'avails'):
                print(f"     {ic.contents.avails}")
            elif hasattr(ic, 'avails'):
                print(f"     {ic.avails}")

    # Check for GettingCloser tags
    gc_tags = list(fm.elems(GettingCloser))
    print(f"\n3. GettingCloser tags: {len(gc_tags)}")

    if gc_tags:
        for tag in gc_tags[:3]:
            print(f"     Target {tag.target}: {tag.taggee}")
            if isinstance(tag.taggee, ImCell) and hasattr(tag.taggee.contents, 'avails'):
                avails = tag.taggee.contents.avails
                large = [a for a in avails if a > 10]
                print(f"       Avails: {avails}, Large: {large}")

    # Run more timesteps
    for i in range(20):
        fm.do_timestep()

    # Check Consume agents built for large numbers
    consume_agents = [a for a in fm.elems(Consume)]
    print(f"\n4. After 30 total timesteps:")
    print(f"   Total Consume agents: {len(consume_agents)}")

    # Look for operations involving numbers >10
    large_ops = []
    for agent in consume_agents:
        if hasattr(agent, 'operands') and agent.operands:
            a, b = agent.operands
            if a is not None and b is not None and (a > 10 or b > 10):
                large_ops.append(agent)

    print(f"   Consume agents with operands >10: {len(large_ops)}")

    if large_ops:
        print("\n   Examples of large-number operations:")
        for agent in large_ops[:10]:
            a, b = agent.operands
            try:
                result = agent.operator.call(a, b)
            except:
                result = None
            print(f"     {agent.operator.name} ({a}, {b}) = {result}")

    # Continue running to see if it solves
    print("\n5. Running to completion...")
    try:
        for _ in range(70):  # Run remaining timesteps (total 100)
            fm.do_timestep()

        final_state = ca[0]
        if hasattr(final_state, 'result') and final_state.result == 15:
            print(f"   ✓ SOLVED in {fm.t} timesteps!")
            print(f"   Solution: {final_state}")
        else:
            print(f"   ✗ Not solved after {fm.t} timesteps")
            print(f"   Final state: {final_state}")
    except Halt as h:
        final_state = ca[0]
        if hasattr(final_state, 'result') and final_state.result == 15:
            print(f"   ✓ SOLVED in {fm.t} timesteps!")
            print(f"   Solution: {final_state}")
        else:
            print(f"   ✗ Not solved")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == '__main__':
    test_hybrid_construction()
