import numpy as np
from typing import List, Optional, Union, Callable, Tuple
from linprog_lib.method.config.configuration import LinearProgrammingConfig

class SimplexProblemConfig(LinearProgrammingConfig):
    """
    Configuration class for Simplex method in Linear Programming.
    This class extends the LinearProgrammingConfig to include specific options for the Simplex method.
    """
    def __init__(self,
                 method: str,
                 objective_type: str,
                 c: List[float],
                 A: List[List[float]],
                 b: List[float],
                 constraint_signs: List[str],
                 var_bounds: Optional[List[Union[str, None]]] = None,
                 problem_form: str = "general",
                 print_solution: bool = True,
                 print_plot: bool = False,
                 print_tables: bool = False,
                 print_path: bool = False,
                 print_plot_path: bool = False,
                 verbose: bool = False,
                 option: str = "coordinates"):
        """
        Initialize the SimplexProblemConfig with the given options.
        Args:
            method (str): The method to be used for solving the problem.
            objective_type (str): The type of objective ('min' or 'max').
            c (List[float]): Coefficients of the objective function.
            A (List[List[float]]): Coefficients of the constraints.
            b (List[float]): Right-hand side values of the constraints.
            constraint_signs (List[str]): Signs of the constraints ('<=', '>=', '=').
            var_bounds (Optional[List[Union[str, None]]]): Variable bounds (default is None).
            problem_form (str): The form of the problem ('general', 'standard', 'canonical').
            print_solution (bool): Whether to print the solution.
            print_plot (bool): Whether to print plots.
            print_tables (bool): Whether to print tables.
            print_path (bool): Whether to print the path taken by the algorithm.
            print_plot_path (bool): Whether to print the plot path.
            verbose (bool): Verbosity level for debugging.
            option (str): Options for the Simplex method, default is "coordinates".
        """
        super(SimplexProblemConfig, self).__init__(
            method=method,
            objective_type=objective_type,
            c=c,
            A=A,
            b=b,
            constraint_signs=constraint_signs,
            var_bounds=var_bounds,
            problem_form=problem_form,
            print_solution=print_solution,
            print_plot=print_plot,
            print_tables=print_tables,
            print_path=print_path,
            print_plot_path=print_plot_path,
            verbose=verbose
        )
        self.option = option



class SimplexProblemRepresentation:
    """
    Class for representing the Simplex problem in a human-readable format.
    This class provides methods to display the problem in LaTeX format.
    """
    def __init__(self,
                 option: str,
                 coordinates_names: List[str],
                 coordinates_values: List[List[float]],
                 objective_function: Union[List[float], Callable[[List[float]], float]],
                 objective_type: str = "max"
                 ):
        """
        Initialize the SimplexProblemRepresentation with the given options.
        Args:
            option (str): The option for the representation ('coordinates' or 'objective').
            coordinates_names (List[str]): Names of the coordinates.
            coordinates_values (List[List[float]]): Values of the coordinates.
            objective_function (Union[List[float], Callable[[List[float]], float]]): Objective function coefficients or callable.
            objective_type (str): The type of objective ('min' or 'max').
        """
        self.option = option
        self.coordinates_names = coordinates_names
        self.coordinates_values = coordinates_values
        self.objective_function = objective_function
        self.objective_type = objective_type.lower()

    def coordinate_method(self):
        """
        Generate a LaTeX representation of the Simplex problem using coordinates.
        Returns:
            str: LaTeX representation of the Simplex problem.
        """
        if self.option != "coordinates":
            raise ValueError("Option must be 'coordinates' for this method.")

        n_vars = len(self.coordinates_values[0])
        n_pts  = len(self.coordinates_names)

        # ===== 1) Calculate z values at each point =====
        if callable(self.objective_function):
            z_vals = [self.objective_function(x) for x in self.coordinates_values]
        else:
            c = np.asarray(self.objective_function, dtype=float)
            z_vals = [float(np.dot(c, x)) for x in self.coordinates_values]

        # ===== 2) Find optimal point =====
        if self.objective_type == "max":
            best_idx = int(np.argmax(z_vals))
        else:
            best_idx = int(np.argmin(z_vals))

        best_name = self.coordinates_names[best_idx]
        best_coords = self.coordinates_values[best_idx]
        best_z = z_vals[best_idx]

        # ===== 3) Create LaTeX table =====
        # 3‑a) Header row
        header_row = " & " + " & ".join(self.coordinates_names) + r" \\ \hline"

        # 3‑b) Coordinate row (x1, x2, ..., xn)
        var_label = "(" + ",".join([f"x_{i+1}" for i in range(n_vars)]) + ")"
        coord_cells = [
            "(" + ", ".join(f"{v:g}" for v in pt) + ")" for pt in self.coordinates_values
        ]
        coord_row = f"{var_label} & " + " & ".join(coord_cells) + r" \\ \hline"

        # 3‑c) z row
        z_row = "z & " + " & ".join(f"{z:g}" for z in z_vals) + r" \\ \hline"

        # 3‑d) Combine table
        n_cols = n_pts + 1
        table = (
            r"\[" "\n"
            r"\begin{array}{|" + "c|" * n_cols + r"}" "\n"
            r"\hline" "\n"
            + header_row + "\n"
            + coord_row  + "\n"
            + z_row      + "\n"
            r"\end{array}"
            r"\]" "\n\n"
        )

        # ===== 4) Conclusion =====
        conclusion = (
            f"\\textbf{{Optimal Point}}: {best_name} = {tuple(best_coords)} "
            f"with \\(z^* = {best_z:g}\\)."
        )

        # ===== 5) Print result =====
        full_output = table + conclusion
        print(full_output)
    
    def objective_method(self, step: float = 2.0, print_result: bool = False) -> Union[None, Tuple[float, float, float]]:
        """
        Generate a LaTeX representation of the Simplex problem using the objective function.
        Args:
            step (float): Step size for the objective function.
        Returns:
            Tuple[float, float, float]: Tuple containing the values of z_a, z_b, and z_c.
        """
        if self.option != "objective":
            raise ValueError("Option must be 'objective' for this method.")

        if callable(self.objective_function):
            z_vals = [self.objective_function(x) for x in self.coordinates_values]
        else:
            c = np.asarray(self.objective_function, dtype=float)
            z_vals = [float(np.dot(c, x)) for x in self.coordinates_values]

        if self.objective_type == "max":
            best_idx = int(np.argmax(z_vals))
            best_z = max(z_vals)
        else:
            best_idx = int(np.argmin(z_vals))
            best_z = min(z_vals)

        best_name = self.coordinates_names[best_idx]
        best_coords = self.coordinates_values[best_idx]

        z_a = best_z - step
        z_b = best_z
        z_c = best_z + step

        if print_result:
            if callable(self.objective_function):
                z_func = "z = f(x_1, x_2)"
            else:
                terms = [f"{coef}x_{i+1}" if coef != 1 else f"x_{i+1}" 
                        for i, coef in enumerate(self.objective_function) if coef != 0]
                z_func = "z = " + " + ".join(terms)

            z_latex = (
                r"\[" "\n"
                + z_func.replace("+ -", "- ") + r" = " + f"{z_b:g}" + r"\\ \text{(optimal, at " + best_name + ")}" "\n"
                r"\]" "\n"
                f"\\textbf{{Optimal Solution}}: \\({best_name} {tuple(best_coords)}\\) with \\(z^* = {best_z:g}\\)."
            )

            print("\nObjective Function Slippage Method:")
            print(z_latex)

        if not print_result:
            return z_a, z_b, z_c

