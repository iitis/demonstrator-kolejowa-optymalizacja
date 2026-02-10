""" execution module for solving trains scheduling problem  """

from scipy.optimize import linprog
import neal
from dwave.system import (
    EmbeddingComposite,
    DWaveSampler
)
from dwave.system.composites import FixedEmbeddingComposite
from minorminer import find_embedding


from .parameters import (Parameters, Railway_input)
from .LP_problem import (Variables, LinearPrograming)
from .make_qubo import (QuboVars, Analyze_qubo, update_hist, is_feasible)



#### ILP solver
def solve_on_LP(trains_input, q_pars):
    """ solve the problem using LP, and save results """
    stay = trains_input.stay
    headways = trains_input.headways
    preparation_t = trains_input.preparation_t

    timetable = trains_input.timetable
    objective_stations = trains_input.objective_stations
    dmax = q_pars.dmax

    pars = Parameters(timetable, stay=stay, headways=headways,
                   preparation_t=preparation_t, dmax=dmax, circulation=trains_input.circ)
    rail_input = Railway_input(pars, objective_stations, delays = trains_input.delays)
    v = Variables(rail_input)
    bounds, integrality = v.bonds_and_integrality()
    problem = LinearPrograming(v, rail_input, M = q_pars.M)
    opt = linprog(c=problem.obj, A_ub=problem.lhs_ineq,
                  b_ub=problem.rhs_ineq, bounds=bounds, method='highs',
                  integrality = integrality)
    v.linprog2vars(opt)

    v.check_clusters()

    d = {}
    d["variables"] = v.variables
    d["objective"] = problem.compute_objective(v, rail_input)

    return d




#####  QUBO handling ######
def prepare_qubo(trains_input, q_pars):
    """ create and save QUBO given railway input and parameters 
    
    """
    stay = trains_input.stay
    headways = trains_input.headways
    preparation_t = trains_input.preparation_t

    timetable = trains_input.timetable
    objective_stations = trains_input.objective_stations

    ppair = q_pars.ppair
    psum = q_pars.psum
    dmax = q_pars.dmax

    par = Parameters(timetable, stay=stay, headways=headways,
                   preparation_t=preparation_t, dmax=dmax, circulation=trains_input.circ)

    rail_input = Railway_input(par, objective_stations, delays = trains_input.delays)
    q = QuboVars(rail_input, ppair=ppair, psum=psum)
    q.make_qubo(rail_input)
    qubo_dict = q.store_in_dict(rail_input)


    return qubo_dict



def solve_qubo1(q_pars, dict_read):
    """ solve the problem given by QUBO and store results """


    qubo_to_analyze = Analyze_qubo(dict_read)
    Q = qubo_to_analyze.qubo

    sampleset = {}
    loops = q_pars.num_all_runs // q_pars.num_reads
    if q_pars.method == "sim":
        for k in range(loops):
            s = neal.SimulatedAnnealingSampler()
            sampleset[k] = s.sample_qubo(
                Q, beta_range = q_pars.beta_range, num_sweeps = q_pars.num_sweeps,
                num_reads = q_pars.num_reads, beta_schedule_type="geometric"
            )

    elif q_pars.method == "real":
        sampler = EmbeddingComposite(DWaveSampler(solver=q_pars.solver, token=q_pars.token))

        for k in range(loops):

            sampleset[k] = sampler.sample_qubo(
                Q,
                num_reads=q_pars.num_reads,
                annealing_time=q_pars.annealing_time
        )
            
    print(f"solved qubo method {q_pars.method}")

    return sampleset
    


def get_solutions_from_dmode(samplesets, q_pars):
    """ from dmode imput return a series of QUBO solutions as [sol1, sol2, ...] """
    solutions = []
    broken_chains = []
    for sampleset in samplesets.values():
        if q_pars.method == "sim":
            for (sol, _, occ) in sampleset.record:  # not used energy in the middle
                for _ in range(occ):
                    solutions.append(sol)
        elif q_pars.method == "real":
            for (sol, _, occ, _) in sampleset.record:
                for _ in range(occ):
                    solutions.append(sol)
    assert len(solutions) == q_pars.num_all_runs

    return solutions


