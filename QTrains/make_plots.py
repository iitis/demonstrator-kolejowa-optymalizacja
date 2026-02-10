"""plots and auxiliary functions """
import copy
import matplotlib.pyplot as plt
import numpy as np




def passing_time_histigrams1(trains_input, q_pars, results):
    """ returs dict histogram of passing times between staitons in trains_input (objectvive stations) """


    hist_pass = results[f"{trains_input.objective_stations[0]}_{trains_input.objective_stations[1]}"]

    if hist_pass == []:
        hist = {"value":[], "count":[], "stations":trains_input.objective_stations, "no_trains":trains_input.notrains, "dmax":q_pars.dmax,
             "softern":q_pars.softern_pass}
        return hist

    xs = list( range(np.max(hist_pass) + 1) )
    ys = [hist_pass.count(x) for x in xs]

    hist = {"value":xs, "count":ys, "stations":trains_input.objective_stations, "no_trains":trains_input.notrains, "dmax":q_pars.dmax,
             "softern":q_pars.softern_pass}

    return hist


def objective_histograms1(results):
    """ returns dict histogram of objectives"""

    hist_obj = results["qubo objectives"]
    ground = results["lp objective"]

    xs = list(set(hist_obj))
    xs = np.sort(xs)
    ys = [hist_obj.count(x) for x in xs]

    hist = {"value":list(xs), "count":ys, "ground_state":ground}

    return hist



def energies_histograms1(results):
    """ returns dict histogram of energies, feasible and not feasible"""

    hist_feas = results["energies feasible"]
    hist_notfeas = results["energies notfeasible"]
    ground = results["lp objective"] - results["q ofset"]
    # to exclude numerical errors 
    hist_feas = list(np.around(np.array(hist_feas),5))
    xs_f = list(set(hist_feas))
    xs_f = np.sort(xs_f)
    ys_f = [hist_feas.count(x) for x in xs_f]

    xs_nf = list(set(hist_notfeas))
    xs_nf = np.sort(xs_nf)
    ys_nf = [hist_notfeas.count(x) for x in xs_nf]

    hist = {"feasible_value":list(xs_f), "feasible_count":ys_f, "notfeasible_value":list(xs_nf), "notfeasible_count":ys_nf, "ground_state":ground}

    return hist

##### plots

def plot_title(no_trains):
    """ title for plot of passing times """

    if no_trains == 1:
        poc = " 1 pociąg"
    elif no_trains in [2,3,4]:
        poc = f" {no_trains} pociągi"
    else:
        poc = f" {no_trains} pociągów"

    tit = "symulowane wyżarzanie" + poc
    return tit



def _ax_hist_passing_times(ax, hist, add_text = True):
    """ axes for the passing time plots """
    xs = hist["value"]
    ys = hist["count"]
    ax.bar(xs,ys)

    stations = hist["stations"]
    ax.set_xlabel(f"Czas przejazdu {stations}")
    ax.set_ylabel("ilość rozwiązań")
    if add_text:
        k = np.max(ys)/12
        #no_trains = hist["no_trains"]
        #dmax = int(hist["dmax"])
        #ax.text(1,k, f"{no_trains} trains, dmax={dmax}", fontsize=10)

    ax.set_xlim(left=0)
    xx = [i for i in xs if i % 2 == 0]
    ax.set_xticks(xx)


def _ax_objective(ax, hist):
    """ axes for the objective plot """

    xs = hist["value"]
    ys = hist["count"]
    ground = hist["ground_state"]

    ax.bar(list(xs),ys, width = 0.3, color = "gray", label = "sym.")
    ax.axvline(x = ground, lw = 2, color = 'red', linestyle = 'dashed', label = 'opt.')

    ax.legend()
    ax.set_xlabel("Funkcja celu - jakość rozwiązania")
    ax.set_ylabel("częstotliwość")



def plot_hist_pass_obj1(trains_input, q_pars, hist_pass, hist_obj, file_pass, file_obj):
    """ plotting of DWave results """

    fig, ax = plt.subplots(figsize=(4, 3))

    _ax_hist_passing_times(ax, hist_pass)
    our_title = plot_title(hist_pass["no_trains"])
    fig.subplots_adjust(bottom=0.2, left = 0.15)
    plt.title(our_title)
    plt.savefig(file_pass)
    plt.clf()


    fig, ax = plt.subplots(figsize=(4, 3))
    _ax_objective(ax, hist_obj)
    our_title = plot_title(hist_pass["no_trains"])
    fig.subplots_adjust(bottom=0.2, left = 0.15)
    plt.title(our_title)
    plt.savefig(file_obj)
    plt.clf()




# train diagrams

def train_path_data(v, p, exclude_st = "", initial_tt = False):
    """
    returns dict, input to train diagram plotter

    input:
    - v - dict - solution in integer variables
    - p -  Parameters class
    - exclude_st = "" string of excluded stations,
    - initial_tt = False, if True data for initial (conflicted) timetable
    """
    paths = p.trains_paths
    tp = list(paths.values())[0]
    tp = copy.deepcopy(tp)

    if exclude_st != "":
        tp.remove(exclude_st)

    stations_loc = {tp[0]: 0}
    time = 0
    for i in range(len(tp) - 1):
        s = tp[i]
        s1 = tp[i+1]
        time += p.pass_time[f"{s}_{s1}"]
        stations_loc[tp[i+1]] = time
    time += time

    xs = {j:[] for j in paths}
    ys = {j:[] for j in paths}

    for i, j in enumerate( paths ):
        for s in tp:
            for variable in v.values():
                if variable.str_id == f"t_{s}_{j}":
                    if initial_tt:
                        time = variable.range[0]
                    else:
                        time = variable.value
                    ys[j].append(time)
                    if j % 2 == 1:
                        ys[j].append(time + p.stay)
                    else:
                        ys[j].append(time - p.stay)

                    xs[j].append(stations_loc[s])
                    xs[j].append(stations_loc[s])

    return {"space": xs, "time":ys, "stations_loc": stations_loc}


def plot_train_diagrams(input_dict, file, title = ""):
    "plotter of train diagrams"

    xs = input_dict["space"]
    ys = input_dict["time"]
    stations_loc = input_dict["stations_loc"]

    for j in ys.keys():
        plt.plot(ys[j], xs[j], "o-", label=f"p. {j} ", linewidth=0.85, markersize=2)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.63), ncol = 4)

    our_marks = [f"{key}" for key in stations_loc]
    locs = list(stations_loc.values())
    plt.title(f"wykres ruchu {title}")
    plt.yticks(locs, our_marks)
    plt.xlabel("minuty")
    plt.ylabel("stacja")
    plt.subplots_adjust(bottom=0.19, top = 0.70)
    plt.savefig(file)
    plt.clf()
