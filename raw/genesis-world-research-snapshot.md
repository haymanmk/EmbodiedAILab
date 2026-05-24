---
title: Genesis physics simulator — research snapshot
source_url: https://github.com/Genesis-Embodied-AI/Genesis
docs_url: https://genesis-world.readthedocs.io
project_page: https://genesis-embodied-ai.github.io/
pypi: https://pypi.org/project/genesis-world/
authors: Zhou Xian (CMU/Genesis AI, lead), Yiling Qiao, Zhenjia Xu, Tsun-Hsuan Wang, Tairan He, Zilin Si, Yufei Wang, Pingchuan Ma, Yuanming Hu (Taichi), Guanya Shi, Lingjie Liu, Taku Komura, Zackory Erickson, David Held, Minchen Li, Linxi "Jim" Fan (NVIDIA), Yuke Zhu, Wojciech Matusik (MIT), Dan Gutfreund (IBM), Shuran Song, Daniela Rus (MIT CSAIL), Ming Lin, Bo Zhu, Katerina Fragkiadaki (CMU advisor), Chuang Gan (IBM/UMass), and ~30 others
saved: 2026-05-24
tags: [simulator, physics, embodied-ai, gpu-sim, generative, taichi, differentiable]
---

# Genesis physics simulator — research snapshot

> Raw-materials capture for the EmbodiedAILab vault. Critical, evidence-based read. Today: 2026-05-24, ~18 months after first release.

## TL;DR for the impatient

