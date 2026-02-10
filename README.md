# 

---


# Konfiguracja środowiska Python

Projekt wykorzystuje izolowane środowisko Pythona, aby zapewnić powtarzalność wyników oraz zgodność wersji bibliotek.  

Wszystkie polecenia należy wykonywać w katalogu głównym repozytorium.

---

## 1. Utworzenie środowiska wirtualnego

```bash
# Linux / macOS
python3 -m venv .venv

# Windows (PowerShell lub CMD)
python -m venv .venv
```
---

### 2. Aktywacja środowiska

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat

```


---

### 3. Aktualizacja pip

```bash
# Linux / macOS
pip install --upgrade pip

# Windows
pip install --upgrade pip

```

---

### 4. Instalacja zależności

```bash
# Linux / macOS
pip install -r requirements.txt

# Windows
pip install -r requirements.txt

```

---

### 5. Dezaktywacja środowiska

```bash
# Linux / macOS
deactivate

# Windows
deactivate

```

---

### 6. Każde kolejne uruchomienie projektu

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat
```


---

# quantum-stochastic-optimization-railways

Zastosowanie obliczeń kwantowych do optymalizacji stochastycznej na przykładzie sieci kolejowej / tramwajowej w Baltimore.

Pliki:

1. `QTrains` – kod źródłowy

2. `tests` – kod testowy

3. `solutions` – zapisane rozwiązania problemów kolejowych; jeśli dla określonych parametrów obliczenia zostały już wykonane i zapisane, nowe obliczenia nie będą uruchamiane, a plik nie zostanie nadpisany

4. `QUBOs` – formulacje QUBO dla problemów kolejowych

5. `histograms` – histogramy z analizy danych

---

#### Rozwiązywanie problemu pociągów

W `computation.py` problemy harmonogramowania pociągów są rozwiązywane za pomocą programowania liniowego całkowitoliczbowego (ILP) oraz kwantowego (symulowanego) wyżarzania.

Argumenty:

* `--notrains` – liczba pociągów w problemie harmonogramowania


Przykład użycia:

```bash
python3 computation.py --notrains 2
```

Rozwiązuje serię problemów przy użyciu symulowanego wyżarzania oraz ILP.

---



# Finansowanie

Materiał dofinansowana ze środków budżetu państwa w ramach programu Ministra Edukacji i Nauki pod nazwą
„Nauka dla Społeczeństwa II”: nr projektu NdSII/SP/0336/2024/01, kwota dofinansowania ```1 000 000``` PLN, całkowita wartość projektu ```1 000 000``` PLN
