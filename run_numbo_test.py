#!/usr/bin/env python3
"""Run Numbo with slipnet-driven evaluation on (4,5,6) -> 15"""

import sys
sys.path.insert(0, '/home/user/FARG_test/FARGish')

from Numbo1 import Numbo, Want, Consume, r4_5_6__15
from FARGish2 import SeqCanvas, SeqState, pr
from util import first

def run_numbo_with_reporting():
    """Run Numbo and report on the promisingness values."""
    print("=" * 70)
    print("NUMBO TEST: (4, 5, 6) -> 15 with Slipnet-Driven Evaluation")
    print("=" * 70)
    print()

    # Create Numbo model
    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    # Run a few timesteps to let Want build some Consume agents
    print("Running initialization...")
    fm.do_timestep(num=3)

    # Get the Want agent
    want = first(fm.elems(Want))

    # Find all Consume agents
    consumes = list(fm.elems(Consume))

    if not consumes:
        print("No Consume agents built yet. Running more timesteps...")
        fm.do_timestep(num=5)
        consumes = list(fm.elems(Consume))

    print(f"\nFound {len(consumes)} Consume agents")
    print("\nPromisingness evaluation:")
    print("-" * 70)

    # Evaluate promisingness for each
    evals = []
    for consume in consumes[:20]:  # Limit to first 20 for readability
        if consume.operator and consume.operands:
            result = consume.operator.call(*consume.operands)
            prom = want.promisingness_of(fm, consume)
            evals.append((prom, consume, result))

    # Sort by promisingness (descending)
    evals.sort(reverse=True, key=lambda x: x[0])

    print(f"{'Promisingness':<15} {'Operation':<20} {'Result':<10} {'Distance from 15'}")
    print("-" * 70)

    for prom, consume, result in evals[:15]:  # Show top 15
        dist = abs(result - 15)
        op_str = f"{consume.operator} {consume.operands}"
        print(f"{prom:<15.4f} {op_str:<20} {result:<10} {dist}")

    print()
    print("=" * 70)
    print("OBSERVATIONS:")
    print("=" * 70)

    # Check if operations producing 15 are at the top
    top_results = [r for _, _, r in evals[:5]]
    if 15 in top_results:
        print("✓ Operations producing target (15) are among the most promising!")
    else:
        print("✗ Operations producing target (15) NOT in top 5")

    # Check gradient
    if len(evals) >= 5:
        distances = [abs(r - 15) for _, _, r in evals[:5]]
        avg_dist_top5 = sum(distances) / len(distances)

        distances_bottom = [abs(r - 15) for _, _, r in evals[-5:]]
        avg_dist_bottom5 = sum(distances_bottom) / len(distances_bottom)

        print(f"✓ Average distance from target in top 5: {avg_dist_top5:.1f}")
        print(f"✓ Average distance from target in bottom 5: {avg_dist_bottom5:.1f}")

        if avg_dist_top5 < avg_dist_bottom5:
            print("✓ Gradient working: top operations are closer to target!")
        else:
            print("✗ Gradient not working as expected")

    print()
    print("=" * 70)
    print("Now running full simulation to attempt solving...")
    print("=" * 70)
    print()

    # Run full simulation
    try:
        fm.do_timestep(num=30)
        print("\nFinal state:")
        pr(fm, edges=False)
    except Exception as e:
        if "SolvedNumble" in str(type(e).__name__):
            print(f"\n✓✓✓ SOLUTION FOUND! ✓✓✓")
            print(f"Solution: {e}")
        else:
            print(f"\nException: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nRandom seed: {fm.seed}")

if __name__ == '__main__':
    run_numbo_with_reporting()
