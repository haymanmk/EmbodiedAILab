---
type: concept
domain: research
created: 2026-05-13
updated: 2026-05-13
aliases: ["robotics stack", "robot development stack", "robotics tooling"]
tags: [robotics, tools, ros2, simulation, controls]
---

# Robotics Development Stack

## Definition

The robotics development stack is the layered set of theory, hardware, middleware, simulation, data tooling, model training, deployment, and safety practices needed to build robots that work outside toy demos.

## Layers

| Layer | What it answers | Typical tools / knowledge |
|---|---|---|
| Mechanics and electronics | What physical machine is being controlled? | CAD, motors, encoders, cameras, grippers, embedded boards |
| Kinematics and dynamics | How does the robot move in space? | Modern Robotics, rigid-body transforms, Jacobians, inverse kinematics, dynamics |
| Control | How are actions stabilized and executed? | PID, impedance control, trajectory tracking, motor drivers |
| Middleware | How do processes communicate? | ROS 2, DDS, topics, services, actions, launch, parameters |
| Planning and manipulation | How are collision-free motions generated? | MoveIt 2, OMPL, planning scenes, grasping pipelines |
| Simulation | How do we test before real hardware? | Gazebo, Isaac Sim, MuJoCo, Isaac Lab, Libero, Meta-World |
| Data | How are robot episodes recorded and loaded? | LeRobotDataset, Open X-Embodiment, DROID-style datasets, Hugging Face Hub |
| Learning | How are policies trained? | PyTorch, LeRobot, ACT, diffusion policy, RL, VLA models |
| Deployment | How does inference run at control rate? | LeRobot rollout, async inference, real-time chunking, edge GPU or remote inference |
| Safety and evaluation | How do we avoid damage and measure progress? | workspace limits, emergency stop, staged evaluation, benchmark tasks, logs |

## Variations / debates

- Classical robotics gives reliability and interpretability; learning-based robotics gives adaptability and easier scaling from demonstrations.
- A useful modern robotics project usually combines both: classical software handles timing, interfaces, safety limits, calibration, and monitoring; learned policies handle perception-to-action behavior.
- LeRobot is strongest in the data, learning, and deployment layers. ROS 2 and MoveIt remain stronger in middleware, robot application structure, and classical manipulation workflows.

## Related concepts

- [[Robot Learning]]
- [[Imitation Learning]]
- [[Vision-Language-Action Models]]

## Mentions

- [[LeRobot]]
- [[Modern Robotics Development - synthesis]]
- [[LeRobot Documentation Index]]

## External sources

- ROS overview: https://www.ros.org/blog/why-ros/
- ROS 2 docs: https://docs.ros.org/
- MoveIt 2 docs: https://moveit.picknik.ai/main/index.html
- Gazebo docs: https://gazebosim.org/docs/latest/getstarted/
- Isaac Sim docs: https://docs.isaacsim.omniverse.nvidia.com/latest/index.html
- Modern Robotics: https://modernrobotics.northwestern.edu/
