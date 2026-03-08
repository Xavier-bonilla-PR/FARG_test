#!/usr/bin/env python3
"""Test slipnet activation spreading for numerical proximity."""

import sys
sys.path.insert(0, '/home/user/FARG_test/FARGish')

from Slipnet import NumericSlipnet, NumberNode
from Numbo1 import Numbo, Want, plus, Consume
from FARGish2 import SeqCanvas, SeqState

def test_number_nodes():
    """Test that number nodes are created with proximity links."""
    print("=" * 60)
    print("Test 1: Number nodes and proximity links")
    print("=" * 60)

    slipnet = NumericSlipnet()
    slipnet.add_number_nodes(lb=1, ub=30)

    # Check that nodes exist
    node_15 = NumberNode(15)
    node_14 = NumberNode(14)
    node_10 = NumberNode(10)

    assert node_15 in slipnet.nodes, "Node 15 should exist"
    assert node_14 in slipnet.nodes, "Node 14 should exist"

    # Check proximity links
    weight_14 = slipnet.weight(node_15, node_14)
    weight_10 = slipnet.weight(node_15, node_10)

    print(f"Weight from 15 to 14 (distance 1): {weight_14:.3f}")
    print(f"Weight from 15 to 10 (distance 5): {weight_10:.3f}")

    assert weight_14 > 0, "Should have link from 15 to 14"
    assert weight_14 > weight_10, "Closer numbers should have higher weight"

    print("✓ Number nodes and proximity links working correctly\n")

def test_activation_spreading():
    """Test that activation spreads from target to nearby numbers."""
    print("=" * 60)
    print("Test 2: Activation spreading from target")
    print("=" * 60)

    slipnet = NumericSlipnet()
    slipnet.add_number_nodes(lb=1, ub=30)

    # Set target 15 and spread activation
    target = 15
    activations = slipnet.set_target_activation(target, activation=1.0)

    # Check activations at various distances
    act_15 = slipnet.get_number_activation(15, activations)
    act_14 = slipnet.get_number_activation(14, activations)
    act_16 = slipnet.get_number_activation(16, activations)
    act_10 = slipnet.get_number_activation(10, activations)
    act_25 = slipnet.get_number_activation(25, activations)

    print(f"Activation at target (15): {act_15:.4f}")
    print(f"Activation at distance 1 (14): {act_14:.4f}")
    print(f"Activation at distance 1 (16): {act_16:.4f}")
    print(f"Activation at distance 5 (10): {act_10:.4f}")
    print(f"Activation at distance 10 (25): {act_25:.4f}")

    # Target should have highest activation
    assert act_15 >= act_14, "Target should have highest activation"
    assert act_14 > act_10, "Closer numbers should have more activation"
    assert act_10 > act_25, "Very distant numbers should have less activation"

    print("✓ Activation spreading working correctly\n")

def test_promisingness():
    """Test that operations producing activated numbers get higher support."""
    print("=" * 60)
    print("Test 3: Promisingness based on slipnet activation")
    print("=" * 60)

    # Create Numbo model
    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    # Create two Consume operations:
    # 1. (4 + 11) = 15  <- should have HIGH promisingness (result = target)
    # 2. (4 x 11) = 44  <- should have LOW promisingness (result far from target)

    consume_good = Consume(operator=plus, operands=(4, 11))
    consume_bad = Consume(operator=plus, operands=(20, 24))

    prom_good = wa.promisingness_of(fm, consume_good)
    prom_bad = wa.promisingness_of(fm, consume_bad)

    print(f"Promisingness of (4 + 11) = 15: {prom_good:.4f}")
    print(f"Promisingness of (20 + 24) = 44: {prom_bad:.4f}")

    assert prom_good > prom_bad, \
        f"Operation producing target should be more promising! ({prom_good:.4f} vs {prom_bad:.4f})"

    print(f"✓ Ratio: {prom_good/prom_bad:.2f}x more promising")
    print("✓ Slipnet-based promisingness working correctly\n")

def test_gradient():
    """Test that promisingness forms a gradient toward target."""
    print("=" * 60)
    print("Test 4: Promisingness gradient toward target")
    print("=" * 60)

    fm = Numbo()
    ca = fm.build(SeqCanvas([SeqState((4, 5, 6), None)]))
    wa = fm.build(Want(15, canvas=ca, addr=0))

    # Test operations producing results at various distances from target
    test_cases = [
        ((1, 14), 15, "exact match"),
        ((1, 13), 14, "distance 1"),
        ((1, 15), 16, "distance 1"),
        ((1, 9), 10, "distance 5"),
        ((1, 19), 20, "distance 5"),
        ((1, 29), 30, "distance 15"),
    ]

    results = []
    for operands, result, label in test_cases:
        consume = Consume(operator=plus, operands=operands)
        prom = wa.promisingness_of(fm, consume)
        results.append((result, prom, label))
        print(f"Result {result:2d} ({label:12s}): promisingness = {prom:.4f}")

    # Check that exact match has highest promisingness
    exact_prom = results[0][1]
    assert all(exact_prom >= prom for _, prom, _ in results), \
        "Exact match should have highest promisingness"

    print("✓ Promisingness gradient working correctly\n")

if __name__ == '__main__':
    test_number_nodes()
    test_activation_spreading()
    test_promisingness()
    test_gradient()

    print("=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
    print("\nSlipnet-driven evaluation is working correctly.")
    print("Operations producing numbers near the target receive higher support")
    print("based on slipnet activation, not hard-coded thresholds.")
