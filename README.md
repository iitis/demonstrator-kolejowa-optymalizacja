# 

---

````markdown
## Konfiguracja środowiska (Linux)

Projekt wykorzystuje izolowane środowisko Pythona, aby zapewnić
powtarzalność wyników oraz zgodność wersji bibliotek.

Wszystkie polecenia należy wykonać w katalogu głównym repozytorium.

---

### 1. Utworzenie środowiska wirtualnego

```bash
python3 -m venv .venv
````

---

### 2. Aktywacja środowiska

```bash
source .venv/bin/activate
```

Po aktywacji w linii poleceń pojawi się prefiks:

```
(.venv)
```

---

### 3. Aktualizacja pip

```bash
pip install --upgrade pip
```

---

### 4. Instalacja zależności

```bash
pip install -r requirements.txt
```

---

### 5. Dezaktywacja środowiska

```bash
deactivate
```

---

## Każde kolejne uruchomienie projektu

Wystarczy ponownie aktywować środowisko:

```bash
source .venv/bin/activate
```

```
```


# quantum-stochastic-optimization-railways
Application of quantum computation for stochastic optimization on the example of railway/tramway network in Baltimore.

Files:

1. ```QTrains``` - source code
2. ```tests``` - testing source code

3. ```solutions``` - stored solutions of railway problems, if for particular parameters setting computations have already been stored, new computation will not be performed and the particular file will not be overwritten
4. ```QUBOs``` - qubos of railway problems
5. ```histograms``` - histograms from data analysis



#### Solving trains problem 

In ```process_q_annealing.py ``` trains scheduling problems are solved via Integer Linear Programming and quantum (or simulated) annealing

Arguments:

- --mode MODE: 1: make, computation (ILP and annealing), 5: CPLEX benchmark 
- --softern_pass SOFTERN_PASS: if true analyze output without feasibility check on a minimal passing time constrain - by default: False


Example usage:

```python3 process_q_annealing.py --mode 1```

Solve the series of problems by simulated annealing and ILP.

```python3 process_q_annealing.py --mode 5```

CPLEX benchmarking.



# Funding

Scientific work co-financed from the state budget under the program of the Minister of Education and Science, Poland (pl. Polska) under the name "Science for Society II" project number NdS-II/SP/0336/2024/01 funding amount ```1000000``` PLN total value of the project ```1000000``` PLN 
