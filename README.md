# Blackjack Simulation Project

This project provides:

- A Blackjack environment (`bj.py`) for simulation.
- Bots and strategies (`bj_bots.py`).
- Tools to visualies strategies (`strategy_tester.py`).
- Test specific strategiies and results (`examples/run_strategy_tester.py`)


## Installation

```bash
# Create conda environment
conda env create -f environment.yml
conda activate blackjack_project

# Or using pip
pip install -e .
pip install numpy matplotlib pytest argparse
```

## Usage

### Run examples
```bash
python examples/run_user_input.py
python examples/run_martingale.py
python examples/run_simulations.py
python examples/run_strategy_tester.py --list-strategies
```

### Run tests
```bash
pytest
```

## Project Structure

```
src/
  my_module.py
  bj.py
  bj_bots.py
  bj_cardcounting.py
  strategy_tester.py
tests/
examples/
setup.py
README.md
environment.yml
```
