# PyPKE

## Purpose
Solving the Point kinetics equation via Taylor expansion

## How it began
Final project to Nuclear Reactor Physics Experiment 2020 spring semester in SNU

## How to install PyPKE
1. Git clone to local environment or virtual environment
```
$ git clone https://github.com/ComputelessComputer/PyPKE
Cloning into 'PyPKE'...
remote: Enumerating objects: 21, done.
remote: Counting objects: 100% (21/21), done.
remote: Compressing objects: 100% (20/20), done.
remote: Total 21 (delta 4), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (21/21), done.
```

2. Install required packages
```
$ pip install -r requirements.txt
Requirement already satisfied: tqdm in /opt/anaconda3/lib/python3.7/site-packages (from -r requirements.txt (line 1)) (4.36.1)
```

3. Run the program - See [Basic options] for more information
```
$ python PyPKE.py
```

## Basic options
1. To see options
```
$ python PyPKE.py -h
usage: PyPKE.py [-h] [--k K] [--r R] [--mode MODE]

optional arguments:
  -h, --help   show this help message and exit
  --k K        Multiplication factor
  --r R        Reactivity
  --mode MODE  default : step / 1 : ramp_dec / 2: ramp_inc
```
2. Reactivity mode
```
$ python PyPKE.py --r 0.001
```
3. Selecting reactivity change function
```
$ python PyPKE.py --mode 1
```
4. They can be typed in altogether
```
$ python PyPKE.py --r 0.001 --mode 0
Welcome to PyPKE!
If you want more information about the program,
please refer to the README.md or visit the GitHub URL.
https://github.com/ComputelessComputer/PyPKE

These are the names for the various kinetic parameters serviced by PyPKE
========================================================================
AGN-201K
REFERENCE-1

Please enter the kinetics parameters model name: agn-201k
Kinetics parameters being used in PyPKE are the following,
Beta
 [0.000331, 0.002198, 0.001963, 0.003972, 0.001156, 0.000465] 
Lambda
 [0.0124, 0.0305, 0.111, 0.301, 1.13, 3.0] 
Prompt neutron life time
 0.0001
Writing neutron and precursor data from 0s to 100s
100%|███████████████████████████████████████████████████████████████████████████████| 1000000/1000000 [00:08<00:00, 111892.13it/s]
```
## To be continued...
