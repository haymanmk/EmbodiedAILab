---
type: concept
domain: research
created: 2026-05-19
updated: 2026-05-19
aliases: ["IsaacLab", "Isaac Sim", "Omniverse Isaac Lab"]
tags: [isaaclab, isaac-sim, simulation, robotics, framework]
---

# Isaac Lab

> NVIDIA's Python framework for robot simulation, training, and teleoperation, built on top of Isaac Sim. The scripting layer you write your robot code against. Where the [[Robotics Development Stack]] "Simulation" layer becomes programmable.

## Everyday analogy: movie set + script + blueprint

Imagine you're directing a movie. Three separate things sit in front of you:

1. **A physical movie set** with real props, real cameras, real lighting. Drop a coin and it falls. Light hits a surface and reflects. — That's **Isaac Sim**: a 3D world with photoreal rendering and physics-accurate everything (PhysX for contact, gravity, joints).

2. **A script** that says "Camera 1, pan left. Actor enters. Picks up coin. Pause two seconds. Exit." — That's **Isaac Lab**: Python code that drives the set frame-by-frame. Your script controls what happens.

3. **A blueprint of the set** — the floor plan plus a labeled list of every prop ("wooden chair, 50cm tall, 5kg, oak texture, sits at coordinates (x, y, z)"). — That's **USD** (Universal Scene Description): the structured file format that describes a scene's prims, transforms, materials, and physics properties.

You (the director) write the Python script (Isaac Lab) that tells the set (Isaac Sim) what to do with the props (USD scene).

**Where the analogy breaks down**: a real movie set runs one take at a time, slowly, with human actors. Isaac Sim runs **thousands of parallel takes simultaneously on a GPU**, because the whole point of training a policy is generating massive amounts of trajectory data. The movie framing helps for understanding *one episode*; for understanding *training*, picture thousands of identical sets, identical scripts, slightly different starting conditions, all rolling in parallel.

## The four layers, in a table

