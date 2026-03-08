# Slipnet-Driven Promisingness Evaluation: Implementation Summary

## Overview

Implemented **Level 2: Evaluation with Slipnet Scoring** for Numbo's arithmetic problem-solving.

This replaces hard-coded proximity thresholds with **emergent evaluation based on slipnet activation**.

---

## What Changed

### Before (Hard-Coded Heuristic)
```python
def promisingness_of(elem):
    if elem.is_blocked:
        return 0.1
    else:
        return 0.2  # Fixed value!
```

**Problems:**
- No awareness of target
- All valid operations equally promising
- System explores randomly

---

### After (Slipnet-Driven)
```python
def promisingness_of(elem):
    result = elem.operator.call(*elem.operands)  # Simulate
    activation = slipnet.get_number_activation(result)  # Query slipnet
    return base_support + (activation * 2.0)  # Emergent!
```

**Benefits:**
- Operations producing target get 7x higher support
- Gradient toward target emerges naturally
- No hard-coded thresholds
- Still pragmatic (simulates results, doesn't require full factual links)

---

## Architecture

### 1. NumericSlipnet Class

**New slipnet with numerical knowledge:**

```python
class NumericSlipnet(IntFeatures):
    def add_number_nodes(self, lb=1, ub=100):
        """Add number nodes with proximity links"""
        # Create nodes for each number
        # Link nearby numbers with strength = 1/(1+distance)
```

**Key feature:** Proximity encoded as link weights, not code logic

---

### 2. Activation Spreading

**When Want is built:**
```python
def on_build(self, fm):
    # Set target activation and spread to nearby numbers
    self._target_activations = fm.slipnet.set_target_activation(self.target)
```

**Result:**
- Target (15) → activation = 0.60
- Distance 1 (14, 16) → activation = 0.03
- Distance 5 (10, 20) → activation = 0.01
- Distance 15 (30) → activation = 0.006

**Gradient emerges from slipnet structure!**

---

### 3. Promisingness Evaluation

**Want queries slipnet for result activation:**

```python
def promisingness_of(self, fm, elem):
    if isinstance(elem, Consume):
        result = elem.operator.call(*elem.operands)
        activation = fm.slipnet.get_number_activation(result, self._target_activations)
        return base_support + (activation * 2.0)
```

**Example:**
- `(4 + 11) = 15` → activation = 0.60 → support = **1.40**
- `(20 + 24) = 44` → activation = 0.0 → support = **0.20**
- **Ratio: 7x more promising for exact match**

---

## Test Results

All tests passed! ✓

### Test 1: Number Nodes and Proximity Links
```
Weight from 15 to 14 (distance 1): 0.500
Weight from 15 to 10 (distance 5): 0.167
✓ Closer numbers have higher link weights
```

### Test 2: Activation Spreading
```
Activation at target (15): 0.6017
Activation at distance 1 (14): 0.0258
Activation at distance 5 (10): 0.0096
✓ Activation decreases with distance from target
```

### Test 3: Promisingness Gradient
```
Promisingness of (4 + 11) = 15: 1.4020
Promisingness of (20 + 24) = 44: 0.2001
✓ 7.00x more promising for exact match
```

### Test 4: Full Gradient
```
Result 15 (exact match): 1.4020
Result 14 (distance 1):  0.2443
Result 20 (distance 5):  0.2161
Result 30 (distance 15): 0.2063
✓ Promisingness decreases with distance
```

---

## The Spectrum: Where Does This Sit?

```
Pure Search ← ──────────────────────── → Pure FARG
Algorithm                                 Emergence

Level 1:              Level 2:              Level 3:
Hard-Coded     →   Slipnet Scoring   →   Factual Links
Thresholds         (IMPLEMENTED)          (Future)

"if result==15:    "activation =          "slipnet has
 return 10.0"       slipnet[15]"          link: 15 is-sum-of
                                          (4,11)"
```

**We chose Level 2:**
- ✓ Emergent scoring (not hard-coded)
- ✓ Slipnet structure drives evaluation
- ✓ Pragmatic (doesn't require 15k factual links)
- ✗ Still simulates operations (calculates results)
- ✗ Not full FARG perception (Level 3 would be)

---

## Philosophical Position

### What We Said FARG Should Be:
> "Operations producing target should **LOOK** promising through perceptual activation"

### What We Built:
- ✓ Promisingness comes from slipnet activation (emergent)
- ✓ No magic numbers (proximity encoded in link structure)
- ✓ Gradient emerges naturally
- ✗ Still simulates results (not pure perception)

### Why This Is Pragmatic:
1. **Avoids combinatorial explosion** of arithmetic facts
2. **Still FARG-flavored**: slipnet guides evaluation
3. **Good example for LLM**: shows slipnet-driven scoring
4. **Works in practice**: 7x boost for promising operations

---

## Key Insight

**Before:** Hard-coded `if result == target: return 10.0`
**After:** Slipnet activation naturally makes target-producing operations promising

**The difference:**
- Hard-coding: "If you get 15, that's good"
- Emergence: "15 is highly activated, so operations producing it look good"

**Subtle but important:** Evaluation logic doesn't "know" about the target.
It only knows to prefer highly-activated numbers.
The target's activation makes it salient.

---

## What's Still Missing (Level 3)

To reach **true FARG perception**, we'd need:

### Arithmetic Facts as Slipnet Links
```python
# Instead of this:
result = operator.call(4, 11)  # Calculate
activation = slipnet[result]   # Check

# Do this:
active_facts = slipnet.get_active_links()  # Query
# Returns: [Link("15 is-sum-of (4,11)", activation=0.8), ...]
chosen_fact = weighted_choice(active_facts)
build_operation_from(chosen_fact)  # No calculation!
```

**Benefits:**
- No simulation/calculation
- Construction follows perception
- Truly emergent

**Challenges:**
- ~15,000 arithmetic facts to encode
- Slipnet links need activation
- Larger architectural change

---

## Conclusion

✓ **Implemented Level 2:** Slipnet-driven evaluation
✓ **Tested and verified:** 7x boost for promising operations
✓ **Committed and pushed:** Ready for review

**This is a pragmatic middle ground:**
- More emergent than hard-coded thresholds
- Less complex than full factual slipnet
- Good foundation for future FARG work

**The system now perceives (via slipnet activation) which results are interesting,**
**rather than hard-coding which results to pursue.**
