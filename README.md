# `linprog` - Linear Programming Problems Solver

---

# Project Pipeline

```
linprog/
├── README.md                   # Overview of the project and usage guide
├── LICENSE                    # License information
├── requirements.txt            # List of dependencies to install
├── app.py                      # Main file to run the application
├── data/                       # Directory containing input data
├── research/                   # Research documents
│   ├── *.ipynb            # Experiment notebook
├── logs/                       # Directory to store log files
│   └── linprog.log             # Main log file for the pipeline
├── method/                     # Directory containing solution methods
│   ├── config/                
│   │   ├── configuration.py    # Configuration for the methods
│   ├── geometric/              # Geometric method
│   │   ├── components.py       # Components of the geometric method
│   │   ├── solver.py           # Logic for solving using the geometric method
│   │   ├── explain.py          # Explanation of variables and steps
│   │   └── main.py             # Run the geometric method
│   ├── simplex/                # Simplex method
│   │   ├── components.py       # Components of the simplex method
│   │   ├── solver.py           # Logic for solving using the Simplex algorithm
│   │   ├── explain.py          # Explanation and illustration
│   │   └── main.py             # Run the simplex method
│   ├── bland/                  # Bland's method
│   │   ├── components.py       # Components of Bland's method
│   │   ├── solver.py           # Logic for solving using Bland's rule
│   │   ├── explain.py          # Explanation of Bland's operation
│   │   └── main.py             # Run Bland's method
│   └── two_phase/              # Two-phase method
│       ├── components.py       # Components of the two-phase method
│       ├── solver.py           # Solve using the two-phase method
│       ├── explain.py          # Explanation and illustration of this method
│       └── main.py             # Run the two-phase method
├── llms_feat/                  # Features integrated with LLMs (left open)
│   └── ...                     # Placeholder for LLMs features
├── utils/                      # General utility functions
│   ├── logger.py               # Setup and manage logging
│   ├── common.py               # General utility functions
├── reference/                  # Reference documents
├── setup.py                    # Package setup for the project
└── template.py                 # Project template
```