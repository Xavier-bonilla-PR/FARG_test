#!/usr/bin/env python3
"""Test if hybrid slipnet approach solves multi-step problems."""

import sys
sys.path.insert(0, '/home/user/FARG_test/FARGish')

from Numbo1 import Numbo

def test_solve(bricks, target, seed, max_timesteps=100):
    """Test if a problem is solved within max timesteps."""
    try:
        result = Numbo.run(
            bricks=bricks,
            target=target,
            seed=seed,
            max_timesteps=max_timesteps,
            log=False,
            pulse_slipnet=True
        )
        return result.final_result == target
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    print("Testing hybrid slipnet with multi-step problems")
    print("=" * 60)

    # Problems requiring multi-step solutions
    test_cases = [
        ((4, 5, 6), 15, "requires 4+5=9, 9+6=15 OR 5+6=11, 11+4=15"),
        ((4, 5, 6), 14, "requires 5+6=11 or 5+4=9, then operate"),
        ((3, 4, 7), 10, "requires 3+7=10 or 7-4=3, 3+3=... wait this needs duplication"),
    ]

    seeds = [42, 123, 456, 789, 999]

    for bricks, target, description in test_cases:
        print(f"\nProblem: {bricks} -> {target}")
        print(f"Strategy: {description}")
        print("-" * 60)

        solved_count = 0
        for seed in seeds:
            solved = test_solve(bricks, target, seed, max_timesteps=100)
            status = "✓ SOLVED" if solved else "✗ Not solved"
            print(f"  Seed {seed:4d}: {status}")
            if solved:
                solved_count += 1

        print(f"  Result: {solved_count}/{len(seeds)} seeds solved")

    print("\n" + "=" * 60)
    print("Test complete")

if __name__ == '__main__':
    main()
