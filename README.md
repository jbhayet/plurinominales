# plurinominales
Simulation of different methods for selecting MPs in Mexican Elections with a proportional scheme. The data in use here are those of the 2021 election (in the data/ folder). 

You may use:
* An assignation at the nation/state level (option --national).
* Use different methods to perform the **initial assignation** (option -m): Majority, D'Hondt, Saint Lague, Hare, Danish, Hagenbasch.
* Use different methods to correct the non-proportionality (option -c): Rojas, Sánchez

For example:
```python
python run_simulation.py -m hare -c sanchez
```
