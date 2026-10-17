# Flappy Bird AI with NEAT

An AI agent trained to play Flappy Bird using NeuroEvolution of Augmenting Topologies (NEAT) and Pygame.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![NEAT](https://img.shields.io/badge/NEAT--Python-0.92-orange)

## 📌 Project Overview

This project implements an AI player for the classic Flappy Bird game using the **NEAT** (NeuroEvolution of Augmenting Topologies) genetic algorithm. Instead of using traditional reinforcement learning, NEAT evolves both the weights and the topology (structure) of neural networks over successive generations to learn the optimal jumping strategy.

Each bird in the population operates its own feedforward neural network. Inputs fed to the neural network include:
1. Bird's current `y`-position
2. Distance from the bird to the top pipe gap
3. Distance from the bird to the bottom pipe gap

Based on these inputs, the neural network outputs a single value determining whether the bird should jump (`output > 0.5`).

---

## 🛠️ Requirements & Installation

### Prerequisites
Make sure you have Python installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/AIEngineer992007/Flappy_Bird_AI.git
cd Flappy_Bird_AI
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

To start the training process, execute:

```bash
python main.py
```

Watch as the population evolves! In early generations, most birds will fail quickly. Within a few generations, the AI will learn to navigate the pipes indefinitely.

---

## 📁 Project Structure

```text
├── imgs/                    # Game assets (sprites for bird, pipe, base, bg)
│   ├── base.png
│   ├── bg.png
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   └── pipe.png
├── config-feedforward.txt   # Configuration parameters for NEAT
├── main.py                  # Primary entry point & game logic loop
├── README.md                # Project documentation
└── requirements.txt         # Required Python packages
```

---

## ⚙️ How NEAT Works in This Project

- **Fitness Function:** 
  - Birds receive a small reward (`+0.1`) for every frame they stay alive.
  - Successfully passing through a pipe yields a significant fitness bonus (`+5`).
  - Colliding with a pipe deducts fitness (`-1`) to discourage reckless maneuvers.
- **Population:** Managed via settings in `config-feedforward.txt`.
- **Termination:** The evaluation runs across generations until the score threshold is reached or manually stopped.

---

## 📜 Acknowledgments

- Inspired by the *Tech With Tim* Flappy Bird AI tutorial series.
- Asset artwork belongs to their respective original creators.