# FARGish Visualization Guide

This guide explains how to visualize Numbo execution to better understand FARG architecture.

## Quick Start

### 1. Simple Trace (Recommended for beginners)

Shows only key events - operations performed and their results:

```bash
python3 trace_viewer.py
```

**Output Example:**
```
============================================================
  NUMBO SIMPLE TRACE
============================================================

Problem: Use (4, 5, 6) with +, -, × to make 15
------------------------------------------------------------

⚡ t= 2: ImCell(5 x 4 = 20 (6 20))
   Activation: 0.160
   Distance from goal: 5

⚡ t= 6: ImCell(6 + 5 = 11 (4 11))
   Activation: 0.124
   Distance from goal: 4
```

This is much easier to read than the full trace!

### 2. Graph Visualization

Creates a visual network diagram showing support propagation:

```bash
python3 graph_visualizer.py 10
```

This runs for 10 timesteps and saves a PNG image showing:
- **Red nodes**: Goals (Want)
- **Green nodes**: Completed operations (ImCell)
- **Blue nodes**: Proposed operations (Consume)
- **Yellow nodes**: Workspace states (Canvas)
- **Edge thickness**: Support strength

The image is saved as `numbo_graph_t10.png`.

### 3. Interactive Visualizer

Step through execution manually:

```bash
python3 numbo_visualizer.py -i
```

Press Enter to advance one timestep at a time and see:
- Current workspace state
- Top active agents
- Operations completed
- Summary statistics

### 4. Simplified Run

Auto-run with cleaner output:

```bash
python3 numbo_visualizer.py
```

## Understanding the Output

### Key Concepts

**Agent (Codelet)**: A proposed action, like `Consume(+ 6 5, ...)`
- These are competing ideas about what to do next
- Created probabilistically based on support

**Activation**: A number showing how much support an agent has
- Higher activation = more likely to be selected
- Flows between connected nodes

**ImCell**: A completed operation
- `ImCell(6 + 5 = 11 (4 11))` means "6+5 was performed, result is 11, workspace now has (4, 11)"

**Canvas**: The workspace state
- `canvas[0]`: Initial state (4, 5, 6)
- `canvas[1]`: State after first operation
- etc.

### FARG Principles Visible

1. **Parallel Exploration**: Multiple `Consume` agents exist simultaneously
2. **Support Propagation**: `Want(15)` gives support to promising operations
3. **Competition**: Negative weights suppress competing alternatives
4. **Probabilistic Selection**: High-activation agents more likely to run

## For Phase 1 Study

### Week 1 Goals

**Understanding Support Propagation:**
1. Run `python3 trace_viewer.py` to see what operations happen
2. Run `python3 graph_visualizer.py 5` to see the support network
3. Read `FARGish2.py` lines 300-400 (activation graph)
4. Read `Numbo1.py` lines 200-350 (Consume agent implementation)

**Key Questions to Answer:**
- How does `Want(15)` decide which operations to support?
- Why do some operations get higher activation than others?
- How do competing operations suppress each other?
- What makes an operation "promising"?

### Tracing Through Code

Start with these files in this order:

1. **FARGish2.py:547** - `build()` method (how agents are created)
2. **FARGish2.py:821** - `do_timestep()` (main loop)
3. **Numbo1.py:237** - `Consume.go()` (what happens when agent runs)
4. **FARGish2.py:337** - `propagate()` (how support flows)

### Adding Your Own Diagnostics

You can modify the scripts to show more info:

```python
# In trace_viewer.py, add after line 95:
print(f"   Support from Want: {fm.activation_g.get_edge_data(wa, cell)}")
```

## Troubleshooting

**Graph doesn't display**: You're running in a headless environment. The graph is saved to a PNG file instead - check for `numbo_graph_*.png`.

**Want module errors**: Make sure you include `canvas=ca, addr=0` parameters when creating Want.

**Too verbose**: Use `trace_viewer.py` instead of running `Numbo1.py` directly.

## Next Steps

Once you understand the basic flow:
1. Modify the problem: Change `(4, 5, 6)` to other numbers
2. Modify the target: Change `15` to other values
3. Add print statements to see when specific agents are created
4. Run multiple times with different seeds to see different solution paths

Good luck with Phase 1!
