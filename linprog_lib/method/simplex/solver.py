import numpy as np
import matplotlib.pyplot as plt
from linprog_lib.utils.logger import logger
from linprog_lib.method.simplex.components import SimplexProblemConfig

class SimplexSolver:
    """
    SimplexSolver class for solving linear programming problems using the Simplex method.
    This class is responsible for implementing the Simplex algorithm and providing methods to solve
    linear programming problems.
    """

    def __init__(self, config: SimplexProblemConfig):
        """
        Initialize the SimplexSolver with the given configuration.
        Args:
            config (SimplexProblemConfig): Configuration object for the Simplex method.
        """
        self.config = config

    def _plot_domain(self):
        """
        Plot the feasible domain defined by the constraints in the Simplex problem configuration.
        """
        if not self.config.print_plot:
            logger.warning("Plotting is disabled in the configuration.")
            return
        
        A = np.array(self.config.A)
        b = np.array(self.config.b)
        num_vars = len(self.config.c)
        
        if num_vars == 2:
            x_vals = np.linspace(0, 20, 1000)
            y_min = np.zeros_like(x_vals)
            y_max = np.full_like(x_vals, 20)
            plt.figure(figsize=(8, 6))
            cnt_constraints = 0
            for i in range(len(A)):
                a1, a2 = A[i]
                b_val = b[i]
                constraint_sign = self.config.constraint_signs[i]
                cnt_constraints += 1
                if a2 != 0:
                    y_vals = (b_val - a1 * x_vals) / a2
                    plt.plot(x_vals, y_vals, label=f"Constraint ({i+1}): {a1}x1 + {a2}x2 {constraint_sign} {b_val}", linestyle='-', alpha=0.8)

                    # Draw arrow to show direction of feasible region
                    test_val = 0
                    satisfies = ((constraint_sign == "<=" and test_val <= b_val) or
                                 (constraint_sign == ">=" and test_val >= b_val) or
                                 (constraint_sign == "=" and test_val == b_val))
                    arrow_direction = -1 if satisfies else 1

                    mid_x = 10
                    mid_y = (b_val - a1 * mid_x) / a2
                    norm = np.sqrt(a1**2 + a2**2)
                    dx = (a1 / norm) * arrow_direction
                    dy = (a2 / norm) * arrow_direction
                    plt.arrow(mid_x, mid_y, dx, dy, color='black', head_width=0.5, head_length=0.8)

                    if constraint_sign == "<=" or constraint_sign == "=":
                        y_max = np.minimum(y_max, y_vals)
                    elif constraint_sign == ">=":
                        y_min = np.maximum(y_min, y_vals)
                else:
                    plt.axvline(b_val / a1, color='red', linestyle='--', label=f"Constraint ({i+1}): x1 {constraint_sign} {b_val / a1}")

            # Add bounds for variables x1, x2 >= 0 (if specified in config)
            for i, bound in enumerate(self.config.var_bounds):
                cnt_constraints += 1
                if bound == ">=" and i == 0:
                    plt.axvline(0, color='black', linestyle=':', label=f"Constraint ({cnt_constraints}): x1 >= 0")
                    plt.arrow(15, 0, 0, 1, color='black', head_width=0.5, head_length=0.8)
                elif bound == ">=" and i == 1:
                    plt.axhline(0, color='gray', linestyle=':', label=f"Constraint ({cnt_constraints}): x2 >= 0")
                    plt.arrow(0, 15, 1, 0, color='black', head_width=0.5, head_length=0.8)

            plt.fill_between(x_vals, y_min, y_max, where=(y_min <= y_max), color='green', alpha=0.3)
            plt.xlabel("x1")
            plt.ylabel("x2")
            plt.title("Feasible Region (2D)")
            plt.legend(loc='upper right')
            plt.show()
    
