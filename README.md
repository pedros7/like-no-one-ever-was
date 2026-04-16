# like-no-one-ever-was: Pokémon AI Battle Simulation & Elo Ranking System
A long-awaited passion project: a Pokémon battle simulator designed to determine the strongest NPC trainer in Pokémon Yellow by ranking them using an Elo-based system. Inspired by similar work from pimanrules, but built with my own approach and perspective.

This project is built around a **database-first architecture**, where all Pokémon, move, and type data is stored in a structured database and fetched dynamically at runtime before each battle.

---

## 🎯 Project Goals

- Simulate accurate Gen 1 Pokémon battles (1v1 initially)
- Store all game data in a relational database
- Fetch Pokémon stats dynamically before each battle
- Compute competitive rankings using Elo-based systems
- Run large-scale simulations for statistical analysis
- Build a scalable, distributed simulation engine
- Explore machine learning models for prediction and optimization

---

## ⚙️ Core Features (MVP)

- Deterministic 1v1 battle simulator
- Gen 1-inspired battle mechanics
- Type effectiveness system
- Move execution system (accuracy, critical hits, damage)
- Database-driven Pokémon, move, and type system
- Runtime data fetching before each battle

---

## 🧱 Architecture Overview

This project follows a phased evolution:

### Phase 1: Core Engine
- Battle system implementation
- Gen 1 mechanics
- Modular simulation design

### Phase 2: Database Layer (Key Design Choice)
- Pokémon, moves, and types stored in a database
- Data ingestion pipeline from external sources
- Runtime data fetching before battles

### Phase 3: Batch Simulation Engine
- Large-scale automated battle execution
- Statistical result collection

### Phase 4: Elo Ranking System
- Dynamic ranking system for Pokémon
- Persistent leaderboard storage

### Phase 5: API Layer
- REST API for simulations and queries
- Programmatic access to battle engine

### Phase 6: Distributed System
- Queue-based simulation workers
- Parallel execution of battle jobs

### Phase 7: Analytics Engine
- Win-rate analysis
- Matchup matrices
- Meta-game insights

### Phase 8: Machine Learning Layer
- Win prediction models
- Optimization of team compositions
- Advanced strategy learning

### Phase 9: Visualization (Optional)
- Battle replay system
- Interactive dashboards
- Leaderboard visualization

---

## 🗄️ Data Sources

All Pokémon data (stats, typing) is dynamically sourced and stored locally in a database.
All Pokémon will be standardized at level 50 with their corresponding stats. Move sets will be constructed by selecting optimal moves from both their in-battle moves and the full set of moves they can learn up to level 50, prioritizing the most effective options available.

---

## 🛠 Tech Stack (Planned)

- Python (core simulation engine)
- PostgreSQL (database layer)
- FastAPI (API layer)
- Redis / Celery (distributed processing)
- Scikit-learn / PyTorch (machine learning experiments)


---

## 📌 Project Status

Early development — core engine + database architecture design in progress.

---

## 📚 Inspiration

Inspired by competitive Pokémon simulation systems and prior community work exploring Gen 1 mechanics, ranking systems, and large-scale battle modeling.
