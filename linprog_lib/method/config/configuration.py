"""
This module defines the LinearProgrammingConfig class, which encapsulates the configuration
for a linear programming problem. It includes methods for initializing the configuration,
validating inputs, and generating a summary of the problem in a LaTeX-like format.
"""

from typing import List, Union, Optional
from linprog_lib.utils.logger import logger

class LinearProgrammingConfig:
    """
    Configuration class for Linear Programming problems.
    This class encapsulates the parameters required to define a linear programming problem,
    including the method to be used, the objective function, constraints, and user preferences.
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
                 verbose: bool = False):
        """
        Initialize the LinearProgrammingConfig with the given parameters.
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
        """
        
        # Validate inputs
        valid_methods = ["geometric", "simplex", "bland", "two_phase"]
        if method not in valid_methods:
            logger.warning(f"Invalid method '{method}'. Must be one of {valid_methods}.")
        self.method = method

        if objective_type not in ["min", "max"]:
            logger.warning(f"Invalid objective type '{objective_type}'. Must be 'min' or 'max'.")
        self.objective_type = objective_type

        valid_forms = ["general", "standard", "canonical"]
        if problem_form not in valid_forms:
            logger.warning(f"Invalid problem form '{problem_form}'. Must be one of {valid_forms}.")
        self.problem_form = problem_form
        
        # Objective function coefficients
        self.c = c
        self.A = A
        self.b = b
        self.constraint_signs = constraint_signs
        self.var_bounds = var_bounds if var_bounds else [None] * len(c)

        # User preferences
        if print_plot and len(self.c) > 2:
            print_plot = False
            logger.warning("Plotting is only supported for 2D problems.")
        if print_plot_path and len(self.c) > 2:
            print_plot_path = False
            logger.warning("Plotting path is only supported for 2D problems.")
        self.print_solution = print_solution
        self.print_plot = print_plot
        self.print_tables = print_tables
        self.print_path = print_path
        self.print_plot_path = print_plot_path
        self.verbose = verbose

    def _format_term_for_expression(self, coef: float, var_name: str, is_first_term: bool) -> str:
        """
        Helper to format a single term in an expression for LaTeX-like output.
        e.g., coef=2, var_name="x_{1}", is_first_term=True  => "2x_{1}"
              coef=0, var_name="x_{2}", is_first_term=False => " + 0x_{2}"
              coef=-1, var_name="x_{3}", is_first_term=False => " - x_{3}"
              coef=1.0, var_name="x_{1}", is_first_term=True => "x_{1}"
              coef=2.0, var_name="x_{1}", is_first_term=True => "2x_{1}"
        Args:
            coef (float): Coefficient of the term.
            var_name (str): Variable name (e.g., "x_{1}").
            is_first_term (bool): Whether this is the first term in the expression.
        Returns:
            str: Formatted term string.
        """
        abs_coef = abs(coef)

        # Format coefficient part (e.g., "2", "", "2.5")
        if abs_coef == 1:
            coef_str_part = ""
        else:
            # If it's a whole number like 2.0, display as "2"
            if abs_coef == int(abs_coef):
                coef_str_part = str(int(abs_coef))
            # If it's a float like 2.5, display as "2.5"
            else:
                coef_str_part = str(abs_coef)
        
        term_core = f"{coef_str_part}{var_name}"

        # Determine sign prefix
        sign_str = ""
        if is_first_term:
            if coef < 0:
                sign_str = "-" 
            # No sign for positive or zero first term (e.g. "2x_1" or "0x_1")
         # Not the first term
        else:
            if coef < 0:
                sign_str = " - " # e.g., "... - 2x_1"
            else:
                sign_str = " + " # e.g., "... + 2x_1" or "... + 0x_1"
        
        return f"{sign_str}{term_core}"

    def summary(self) -> str:
        """
        Generate a summary of the linear programming problem in LaTeX-like format.
        Returns:
            str: A formatted string summarizing the problem.
        """
        summary_lines = []

        # 1. Objective Function
        obj_expr_parts = []
        first_written_obj_term = True
        all_obj_coeffs_zero = all(val == 0 for val in self.c)
        
        if not self.c or all_obj_coeffs_zero: 
            objective_str = "0"
        else:
            for j, coef_val in enumerate(self.c):
                if coef_val == 0:
                    continue 

                var_name = f"x_{{{j+1}}}"
                term_str = self._format_term_for_expression(coef_val, var_name, first_written_obj_term)
                obj_expr_parts.append(term_str)
                first_written_obj_term = False 
            
            if not obj_expr_parts:
                objective_str = "0" 
            else:
                objective_str = "".join(obj_expr_parts)
        
        obj_keyword = "\\text{min}" if self.objective_type == "min" else "\\text{max}"
        summary_lines.append(f"\\[ \n\\begin{{align*}}\n{obj_keyword} \\quad & {objective_str} \\\\")

        # 2. Constraints
        if self.A: 
            constraints_tex_parts = []
            for i, (a_row, b_val, sign_char) in enumerate(zip(self.A, self.b, self.constraint_signs)):
                lhs_parts = []
                first_written_constraint_term = True
                all_coeffs_zero_in_row = all(c_val == 0 for c_val in a_row)

                if (all_coeffs_zero_in_row and a_row) or (not a_row):
                    lhs_str = "0"
                else:
                    for j, val_a in enumerate(a_row):
                        if val_a == 0:
                            continue
                        var_name = f"x_{{{j+1}}}"
                        term_str = self._format_term_for_expression(val_a, var_name, first_written_constraint_term)
                        lhs_parts.append(term_str)
                        first_written_constraint_term = False
                    lhs_str = "".join(lhs_parts)
                
                tex_sign = ""
                if sign_char == '<=': tex_sign = "\\leq"
                elif sign_char == '>=': tex_sign = "\\geq"
                elif sign_char == '=': tex_sign = "="
                else: tex_sign = sign_char

                prefix = "\\text{subject to} \\quad & " if i == 0 else "& "
                constraints_tex_parts.append(f"{prefix}{lhs_str} {tex_sign} {b_val}")
            
            if constraints_tex_parts:
                summary_lines.extend([s + " \\\\" for s in constraints_tex_parts])

        # 3. Variable Bounds/ Domain
        if self.c:
            all_vars_real_unbounded = True
            if self.var_bounds:
                for bound_spec in self.var_bounds:
                    if bound_spec is not None: # A specific bound like '>=' exists
                        all_vars_real_unbounded = False
                        break
            
            if all_vars_real_unbounded:
                var_list_str = ", ".join([f"x_{{{j+1}}}" for j in range(len(self.c))])
                summary_lines.append(f"\\text{{for }} {var_list_str} \\in \\mathbb{{R}}\n \\]")
            else:
                bound_strs_list = []
                for i, bound_sign_char in enumerate(self.var_bounds):
                    var_name = f"x_{{{i+1}}}"
                    if bound_sign_char == '>=':
                        bound_strs_list.append(f"{var_name} \\geq 0")
                    elif bound_sign_char == '<=':
                        bound_strs_list.append(f"{var_name} \\leq 0")
                    elif bound_sign_char == '=': 
                        bound_strs_list.append(f"{var_name} = 0")
                    elif bound_sign_char is None: 
                        bound_strs_list.append(f"{var_name} \\in \\mathbb{{R}}")
                
                if bound_strs_list: 
                     summary_lines.append(f"\\text{{for }} \\quad & {', '.join(bound_strs_list)}\n\\end{{align*}}\n\\]")
        
        return '\n'.join(summary_lines)

    def __repr__(self) -> str:
        return self.summary()
