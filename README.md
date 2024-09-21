# Markov Process Simulation

## Description
This project simulates discrete homogeneous Markov processes with the ability to manually input or randomly generate data. The program calculates the fundamental matrix and models system behavior over a specified number of steps (tacts). It also visualizes transition graphs and the probabilities over time using Kolmogorov equations.

## Features
- **Random Data Generation**: Automatically generates initial probability vectors, transition matrices, and cost vectors for the Markov process simulation.
- **Manual Input Mode**: Allows users to manually input the initial probability vector, transition matrix, and cost vector.
- **Kolmogorov Equations**: Solves the Kolmogorov system of equations to estimate probabilities over time.
- **Transition Graph Visualization**: Displays a visual representation of the transition graph between states.
- **Probability Plotting**: Shows the state probabilities over time through a graphical plot.

## Requirements
- Python 3.12.6
- Required libraries: `tkinter`, `matplotlib`, `numpy`, `scipy`, `networkx`

Install the required libraries by running:

```bash
pip install -r requirements.txt
```

### Run the Application:
```bash
python main.py
```

## Input Data
You can either manually input the matrix size and the number of tacts, or generate random data using the provided buttons in the graphical interface. Toggle between random data generation and manual data input.

## Calculate Probabilities
Press the "Calculate Probabilities" button to simulate the Markov process over the selected number of steps. View the calculated transition probabilities and costs in the "Data" tab.

## Visualization
The program generates plots of state probabilities over time. The transition graph between states can be visualized by pressing the "Show Transition Graph" button.

## Example

For a matrix size of 5 and 10 tacts:

- The application generates a random transition matrix, initial probabilities, and a cost vector.
- The simulation runs and displays the state probabilities over the defined number of tacts.
- The transition graph visualizes the relations between states, with edge weights representing transition probabilities.

## Instructor
**Instructor:** Tatiana Borisovna Efimova — PhD in Economics, Associate Professor, and Head of the "Digital Technologies" Department at Samara State University of Transport (SamGUPS). She specializes in the integration of digital technologies and innovations in economic processes.

## Specialization
**Information Systems and Technologies (IST)** — my specialization, which focuses on studying and applying modern digital technologies to optimize and automate various processes.