from typing import List
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from string import ascii_uppercase
from linprog_lib.utils.logger import logger
from linprog_lib.method.simplex.components import SimplexProblemConfig
from linprog_lib.method.simplex.components import SimplexProblemRepresentation

class SimplexSolver:
    """
    SimplexSolver class for solving linear programming problems using the Simplex method.
    This class is responsible for implementing the Simplex algorithm and providing methods to solve
    linear programming problems.
    """

    def __init__(self, config: SimplexProblemConfig, step: float = None):
        """
        Initialize the SimplexSolver with the given configuration.
        Args:
            config (SimplexProblemConfig): Configuration object for the Simplex method.
            step (float): Step size for the objective function line (default is 10.0).
        """
        self.config = config
        self.problem_representation = None
        if self.config.option not in ["objective"] and step is not None:
            step = None
            logger.warning(f"Invalid option '{self.config.option}'. Must be 'objective'.")
        self.step = step

    def _calculate_intersection(self):
        """
        Calculate all valid intersection points (vertices) of the constraint lines.
        Returns:
            coordinates_names (List[str]): Names of the vertices (O, A, B, C, ...).
            coordinates_values (List[List[float]]): Coordinates of the vertices.
        """
        A = np.array(self.config.A)
        b = np.array(self.config.b)
        num_vars = A.shape[1]

        # Add bounds x_i >= 0 (if specified in config)
        var_bounds = self.config.var_bounds or [">="] * num_vars
        for i, bound in enumerate(var_bounds):
            if bound == ">=":
                row = np.zeros(num_vars)
                row[i] = 1.0
                A = np.vstack([A, row])
                b = np.append(b, 0.0)

        # Generate all possible combinations of n constraints
        all_indices = range(len(A))
        vertices = {}
        for combo in combinations(all_indices, num_vars):
            try:
                A_eq = A[list(combo)]
                b_eq = b[list(combo)]
                if np.linalg.matrix_rank(A_eq) < num_vars:
                    continue
                point = np.linalg.solve(A_eq, b_eq)

                # Feasibility check
                feasible = True
                for a_row, b_val, sign in zip(A, b, self.config.constraint_signs + [">="]*num_vars):
                    if sign == "<=" and np.dot(a_row, point) > b_val + 1e-8:
                        feasible = False
                        break
                    if sign == ">=" and np.dot(a_row, point) < b_val - 1e-8:
                        feasible = False
                        break
                    if sign == "=" and abs(np.dot(a_row, point) - b_val) > 1e-8:
                        feasible = False
                        break

                if feasible:
                    vertices[tuple(np.round(point, 8))] = None

            except np.linalg.LinAlgError:
                continue
        
        # Generate point names (O, A, B, C, ...)
        coordinates_names = []
        coordinates_values = []
        for idx, pt in enumerate(vertices.keys()):
            name = ascii_uppercase[idx] if any(pt) else "O"
            coordinates_names.append(name)
            coordinates_values.append(list(pt))
        
        return coordinates_names, coordinates_values

    def _plot_domain(self, coordinates_names: List[str], coordinates_values: List[List[float]]):
        """
        Plot the feasible domain defined by the constraints in the Simplex problem configuration.
        Args:
            coordinates_names (List[str]): Names of the coordinates (variables).
            coordinates_values (List[List[float]]): Values of the coordinates.
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

            # Plot vertices with names
            for name, coords in zip(coordinates_names, coordinates_values):
                x, y = coords
                plt.scatter(x, y, color='black', zorder=5)
                plt.text(x + 0.2, y + 0.2, name, fontsize=12, fontweight='bold')

            # Check if option is objective slippage
            if self.config.option == "objective":
                z_a, z_b, z_c = self.problem_representation.objective_method(step=self.step, print_result=False)
                for i, z_val in enumerate([z_a, z_b, z_c]):
                    y_vals = (z_val - self.config.c[0] * x_vals) / self.config.c[1]
                    if i == 1:
                        plt.plot(x_vals, y_vals, label=f"Objective Line: z = {z_val}", linestyle='--', linewidth=2)
                    else:
                        plt.plot(x_vals, y_vals, linestyle=':', linewidth=2)

            plt.fill_between(x_vals, y_min, y_max, where=(y_min <= y_max), color='green', alpha=0.3)
            plt.xlabel("x1")
            plt.ylabel("x2")
            plt.title("Feasible Region (2D)")
            plt.legend(loc='upper right')
            plt.show()
    
    def solve(self):
        """
        Solve the linear programming problem using the Simplex method.
        Returns:
            None
        """
        coordinates_names, coordinates_values = self._calculate_intersection()
        self.problem_representation = SimplexProblemRepresentation(
            option=self.config.option,
            coordinates_names=coordinates_names,
            coordinates_values=coordinates_values,
            objective_function=self.config.c,
            objective_type=self.config.objective_type
        ) if self.problem_representation is None else self.problem_representation
        self._plot_domain(coordinates_names, coordinates_values)

        if self.config.option == "objective":
            self.problem_representation.objective_method(step=self.step, print_result=True)
        elif self.config.option == "coordinates":
            self.problem_representation.coordinate_method()