| Layer | What it is | Who built it | Your handle |
|---|---|---|---|
| **USD** (Universal Scene Description) | Open file format for describing 3D scenes (Pixar's, used industry-wide) | Pixar | `.usd` / `.usda` files |
| **Isaac Sim** | The simulator that runs USD scenes with photoreal rendering + GPU PhysX | NVIDIA | `SimulationApp` (booted via `AppLauncher`) |
| **Isaac Lab** | Python framework on top of Isaac Sim with robot-shaped APIs (scenes, articulations, sensors, controllers, environments) | NVIDIA | `isaaclab.*` Python packages |
| **LeIsaac** | Project on top of Isaac Lab adding LeRobot-shaped teleop + dataset recording for the SO101Leader and friends | Lightwheel AI | `leisaac.*` Python packages |

Reading bottom-up: when your LeIsaac code does `device.get_pose()`, that call passes through LeIsaac → Isaac Lab → Isaac Sim → USD scene state. Each layer adds vocabulary; none replaces the layer below.

## Application lifecycle: why imports come AFTER the app launch

Every Isaac Lab standalone script has the same skeleton:

```python
"""Step 1: parse CLI args and launch the Isaac Sim app."""
import argparse
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="My first Isaac Lab script")
AppLauncher.add_app_launcher_args(parser)   # registers --headless, --device, --enable_cameras, etc.
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# === Everything below this line happens INSIDE the running Isaac Sim app ===

"""Step 2: only NOW import the rest of Isaac Lab."""
import isaaclab.sim as sim_utils

"""Step 3: build the scene and run the simulation."""
def main():
    sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)

    # Spawn a ground plane so the camera has something to look at.
    ground_cfg = sim_utils.GroundPlaneCfg()
    ground_cfg.func("/World/Ground", ground_cfg)

    sim.reset()
    while simulation_app.is_running():
        sim.step()


if __name__ == "__main__":
    main()
    simulation_app.close()
```

**Why this order?** Isaac Sim is not a plain Python library. It's a C++ application (NVIDIA Omniverse Kit) with its own embedded Python interpreter. The line

```python
app_launcher = AppLauncher(args_cli)
```

does not merely *construct a Python object* — it **boots the entire Omniverse runtime**: loads native shared libraries, initializes the renderer, starts PhysX, and registers a tree of Python extensions. Many `isaaclab.*` modules are only available *after* the app is running, because they're registered as Kit extensions at boot. Importing them earlier raises `ModuleNotFoundError` or a more cryptic "extension not enabled" error.

**The right mental model**: think of `AppLauncher(args_cli)` as roughly

```python
# pseudocode
boot_isaac_sim_process()
attach_my_python_interpreter_to_it()
```

Everything you import afterwards is reaching into that *running* Isaac Sim process. Your Python is no longer a standalone script; it's a controller sitting inside a 3D application.

**Practical rule**: in any standalone script, all `isaaclab.*`, `isaacsim.*`, `omni.*`, and `pxr.*` (USD) imports must live below the `simulation_app = app_launcher.app` line. Standard library + third-party imports (`argparse`, `math`, `numpy`, `torch`) can sit above.

## The simulation loop

After the scene is built, the actual physics ticking is just:

```python
while simulation_app.is_running():
    sim.step()
```

Each `sim.step()` advances PhysX by `dt` seconds (default 1/60 s ≈ 16 ms), renders if cameras are enabled, and re-syncs the USD scene state. `simulation_app.is_running()` returns `False` when the user closes the GUI window or your script calls `simulation_app.close()`. Every Isaac Lab tutorial and every LeIsaac task ends up looking like this loop — only the body changes.

## How to actually run a script

Isaac Lab ships with a wrapper that knows where its bundled Python interpreter lives:

```bash
./isaaclab.sh -p path/to/my_script.py --headless
```

- `-p path/to/script.py` — run a Python script with Isaac Lab's bundled Python
- `--headless` — don't open the GUI window (faster; required for training and data collection on a remote host)
- `--device cuda:0` — pick the GPU
- `--enable_cameras` — turn on rendering of camera sensors (needed for vision policies)

You can also call the bundled Python directly (`./_isaac_sim/python.sh` on Linux), but `isaaclab.sh -p` is the idiomatic entry point.

## Where this lands in the LeIsaac stack

LeIsaac is "just" an Isaac Lab project that follows the same skeleton. When you eventually run a LeIsaac teleop session, the entry script:

1. Calls `AppLauncher` exactly as above.
2. Imports `isaaclab.devices.OpenXRDevice` (the VR-headset reader) and `isaaclab.controllers` (IK).
3. Imports `leisaac.envs.<TaskName>Env` (a LeIsaac task with a robot and a scene).
4. Spins the same `while simulation_app.is_running(): step` loop, where each step reads the VR pose, retargets, IKs to joint angles, sends them to the simulated robot, and writes the resulting (observation, action) frame to a LeRobot-format dataset.

The bones are identical; the body is LeIsaac-specific.

## What's next in this curriculum

This page covers the mental model + the bootstrap. The remaining Layer B lessons in rough order:

1. **USD basics** — what's inside a `.usd` file; the prim/path tree; the `/World/...` namespace; how to convert a URDF to USD with Isaac Lab's converter.
2. **Scene abstractions** — `InteractiveScene`, `Articulation`, sensors, controllers. The "named handles to objects in your blueprint" layer.
3. **Environment workflows** — `ManagerBasedEnv` vs `DirectRLEnv`; when to reach for which; how a "task" is defined.
4. **Teleop primitives** — `OpenXRDevice`, `Retargeter`; the device-to-action pipeline LeIsaac wires together.

After Layer B is comfortable, Layer C (LeIsaac itself) is mostly reading other people's code with framework knowledge in hand.

## Things to try (optional)

If you have a working install, these ground the abstractions:

1. Run the empty-scene tutorial: `./isaaclab.sh -p source/standalone/tutorials/00_sim/create_empty.py`. Verify a window opens with a ground plane.
2. Modify it to spawn a cube above the ground; watch it fall.
3. Add `--headless` to step 2 and notice the script still runs (no window, but the loop ticks). This is the mode you'll use for data collection.

You don't need to do these before the next lesson — they're for grounding the abstractions if you have a working Isaac Lab install.

## Related concepts

- [[VR Teleoperation in Simulation]] — where Isaac Lab sits in the teleop stack
- [[Robotics Development Stack]] — the bigger picture
- [[LeRobot]] — the dataset/policy framework on the other end of LeIsaac

## Mentions

- [Isaac Lab official docs](https://isaac-sim.github.io/IsaacLab/) — authoritative reference, pulled live via context7 from `/isaac-sim/isaaclab`
- [LeIsaac repo](https://github.com/lightwheelai/leisaac) — the framework on top
