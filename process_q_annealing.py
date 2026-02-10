""" prepare inputs and analyze outputs from quantum annelaing """

import argparse



from QTrains import solve_on_LP, prepare_qubo, analyze_qubo_Dwave1
from QTrains import passing_time_histigrams1, objective_histograms1, plot_hist_pass_obj1, display_prec_feasibility1
from QTrains import Analyze_qubo
from QTrains import solve_qubo1, plot_train_diagrams
from QTrains import train_path_data, best_feasible_state, high_excited_state, get_solutions_from_dmode

from trains_timetable import Input_timetable, Comp_parameters





def process1(trains_input, q_pars):
    """ the sequence of calculation  makes computation if results has not been saved already"""

    dict_qubo = prepare_qubo(trains_input, q_pars, "")


    lp_sol = solve_on_LP(trains_input, q_pars, "")

    samplesets = solve_qubo1(q_pars, dict_qubo, "")

    results = analyze_qubo_Dwave1(trains_input, q_pars, dict_qubo, lp_sol, samplesets)


    file_pass = f"{trains_input.objective_stations[0]}_{trains_input.objective_stations[1]}.pdf"
    file_obj = "obj.pdf"

    hist_pass = passing_time_histigrams1(trains_input, q_pars, results)
    hist_obj = objective_histograms1(results)

    plot_hist_pass_obj1(trains_input, q_pars, hist_pass, hist_obj, file_pass, file_obj)

    display_prec_feasibility1(trains_input, q_pars, results)

    v = lp_sol["variables"]
    exclude_st = ""

    qubo_to_analyze = Analyze_qubo(dict_qubo)

    file =  "Conflicted_train_diagram.pdf"
    input_dict = train_path_data(v, qubo_to_analyze, exclude_st = exclude_st, initial_tt=True)
    plot_train_diagrams(input_dict, file)

    file =  "ILP_train_diagram.pdf"
    input_dict = train_path_data(v, qubo_to_analyze, exclude_st = exclude_st)
    plot_train_diagrams(input_dict, file)

    solutions = get_solutions_from_dmode(samplesets, q_par)
    solution, _ = best_feasible_state(solutions, qubo_to_analyze)
    v = qubo_to_analyze.qubo2int_vars(solution)

    file =  "best_solution_train_diagram.pdf"
        
    input_dict = train_path_data(v, qubo_to_analyze, exclude_st = exclude_st)
    plot_train_diagrams(input_dict, file)

    solution, _ = high_excited_state(solutions, qubo_to_analyze, trains_input.objective_stations, increased_pt=16)
    v = qubo_to_analyze.qubo2int_vars(solution)

    file =  "excited_solution_train_diagram.pdf"
        
    input_dict = train_path_data(v, qubo_to_analyze, exclude_st = exclude_st)
    plot_train_diagrams(input_dict, file)




if __name__ == "__main__":


    parser = argparse.ArgumentParser("mode of problem solving: computation /  output analysis")

    parser.add_argument(
        "--mode",
        type=int,
        help="process 1: make computation (ILP and simulated annealing)",
        default=1,
    )

    parser.add_argument(
        "--softern_pass",
        type=bool,
        help="if true analyze output without feasibility check on minimal passing time constrain",
        default=False,
    )


    args = parser.parse_args()


    q_par = Comp_parameters()
    q_par.softern_pass = args.softern_pass

    q_par.compute = False  # make computations / optimisation
    q_par.analyze = False  # Analyze results

    assert args.mode in [0,1,2,3,4,5,6]
    if args.mode == 1:

        our_qubo = Input_timetable()

        delays = {1:5, 2:2, 4:5}


        our_qubo.qubo_real_4t(delays)
        q_par.dmax = 6
        q_par.ppair = 2.0
        q_par.psum = 4.0
        process1(our_qubo, q_par)

        our_qubo = Input_timetable()



    