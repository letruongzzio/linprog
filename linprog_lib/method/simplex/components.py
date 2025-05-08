from typing import List, Optional, Union
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
                 options: str = "coordinates"):
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
            options (str): Options for the Simplex method, default is "coordinates".
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
        self.options = options
