# Artificial Intelligence Lab 2 — Intelligent Agents & PEAS

**Student:** Ali Abbas
**Roll No.:** 030
**Course:** Artificial Intelligence
**Lab:** 2 — Intelligent Agents & PEAS

---

## 📌 Overview

This repository contains my work for **Artificial Intelligence Lab 2**, focusing on intelligent agents, PEAS specifications, environment classification, and a stateful classroom agent.

The purpose of this lab is to understand how intelligent agents perceive their environment, make decisions, select actions, and use previous information to avoid unnecessary repeated commands.

## 📂 Repository Contents

### Task 1: PEAS Specifications

This task describes the PEAS framework (Performance Measure, Environment, Actuators, and Sensors) for two intelligent agents.

* **Delivery Robot:** PEAS components, operating assumptions, tools, and design trade-offs.
* **LLM-Based Student-Support Agent:** PEAS components, tools, assumptions, and trade-offs.

### Task 2: Environment Classification

This task analyzes the environments in which the two agents operate.

* Classification of the delivery robot and student-support agent environments.
* Discussion of fully and partially observable environments.
* Explanation of deterministic and stochastic environments.
* Comparison between real-world environments and simulated environments.

### Task 3: Stateful Classroom Agent

This task implements a simple Python-based classroom agent that remembers its previous target mode and avoids sending duplicate commands.

The implementation includes:

* Temperature and room-occupancy percepts.
* Rules for selecting `COOL`, `WARM`, `IDLE`, and `ECO` modes.
* Previous-mode memory to prevent repeated commands.
* Tests for repeated percepts and temperature boundaries.
* An empty-room test case.
* Captured program output and a reflection on the implementation.

## ⚙️ How the Classroom Agent Works

The agent receives two input values, known as **percepts**:

* `temperature`: The room temperature in degrees Celsius.
* `occupied`: `True` if the room is occupied; otherwise, `False`.

### Decision Rules

| Condition                                                     | Target Mode |
| ------------------------------------------------------------- | ----------- |
| Room is empty                                                 | `ECO`       |
| Occupied room temperature is above 26°C                       | `COOL`      |
| Occupied room temperature is below 20°C                       | `WARM`      |
| Occupied room temperature is between 20°C and 26°C, inclusive | `IDLE`      |

The agent compares the selected target mode with its previous mode.

* If the target mode changes, the agent prints `COMMAND SENT`.
* If the target mode remains the same, the agent prints `NO COMMAND`.

The percepts used in this lab are predefined sample inputs, not readings from real sensors.

## 💻 Requirements

* Python 3
* No third-party Python packages are required for the simple Task 3 script.

## ▶️ How to Run

Open a terminal in the repository directory and execute:

```bash
python lab2_task3_simple.py
```

If your system uses `python3`, run:

```bash
python3 lab2_task3_simple.py
```

If the script is stored inside a task folder, update the command to match its actual location.

The program displays a step-by-step trace containing the previous mode, current percept, target mode, and command status.

## 🧪 Test Cases

The sample inputs are designed to check the following behavior:

1. A high temperature in an occupied room selects `COOL`.
2. Repeated percepts with the same target mode do not send duplicate commands.
3. At exactly 20°C, the occupied room selects `IDLE`.
4. At exactly 26°C, the occupied room selects `IDLE`.
5. A temperature below 20°C in an occupied room selects `WARM`.
6. An empty room selects `ECO`, regardless of the temperature in the sample input.

## ⚠️ Limitations

* The program uses predefined percepts rather than live sensor data.
* The modes are simulated labels; the script does not control actual heating or cooling equipment.
* Previous-mode memory lasts only while the program is running.
* The implementation demonstrates basic rule-based decision-making and is not a complete building-management system.
* A real implementation would require sensor validation, safety checks, hardware integration, and robust error handling.

## 🔐 Responsible Practice

Intelligent agents should be tested carefully before real-world deployment. They should handle uncertainty appropriately, protect user data, and avoid consequential actions without suitable safety checks or human oversight.

The PEAS specifications and environment classifications in this repository are based on the assumptions discussed in the lab work.

## 👨‍💻 Author

**Ali Abbas**
**Roll No.:** 030

---

*Artificial Intelligence Lab 2 — Intelligent Agents & PEAS*