def analyze_qubo_Dwave1(trains_input, q_pars, dict_qubo, lp_sol, samplesets):
    """ analyze results of computation on QUBO and comparison with LP """


    qubo_to_analyze = Analyze_qubo(dict_qubo)

    stations = trains_input.objective_stations

    our_solutions = get_solutions_from_dmode(samplesets, q_pars)

    results = analyze_QUBO_outputs(qubo_to_analyze, stations, our_solutions, lp_sol, softernpass = q_pars.softern_pass)

    return results




def analyze_QUBO_outputs(qubo, stations, our_solutions, lp_solution, softernpass):
    """  returns histogram of passing times between selected stations and objective 
    """
    hist = list([])
    qubo_objectives = list([])

    energy_feasible = list([])
    energy_notfeasible = list([])

    count = 0
    no_feasible = 0

    display = len(our_solutions) < 100

    for solution in our_solutions:
        if display:
            dsiplay_solution_analysis(qubo, solution, lp_solution)

        count += 1

        if is_feasible(solution, qubo, softernpass):
            no_feasible += 1
            qubo_objectives.append(qubo.objective_val(solution))
            energy_feasible.append(qubo.energy(solution))

            update_hist(qubo, solution, stations, hist, softernpass)
        else:
            energy_notfeasible.append(qubo.energy(solution))

    perc_feasible = no_feasible/count

    results = {"perc feasible": perc_feasible, f"{stations[0]}_{stations[1]}": hist}
    results["no qubits"] = qubo.noqubits
    results["no qubo terms"] = len(qubo.qubo)
    results["lp objective"] = lp_solution["objective"]
    results["q ofset"] = qubo.sum_ofset
    results["qubo objectives"] = qubo_objectives
    results["energies feasible"] = energy_feasible
    results["energies notfeasible"] = energy_notfeasible
    return results



##### results presentation


def dsiplay_solution_analysis(trains_input, our_solution, lp_solution, timetable = False):
    "prints features of the solution "
    print( "..........  QUBO ........   " )
    print("qubo size=", len( trains_input.qubo ), " number of Q-bits=", len( our_solution ))
    print("energy=", trains_input.energy( our_solution ))
    print("energy + ofset=", trains_input.energy( our_solution ) + trains_input.sum_ofset)
    print("QUBO objective=", trains_input.objective_val( our_solution ), "  ILP objective=", lp_solution["objective"] )

    print("broken (sum, headway, pass, circ)", trains_input.count_broken_constrains( our_solution ))
    print("broken MO", trains_input.broken_MO_conditions( our_solution ))

    if timetable:
        print(" ........ vars values  ........ ")
        print(" key, qubo, LP ")

        vq = trains_input.qubo2int_vars( our_solution )
        for k, v in vq.items():
            print(k, v.value, lp_solution["variables"][k].value)
        print("  ..............................  ")



def display_prec_feasibility1(trains_input, q_pars, res_dict):
    """ print results of computation """


    print("xxxxxxxxx    RESULTS     xxxxxx ", trains_input.notrains,  "trains xxxxx")
    print("delays", trains_input.delays )
    print("method", q_pars.method)
    print("psum", q_pars.psum)
    print("ppair", q_pars.ppair)
    print("dmax", q_pars.dmax)
    print("LP objective", res_dict["lp objective"])
    print("qubo ofset", res_dict["q ofset"])

    if q_pars.method == "real":
        print("annealing time", q_pars.annealing_time)
    print("no qubits", res_dict["no qubits"])
    print("no qubo terms", res_dict["no qubo terms"])
    print("percentage of feasible", res_dict["perc feasible"])