- **Genesis** is a unified Python-fronted, GPU-accelerated physics simulator (rigid + MPM + SPH + FEM + PBD + Stable Fluid) released 2024-12-19. Repo at `Genesis-Embodied-AI/Genesis`; PyPI as `genesis-world`. Current version: **v0.4.7** (2026-05-16).
- The headline "**43M FPS**, **10–80× faster than Isaac/MuJoCo MJX**" claim is partially supported but heavily caveated. Independent benchmarks (Stone Tao / StoneT2000) showed the original number collapsed ~150× under realistic settings; in some configs Genesis is **3–10× slower** than ManiSkill/SAPIEN on manipulation.
- The **generative framework is still not open-sourced** as of May 2026 — issue [#6](https://github.com/Genesis-Embodied-AI/Genesis/issues/6) still has users bumping it 17+ months later. It was effectively spun out into the for-profit **Genesis AI** ($105M seed, July 2025; first model GENE-26.5 in May 2026).
- **No first-party VR/XR/teleop.** Confirmed in issue [#1626](https://github.com/Genesis-Embodied-AI/Genesis/issues/1626): collaborator `YilingQiao` says "it's a bit out of scope for this repo." Keyboard teleop only. By contrast, **Isaac Lab 2.3.2 (2026-01-30) ships Meta Quest VR teleop**.
- The physics engine itself is real, technically interesting (Taichi-based, now using a Genesis-internal Quadrants compiler since v0.4.0), with strong multi-physics scope. Where it actually wins is **mixing rigid + soft + fluid in one engine**, not pure RL throughput.

## What Genesis actually is

A "universal" physics + simulation platform with four advertised pillars (per project page and README):

1. **Physics engine** — re-built from scratch around a unified material-point / particle / rigid solver pipeline; intended to handle rigid, soft, cloth, fluid, granular, and thin-shell materials in one engine with cross-solver coupling.
2. **Robotics simulation platform** — pythonic API, asset loaders (MJCF/.xml, URDF, .obj, .glb, .ply, .stl), batched/parallel envs for RL.
3. **Photo-realistic rendering** — native ray-tracing path + rasterizer fallback; batched camera support for RL.
4. **Generative data engine** — promised text → 4D scene generation pipeline (**unreleased as of 2026-05**).

Solvers integrated (per `why_a_new_simulator` doc and README):

| Solver | Purpose | Differentiable? |
|---|---|---|
| Rigid body | articulated robots, contact | planned (next) |
| MPM | soft, granular, deformable | **yes** (only one currently stable) |
| SPH | smoothed-particle fluids | no |
| FEM | finite-element solids | no |
| PBD | position-based dynamics (cloth, hair) | no |
| Stable Fluid | gas/smoke (Eulerian) | no |
| Tool Solver | task-specific manipulators | **yes** |

Backends and OS:
- Compute: NVIDIA GPU, AMD GPU, Apple Metal, CPU (Linux/macOS/Windows).
- Build: Originally a Taichi fork (`GsTaichi`); migrated to in-house **Quadrants compiler** in v0.4.0 (2026-02-18) with ~30% additional perf on collision-heavy scenes.
- Python: requires `>=3.10,<3.14` (per docs); PyTorch is a hard dependency.

Robot platforms supported in examples / asset zoo: Franka, Anymal C, Unitree Go2, SO-101 (LeRobot arm), drones, humanoid (G1-class), soft robots.

## Speed and fidelity claims

### Headline numbers (with sources)

| Claim | Source | Conditions |
|---|---|---|
| 43,000,000 FPS | [Project page](https://genesis-embodied-ai.github.io/) + README | Single plane + Franka arm, no self-collision, idle pose, hibernation=True, 30,000 parallel envs, RTX 4090 |
| 430,000× real time | Project page | Same as above |
| 10–80× faster than Isaac Gym / Sim / Lab / MuJoCo MJX | [why_a_new_simulator doc](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/why_a_new_simulator.html) + Zhou Xian's X thread | No detailed conditions in the original claim |
| Train real-world transferable locomotion policy in **26 seconds** | Project page | Quadruped, unspecified hardware, demo-cherry-picked |
| 27M FPS with random actions, 43M FPS with self-collisions enabled | [Official benchmark report Jan 8 2025](https://github.com/zhouxian/genesis-speed-benchmark) | Franka, idle-ish pose, RTX 4090 |

### Independent verification / pushback

#### Stone Tao (StoneT2000), maintainer of ManiSkill/SAPIEN — primary critic

Blog: `stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is` (Dec 20 2024). Headline finding: "**up to 10× slower, not 10–80× faster**."

Four methodological issues identified:
1. **Minimum-fidelity solver config** — benchmark uses fastest physics with **only 1 substep**; Genesis's own training code uses 2–4.
2. **Idle simulation** — robot takes 1 action then sits still for 999 steps. Rigid-body solver early-exits ("auto-pause" / "hibernation"), making per-step time near-zero.
3. **Self-collisions disabled by default** — the Franka in the headline run can pass through itself.
4. **Object hibernation = True** — non-moving objects skipped entirely.

Corrected results (RTX 4090, Stone Tao's `genesis_corrected_franka_benchmark.py`):
- "43M FPS drops ~150× to ~0.29M FPS (290k FPS) when proper settings are applied."
- **FrankaPickCubeBenchmark**: Genesis ~10k–100k FPS depending on env count; ManiSkill/SAPIEN runs **3–10× faster**.
- Genesis showed contact-accuracy issues (cube falls out of gripper) at default solver settings — Genesis authors later acknowledged this came from poorly-tuned constraint solver config.
- **With camera rendering enabled, Genesis drops to ~10× realtime**; Isaac Lab and ManiSkill stay at ~1000× realtime.
- **Locomotion training speed in Genesis equals Isaac Lab** (admitted by a Genesis author per the blog).

Stone Tao also flagged that the 43M FPS / 30k envs figure is really **~1,400 FPS per env**, which is more reasonable but very differently framed than headline marketing.

Follow-up: After the team published the comprehensive Jan 8 2025 [benchmark report on Notion](https://placid-walkover-0cc.notion.site/genesis-performance-benchmarking) and corrected scripts, Stone Tao [posted in issue #181](https://github.com/Genesis-Embodied-AI/Genesis/issues/181) (2025-01-08): *"Thanks to the authors for the comprehensive report. Don't have time to verify things but the numbers in the report look more accurate when given the right context."* — a partial mea culpa from the Genesis side, not a vindication of the original 10–80× claim.

#### MuJoCo team response (google-deepmind/mujoco discussion [#2303](https://github.com/google-deepmind/mujoco/discussions/2303))

- `yuvaltassa` (MuJoCo lead): *"As far as we can tell there is no reason for it to be that much faster. It appears they are comparing to single threaded MuJoCo rather than multithreaded or MJX, so the comparison seems disingenuous."*
- `zhouxian` (Genesis) clarified: the 10–80× number is against **Isaac** specifically, not MJX. He gave two reasons for not benchmarking MJX directly:
  1. MJX lacks robust mesh-collision support without hand-tuned MJCF.
  2. When restricted to primitive collisions, MJX performance ≈ Isaac.

#### Hacker News critical comments (item [42457213](https://news.ycombinator.com/item?id=42457213))

- `forrestthewoods`: "23.26 nanoseconds per frame — twice as fast as a single cache miss?" — points out the headline is incoherent at single-robot level.
- `GrantMoyer`: noted the "`hibernation = True`" fine-print on benchmark videos was omitted from marketing.
- `bengarney`: *"The performance numbers are so far beyond real world numbers as to be incoherent. If you redefine what all the words mean, then the claims are not comparable."* Also called the code, minus Taichi, *"adequate implementations of well-known techniques… something a really good developer could bang out in a couple of months."*
- `erwincoumans` (creator of Bullet Physics): confirmed Genesis uses Taichi for CUDA compilation similar to NVIDIA Warp — gives the engine technical legitimacy despite marketing.
- `dr_kretyn`, `dragonwriter`: "100% Python" is misleading — code calls into Taichi/Numba native-compiled kernels (which is fine, but not what users hear).
- `poslathian`: "Zero details amidst tons of documentation… how these two universes [physics + generative] are being unified."

#### What the official January 8, 2025 benchmark report actually shows

After Stone Tao's blog post, the Genesis team published a corrected benchmark suite at [zhouxian/genesis-speed-benchmark](https://github.com/zhouxian/genesis-speed-benchmark) with a detailed Notion writeup. Key methodology shifts in the response:
- Reported numbers now use `substeps=2` (matching training code), not 1.
- Self-collisions enabled in the headline number.
- A "random actions" variant (per-step joint perturbations) reported alongside the idle case.
- Multiple environments tested: `franka/`, `franka_dynamic/`, `anymal_c/`, `go2/`, `grasp/`, `multi_obj/`.

Reported corrected numbers (Genesis self-published):
- Franka, self-collisions on, idle pose: still ~43M FPS aggregate (RTX 4090, 30k envs ≈ 1,400 FPS/env).
- Franka, self-collisions on, **random actions**: ~27M FPS aggregate.
- Stone Tao's response (in [issue #181](https://github.com/Genesis-Embodied-AI/Genesis/issues/181), 2025-01-08): *"The numbers in the report look more accurate when given the right context"* — a measured acceptance, not a full vindication. He explicitly noted he didn't re-verify them.

The corrected `franka.py` benchmark in the official examples (still shipping as of 2026-05) uses: `B=30000`, `dt=0.01`, `performance_mode=True`, optional `-c` flag for self-collision (~5% perf hit), optional `-r` flag for random actions. Hibernation is no longer the default in the script, but `performance_mode=True` enables several of the auto-pause heuristics under the hood.

### Net verdict on the speed claims

- The **43M FPS / 430,000× headline is methodologically misleading** at the marketing level — it measures parallel batched throughput on a near-idle robot with the most permissive solver config. The per-robot effective throughput is on the order of **1,000–10,000 FPS**, which is competitive with but not categorically faster than modern GPU sims.
- The **10–80×** claim against Isaac/MJX **does not survive independent benchmarking** for typical RL workloads. Realistic numbers put Genesis **near parity with Isaac Lab on locomotion** (admitted by a Genesis author per Stone Tao's blog) and **3–10× slower than ManiSkill** on manipulation tasks where the solver actually has to work.
- The team did publish corrected benchmarks and walked back some claims by Jan 8 2025. Whether **current v0.4.x** with the new Quadrants compiler has materially closed the gap is **not independently verified** as of 2026-05 — Stone Tao has not re-benchmarked.
- Genesis's actual technical advantage is **not raw throughput** but **multi-physics breadth** (rigid + MPM + SPH + FEM + PBD + Stable Fluid in one engine). The marketing emphasized the weakest claim.

## Architecture

- **Frontend**: Pure-Python user API (`import genesis as gs`). The marketing line "100% Python" is technically true for user-facing code, but the hot path is native via Taichi-emitted CUDA/Metal/LLVM kernels — same trick as NVIDIA Warp or JAX-via-XLA. (HN commenters `dr_kretyn` and `dragonwriter` called this language pedantic but acknowledged it's a reasonable abstraction.)
- **Compute backend evolution**:
  - **v0.1–v0.3 (Dec 2024 → late 2025)**: Genesis ran on a Genesis-Embodied-AI fork of Taichi called **GsTaichi**. Taichi creator Yuanming Hu is a Genesis co-author, so this was upstream-friendly.
  - **v0.4.0 (2026-02-18)**: Switched to an in-house compiler called **Quadrants** that replaces GsTaichi. The release notes credit Quadrants with "up to 30%" speedup on collision-heavy scenes and full feature parity across NVIDIA / AMD / Metal backends (where previously CUDA was first-class and others lagged).
  - **v0.4.6 (2026-04-11)**: Backported CUDA-only perf uplifts to all GPU backends, fixed several CUDA crashes.
  - **v0.4.7 (2026-05-16)**: New tactile sensor type; experimental ImGui interactive viewer plugin.
- **Differentiability**: Limited in the open-source release. Only **MPM solver** and **Tool Solver** expose gradients. Rigid-body differentiability is listed as "planned, starting with rigid & articulated body solver" since the original Dec 2024 announcement and is still "planned" in v0.4.7. This is a regression vs. the team's prior academic work (Qiao et al. on differentiable articulated bodies, FluidLab) where differentiable rigid + articulated bodies already existed in research code. Plausible reason: the company retains differentiable-rigid as a private gradient pipeline.
- **RL integration**: No first-party RL library. Examples in `examples/locomotion/` ship hand-rolled PPO loops (Go2, Anymal C). Users typically wire up `skrl`, `stable-baselines3`, or NVIDIA's `rl_games` themselves. Contrast with Isaac Lab, which ships `rl_games`, `skrl`, and `rsl_rl` integrations out of the box.
- **Asset I/O**: MJCF (`.xml`), URDF (incl. `xacro` since v0.3.x), `.obj`, `.glb`, `.ply`, `.stl`. USD support is partial — recent v0.4.x release notes mention USD texture rendering and batched USD cameras, but full USD scene graph editing is not the first-class workflow it is in Isaac Sim.
- **Rendering**: Two paths.
  - **Rasterizer**: fast, supports batched cameras (added in v0.4.x), used for RL pixel-observation training.
  - **BVH ray-tracer**: photo-real, used for hero demos and synthetic-data generation.
  - Camera rendering throughput is the weak spot — Stone Tao measured a drop to ~10× realtime with cameras enabled vs ~1000× for Isaac Lab. The rasterizer improvements in v0.4.x are explicitly aimed at this gap.
- **Parallelism model**: Genesis batches *envs* on the GPU like Isaac Gym did, not via separate processes. The `B` (batch) dimension is exposed in the API. Hibernation/sleeping is a per-object optimization on top.
- **Solver coupling**: The architectural claim that sets Genesis apart from Isaac/MJX/Brax is *unified* multi-solver coupling — e.g., a rigid Franka gripper interacting with an MPM dough or an SPH liquid in the same step. Independent verification of stability and accuracy of this coupling at scale is **still thin**; demos look good, papers are mostly the team's own.

## Generative framework status

- Promised in Dec 2024 announcement: text → 4D dynamic scene generation, articulated-object generation, character animation with emotion, drone swarms, etc. (All demos shown on project page.)
- **Issue #6 timeline (still open across 2025–2026)**:
  - 2024-12-19: First user asks for a release timeline.
  - 2024–2025: Collaborator `ziyanx02`: *"Providing a detailed timeline is challenging due to limited contributors, but stay tuned."*
  - Users repeatedly bumping; one comment notes *"6 months and no estimate for the release of one of the key advertised use cases."*
  - `rfan-debug` (May/June 2025): congratulates the team on their seed round — implicitly acknowledging the generative IP went to **Genesis AI** the company.
  - As of 2026-05, **no public release of the generative framework**. The HN community's accusation (`PyroFilmsFX`: *"this was quite the misrepresentation to not once mention that that portion is unreleased"*) has aged well.
- The generative pipeline now appears to live inside **Genesis AI** the startup, used internally as a synthetic-data engine for their **GENE-26.5** robotics foundation model (announced 2026-05-06 via TechCrunch). The open-source repo gets the physics engine; the company keeps the data engine and the model.

## VR / teleop status

- **Confirmed: no first-party VR/XR/OpenXR support** in Genesis as of 2026-05. Verified against the latest docs (v0.4.7), examples directory, release notes, and issue tracker.
- **Issue [#1626](https://github.com/Genesis-Embodied-AI/Genesis/issues/1626)** ("Does Genesis support VR device control of robotic arms, e.g. Meta Quest or Apple Vision Pro?"), opened 2025-08-25 (in Chinese), closed same day:
  - Community contributor `MRiabov` pointed the asker at `examples/keyboard_teleop.py` and asked them to upstream any VR work.
  - Genesis collaborator **`YilingQiao`** (Yiling Qiao — a core author of the Genesis paper) replied: *"Yes, we tried VR control ourselves. You can implement it based on the keyboard_teleop example and adapt it to your own codebase for VR. **However, it's a bit out of scope for this repo**, since it involves many other dependencies and would be hard to maintain. We're happy to help if you encounter any issues related to Genesis during your implementation."*
  - **Translation**: The team has internal VR code (probably inside Genesis AI the company) but it is not coming to the open-source repo.
- **Issue [#1529](https://github.com/Genesis-Embodied-AI/Genesis/issues/1529)** ("human teleoperation support", opened 2025-08-09, still open as of 2026-05): collaborator `Kashu7100` redirects users to `keyboard_teleop.py`. Other commenters note the keyboard action space is too small for VLA training and that roll/pitch can't be mapped onto a keyboard.
- The only first-party teleop is **keyboard**: `examples/keyboard_teleop.py`, added in PR [#1344](https://github.com/Genesis-Embodied-AI/Genesis/issues/1344) on 2025-07-02. Subsequent fixes: #1558 (gripper penetration), #2353 (keyboard focus / reserved keys).
- **Contrast with Isaac Lab (Jan 2026 baseline)**:
  - Isaac Lab **2.3.2** (2026-01-30) ships **Meta Quest VR teleop** as a documented feature, paired with the Mimic data pipeline for demonstration recording.
  - Isaac Lab also supports **Pico 4 Ultra** and **Apple Vision Pro** via **NVIDIA CloudXR** (Early Access).
  - Documentation: [Setting up CloudXR Teleoperation — Isaac Lab](https://isaac-sim.github.io/IsaacLab/main/source/how-to/cloudxr_teleoperation.html).
  - GR00T-WholeBodyControl (NVLabs) ships VR teleop integrations on top of Isaac Lab.
- **Implication for the user's active VR teleoperation in Isaac Lab project**:
  - If VR teleop in simulation is on the critical path, Genesis is a **DIY effort** — you would need to wrap your own OpenXR / Oculus SDK / Quest Link input on top of the `keyboard_teleop.py` pattern, expose IK targets in the API, and handle latency. Maintainer-confirmed out-of-scope, so no upstream help.
  - Isaac Lab is the path of less resistance for the user's current track. Genesis becomes interesting *later* if/when the work shifts into multi-material manipulation (cables, fabric, fluid in food handling) where Isaac Lab is weaker.

## Comparison: Genesis vs Isaac Lab vs MuJoCo MJX vs Brax vs SAPIEN

| Dimension | Genesis (v0.4.7, 2026-05) | Isaac Lab (2.3.2, 2026-01) | MuJoCo MJX (3.x) | Brax (JAX) | SAPIEN / ManiSkill |
|---|---|---|---|---|---|
| Rigid-body RL throughput | ~Isaac Lab parity on locomotion (per author admission); ~3–10× slower on manipulation (Stone Tao) | **150k+ FPS** for manipulation (NVIDIA blog, 2026); benchmark leader | Competitive on primitive collisions; mesh collision is weak | Hundreds of millions of physics steps/s, but only rigid + simple contact | Strong on manipulation; ManiSkill suite is the manipulation benchmark gold standard |
| Soft body / FEM / MPM | **Yes** (MPM, FEM, PBD) — main differentiator | Limited (PhysX soft body, recent) | Soft body via plugins, less mature | No | Limited (PhysX-based) |
| Fluid (SPH / Stable Fluid) | **Yes** | No | No | No | No |
| Multi-physics coupling | **Yes** (unified solver — main selling point) | No | No | No | No |
| Differentiable | Partial (MPM, Tool) | No | Yes (JAX-native) | **Yes** (JAX-native) | No |
| Photo-real rendering | Built-in ray-tracer | RTX path-tracing (via Omniverse) | None (separate viewer) | None | Built-in, fast |
| Sensors | Raycaster, DepthCamera, Lidar (Spherical pattern), Tactile (ElastomerDisplacement), Proximity, Temperature, ContactProbe — added v0.3.x | Full suite incl. visuo-tactile, RTX Lidar, IMU, force | Standard MuJoCo sensors | Minimal | Standard set |
| VR / Teleop | **Keyboard only** (no VR; out of scope per maintainer) | **Meta Quest + CloudXR** (built-in since 2.3.2) | None first-party | None | None first-party |
| Asset / scene format | MJCF, URDF, glTF, USD (partial) | USD-first (heavy) | MJCF | Custom + URDF | URDF |
| Windows support | Yes, but build-from-source still flaky (issue #1367, Jul 2025) | Limited (Linux strongly preferred) | Yes | Yes | Linux primary |
| Ecosystem & papers using it | Small but growing; many forks; mostly Genesis team's own | Huge (NVIDIA-backed, GR00T, etc.) | Huge (DeepMind backing) | Medium | Strong in manipulation research |
| Sim-to-real demos | Quadruped backflip demo (contested), early-stage | Mature (countless robots) | Mature | Limited (rigid only) | Strong manipulation sim-to-real |
| License | Apache-2.0 | BSD-3 (Isaac Lab); Omniverse EULA for Sim | Apache-2.0 | Apache-2.0 | MIT (SAPIEN) |

**Who should pick what (rough heuristic, May 2026):**
- **Need VR teleop in sim today** → Isaac Lab. Not negotiable.
- **Pure RL locomotion / humanoid throughput** → Isaac Lab or MJX. Genesis is competitive but not the leader.
- **Mixing rigid + soft + fluid in one env** (food handling, dough, water, cables) → **Genesis is genuinely the only practical option** in this list.
- **JAX-native differentiable rigid sim** → Brax / MJX.
- **Manipulation benchmarking with mature pipelines** → ManiSkill / SAPIEN.
- **Multi-physics + Apple Silicon dev box** → Genesis (Metal backend) is unusual here.

## Sensor inventory (as of v0.4.7)

Drawn from the [sensors docs](https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/sensors.html) and release notes:

| Sensor | Added | Status | Notes |
|---|---|---|---|
| Raycaster (generic) | v0.3.x (Sep 2025, PR #1742) | Stable | Configurable RaycastPattern; SphericalPattern → Lidar-like, GridPattern → planar |
| Lidar | v0.3.x via Raycaster + SphericalPattern | Stable | No RTX/PhysX Lidar parity with Isaac Sim |
| DepthCamera | v0.3.x (PR #1772) | Stable | `read_image()` formats raycasts as depth image |
| ElastomerDisplacement (tactile) | v0.3.x | Stable | Models tactile skin via probes reporting 3D displacement; cheaper than full FEM tactile |
| New tactile sensor type | v0.4.7 (May 2026) | New | Improves raycasting-based and previous tactile sensors; details thin in release notes |
| ProximitySensor | v0.3.x | Stable | Simple proximity probe |
| TemperatureGridSensor | v0.3.x | Stable | Spatial temperature field |
| KinematicContactProbe | v0.3.x | Stable | Contact event probe |
| IMU / RGB camera | Built-in | Stable | Standard |
| Force / torque | Limited | — | Less documented than Isaac Lab equivalent |
| Visuo-tactile (GelSight-like) | — | Missing | Isaac Lab 2.3 has this; Genesis only has ElastomerDisplacement approximation |
| Event camera | — | Missing | Both stacks lack this |

**Takeaway**: Genesis caught up on basic sensors between Sep–Dec 2025 (well after the Dec 2024 launch), but Isaac Lab still leads on visuo-tactile and RTX Lidar fidelity.

## Adoption signals

- **GitHub stars (Genesis-Embodied-AI/Genesis)**: ~28,800 stars, 2,714 forks, 120 open issues (as of 2026-05-23). Repo created 2023-10-31, public release Dec 2024.
- **PyPI**: `genesis-world` on PyPI, currently at v0.4.7.
- **Release cadence**: Steady — ~20 releases between v0.2.1 (2025-01-08) and v0.4.7 (2026-05-16). Roughly one release every 3–4 weeks. Indicates active maintenance.
- **Forks of note**: dozens of personal forks, none significant. The core Genesis-Embodied-AI org is the only meaningful maintainer.
- **Papers / projects using Genesis** (sample, not exhaustive):
  - **RoboGen** (Wang et al., ICML 2024, arXiv [2311.01455](https://arxiv.org/abs/2311.01455)) — explicitly says it's powered by Genesis. Same team.
  - **Virtual Community** (arXiv 2508.14893, 2025).
  - **Scan, Materialize, Simulate** (arXiv 2505.14938, 2025).
  - The genesis-world README's "Acknowledgements" cites prior work: FluidLab (arXiv 2303.02346), SoftZoo (2303.09555), RoboNinja (2302.11553), DiffuseBot, EMDM, Qiao et al. differentiable-physics papers (ICML 2020/2021, NeurIPS 2021). Most of these *precede* Genesis and are listed as inputs, not citations.
- **Independent academic adoption beyond the original team is still thin** as of mid-2026. The repo is widely starred / forked but the citation footprint outside the Genesis-Embodied-AI authors is small compared to Isaac Lab or MJX.

## Known limitations / open issues

- **Generative framework not released** — the headline use case is still proprietary inside Genesis AI the startup. (Issue #6, 17+ months open.)
- **No VR/XR/OpenXR** — maintainer-confirmed out of scope (issue #1626).
- **Contact-solver tuning is finicky** — multiple issues (#1557, #2041, #2158) on gripper penetration, "cube falls out of gripper," SO101 anomalies; constraint solver defaults required hand-tuning even for tutorial examples.
- **Windows build-from-source is fragile** (issue #1367, 2025-07). Pre-built wheels mostly work but native builds break.
- **Rendering throughput** — Stone Tao measured ~10× realtime with cameras enabled vs ~1000× for Isaac Lab. Improving in v0.4.x (Rasterizer batched cameras, USD textures) but not yet at Isaac Lab's level.
- **Differentiable rigid bodies still missing** in open source, even though the team had this in prior academic work. Likely a strategic withholding (the company keeps the data-generation gradients).
- **No first-party RL trainer** — users glue their own PPO/SAC. Compared to Isaac Lab's `rl_games` / `skrl` integration, this is friction.
- **Soft-body stability** — Stone Tao and HN commenters note: soft-body / fluid demos look impressive on video but stable real-time RL with MPM in the loop is still hard. Hibernation tricks don't apply to MPM.
- **Documentation**: Improved significantly over 2025 but still uneven; user guide present, API reference is mostly auto-generated.
- **Sensors added late**: Raycaster, DepthCamera, Lidar (SphericalPattern), tactile (ElastomerDisplacement), Proximity, Temperature, KinematicContactProbe — all landed in v0.3.x releases (Sep–Dec 2025). v0.4.7 (May 2026) adds an experimental ImGui interactive viewer and improved tactile sensors.

## Original team and incentives

- **Lead**: Zhou Xian — CMU Robotics Institute PhD (advisor: Katerina Fragkiadaki). Now CEO/founder of **Genesis AI** (the company).
- **Co-founder of the company**: Théophile Gervet (ex-Mistral research scientist).
- **Academic collaboration**: 24-month effort spanning ~20 labs:
  - CMU, MIT (CSAIL), Stanford, NVIDIA, Tsinghua, UMD, Columbia, Imperial College London, Georgia Tech, HKU, UPenn, Utah, UW, UMich, UT Austin, IBM Research, Taichi, plus more.
  - Notable senior names: Daniela Rus (MIT CSAIL), Wojciech Matusik (MIT), Yuanming Hu (Taichi creator), Linxi "Jim" Fan (NVIDIA), Yuke Zhu (UT Austin / NVIDIA), Shuran Song (Columbia / Stanford), Ming Lin (UMD), Bo Zhu (Dartmouth/Georgia Tech), Chuang Gan (UMass / IBM), Katerina Fragkiadaki (CMU), Taku Komura (HKU).
- **Funding (Genesis AI the company)**: $105M seed announced 2025-07-01. Lead: Eclipse, Khosla Ventures. Other investors: Bpifrance, HongShan (HSG), Eric Schmidt, Xavier Niel, Daniela Rus (also a co-author), Vladlen Koltun. Bloomberg confirms US + China VC mix.
- **Offices**: Silicon Valley, Paris, London. ~60 employees (per TechCrunch May 2026), ~40–45% Europe / 50–55% US.
- **First product**: **GENE-26.5** (May 2026) — robotics foundation model for dexterous hands (cooking, piano, Rubik's cube demos). Partner manufacturer: Wuji Tech (China). The Genesis simulator is positioned as the synthetic-data engine that bottlenecks model iteration speed.
- **Incentive read**: The open-source physics engine is a **distribution / recruiting / mindshare lever** for Genesis AI the company. The generative framework — the only piece that would meaningfully advantage a competitor's foundation-model effort — has been quietly retained as proprietary. Expect this split to persist.

## Papers

- **Project page paper / workshop ref**: "Genesis: A Generative and Universal Physics Engine for Robotics" — listed as ICRA 2025 publication (workshop track, 2025-05-18 publication date, IBM-tagged for Chuang Gan). **No arXiv ID located** as of 2026-05-24. The project does not currently have a peer-reviewed, citable full paper on arXiv that lays out the engine's design and benchmarks; the closest is the Notion benchmark report. This is a notable gap.
- **Underlying / cited work** (all pre-date Genesis itself):
  - **DiffTaichi** (Hu et al., ICLR 2020), arXiv [1910.00935](https://arxiv.org/abs/1910.00935)
  - **FluidLab** (Xian et al., ICLR 2023), arXiv 2303.02346
  - **RoboGen** (Wang et al., ICML 2024), arXiv [2311.01455](https://arxiv.org/abs/2311.01455)
  - **SoftZoo** (arXiv 2303.09555)
  - **RoboNinja** (arXiv 2302.11553)
  - **DiffuseBot** (NeurIPS 2023)
  - Scalable / efficient differentiable simulation series (Qiao et al., ICML 2020 / ICML 2021 / NeurIPS 2021).

## References

### Official (Genesis team)
1. [Genesis project landing page](https://genesis-embodied-ai.github.io/) — headline claims, lab/author list, demos.
2. [Genesis GitHub repo](https://github.com/Genesis-Embodied-AI/Genesis) — README, source, issues.
3. [Genesis docs (readthedocs)](https://genesis-world.readthedocs.io) — user guide, API, sensors.
4. [Why a new simulator](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/why_a_new_simulator.html) — official 10–80× framing.
5. [genesis-world on PyPI](https://pypi.org/project/genesis-world/) — release artifacts.
6. [Releases page](https://github.com/Genesis-Embodied-AI/Genesis/releases) — v0.2.1 → v0.4.7 changelog (2025-01-08 → 2026-05-16).
7. [zhouxian/genesis-speed-benchmark](https://github.com/zhouxian/genesis-speed-benchmark) — official benchmark scripts (Franka, AnymalC, Go2, grasp, multi_obj).
8. [Genesis benchmark Notion report (Jan 8 2025)](https://placid-walkover-0cc.notion.site/genesis-performance-benchmarking) — official response to Stone Tao.
9. [Zhou Xian's homepage](https://www.zhou-xian.com/) — founder background.

### Primary (Genesis AI company)
10. [TechCrunch — Genesis AI $105M seed, 2025-07-01](https://techcrunch.com/2025/07/01/genesis-ai-launches-with-105m-seed-funding-from-eclipse-khosla-to-build-ai-models-for-robots/)
11. [TechCrunch — Genesis AI full-stack demo, 2026-05-06](https://techcrunch.com/2026/05/06/khosla-backed-robotics-startup-genesis-ai-has-gone-full-stack-demo-shows/) — GENE-26.5 launch.
12. [PRNewswire — Genesis AI stealth emergence, 2025-07-01](https://www.prnewswire.com/news-releases/genesis-ai-emerges-from-stealth-with-105m-to-build-universal-robotics-foundation-model-and-horizontal-platform-for-general-purpose-physical-ai-302495016.html)

### Independent benchmarks / analyses
13. [Stone Tao — "How fast is the new hyped Genesis simulator?"](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is) — the primary critical analysis. Dec 20 2024.
14. [MuJoCo discussion #2303](https://github.com/google-deepmind/mujoco/discussions/2303) — MuJoCo team + Genesis author back-and-forth.
15. [Genesis issue #181](https://github.com/Genesis-Embodied-AI/Genesis/issues/181) — Stone Tao filed methodology concerns; Genesis team's report acknowledged.
16. [Silicon Valley Robotics Center — Best Robot Simulators for RL 2026](https://www.roboticscenter.ai/rl-environments/best-2026) — independent 2026 ranking; Genesis is #5.
17. [Simulately wiki — Overall Comparison](https://simulately.wiki/docs/comparison/) — multi-sim comparison table.

### Community discussion
18. [HN — Genesis generative physics engine, item 42457213](https://news.ycombinator.com/item?id=42457213) — substantive technical pushback.
19. [HN — Genesis 4D generative physics, item 42466792](https://news.ycombinator.com/item?id=42466792) (rate-limited, content overlaps).
20. [HN — Genesis universal physics, item 42456802](https://news.ycombinator.com/item?id=42456802).
21. [Genesis issue #6 — Generative framework timeline](https://github.com/Genesis-Embodied-AI/Genesis/issues/6) — 17+ month-old unresolved community ask.
22. [Genesis issue #1626 — VR control](https://github.com/Genesis-Embodied-AI/Genesis/issues/1626) — confirmed out-of-scope.
23. [Genesis issue #1529 — Human teleoperation support](https://github.com/Genesis-Embodied-AI/Genesis/issues/1529) — points users back to keyboard teleop.

### Promotional / overview (lower trust, use only for context)
24. [MarkTechPost — Meet Genesis](https://www.marktechpost.com/2024/12/19/meet-genesis-an-open-source-physics-ai-engine-redefining-robotics-with-ultra-fast-simulations-and-generative-4d-worlds/)
25. [DataCamp — Genesis Physics Engine](https://www.datacamp.com/blog/genesis-physics-engine)
26. [Marvik blog — Genesis: Redefining Robotics](https://www.marvik.ai/blog/genesis-redefining-robotics-and-physics-simulations)
27. [AI Business Weekly — 20 AI labs release Genesis](https://aibusinessweekly.net/p/genesis-open-source-physics-simulator-robotics-ai)
28. [Slashdot — 430,000× faster than reality](https://hardware.slashdot.org/story/24/12/24/022256/new-physics-sim-trains-robots-430000-times-faster-than-reality)

### Adjacent / comparison
29. [Isaac Lab releases](https://github.com/isaac-sim/IsaacLab/releases) — 2.3.2 ships Meta Quest VR teleop (Jan 30 2026).
30. [Isaac Lab CloudXR teleop doc](https://isaac-sim.github.io/IsaacLab/main/source/how-to/cloudxr_teleoperation.html) — Meta Quest 3 + Pico 4 Ultra.

## Open questions to follow up

- **Independent v0.4.x benchmark**: no third party seems to have re-run Stone Tao's corrected benchmarks against current Genesis (v0.4.7 + Quadrants compiler). Worth re-checking if the 3–10× manipulation gap vs ManiSkill has closed.
- **Will the generative framework ever be open-sourced?** As of 2026-05 the answer effectively reads "no" — it's the moat for Genesis AI the company. Should be flagged as proprietary when teaching this, not "near future."
- **Peer-reviewed Genesis paper**: only an ICRA 2025 workshop reference exists; no full arXiv preprint with full author list and benchmarks. Watch for a future archival paper.
- **Sim-to-real**: the 26-second locomotion-policy training claim has not been reproduced publicly to my knowledge. Look for academic papers with Genesis-trained policies deployed on real hardware (not just the team's own demos).
- **VR teleop status in Genesis**: monitor whether the community contributes an OpenXR / Quest 3 adapter on top of `keyboard_teleop.py`. Issue #1529 is the canonical place.
- **Genesis AI's GENE-26.5**: is it actually trained on Genesis-simulator data, or has Genesis AI built a separate internal sim? The public messaging conflates them; the engineering reality might not.
- **Differentiable rigid-body release timeline**: README says "planned" since Dec 2024; still planned in v0.4.7. Confirm whether this lands as open source or stays internal.
- **Apple Metal backend**: Genesis claims Metal support; no independent confirmation that meaningful RL workloads actually run usefully on M-series Macs.

## Practical guidance for an Isaac-Lab-first user evaluating Genesis

(Synthesizing the above from the perspective of the user's stated context: automation engineer, learning embodied AI, building VR teleop in Isaac Lab, evaluating Genesis vs Isaac Sim as a Quest 3 bridge.)

1. **Don't switch the VR teleop track to Genesis.** The maintainer has explicitly said VR is out of scope. The keyboard_teleop pattern would be the only starting point, and Genesis has no OpenXR / Quest hooks. Isaac Lab 2.3.2 already ships Meta Quest teleop — that's where the user already is, and the answer for VR is "stay there."
2. **Treat Genesis as a complementary tool, not a replacement.** It is genuinely the best practical option in this list for **multi-material manipulation** (rigid + soft + fluid in one env). If the project later expands into food handling, dough kneading, cable routing, fabric, or liquids, Genesis becomes interesting in a way Isaac Lab isn't.
3. **Don't trust the marketing numbers.** Use the official `examples/speed_benchmark/*.py` scripts on your own hardware before believing any speedup claim. Expect ~1,400 FPS per env at best with batched parallel envs, not the 43M FPS aggregate marketing.
4. **The generative framework should be treated as proprietary**, not "coming soon." 17 months of community asks have not produced a release plan. The data-generation IP has clearly moved to Genesis AI the company.
5. **Watch Quadrants and v0.5+.** The migration to the in-house compiler in v0.4.0 is a meaningful architectural inflection. Worth re-benchmarking against MJX and Isaac Lab once an independent party publishes numbers on current versions.
6. **Sim-to-real story is unproven beyond team demos.** The 26-second locomotion-policy training claim and double-backflip quadruped demo are the team's own work. Until external labs publish papers with Genesis-trained policies running on real hardware, treat sim-to-real as research-grade, not production-grade.
