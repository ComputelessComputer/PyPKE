# PyPKE

## Introduction
### Purpose
Solving the Point kinetics equation via Taylor expansion
### How it began
Final project to Nuclear Reactor Physics Experiment 2020 spring semester in SNU
### Open-source project
If you have any suggestions to improve PyPKE, please contact via e-mail; botsforme@snu.ac.kr

## How to install PyPKE
1. Git clone to local environment or virtual environment
```
$ git clone https://github.com/ComputelessComputer/PyPKE
```

2. Install required packages
```
$ pip install -r requirements.txt
```
If this doesn't work, that is probably because you do NOT have pip installed in your environment.

```
$ sudo apt install python-pip
...
```
  Also, you might want to check your Python version.
```
$ python -V
Python 3.6.9
```
If the version is 3.X, you will have no problem running PyPKE.
  
## To see help
```
$ python PyPKE.py -h
usage: PyPKE.py [-h] [-F FUNCTION] [-O OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -F FUNCTION, --function FUNCTION
                        0(default) : step / 1 : ramp
  -O OUTPUT, --output OUTPUT
                        0(default) : *.dat only / 1 : graph only / 2 : both
```
## Run the program
1. Running in default mode: step reactivity + .dat file output only
```
$ python PyPKE.py
```
2. You can now select the kinetic parameters given by different experiments.
The parameters can be typed in as lower case.
```
Initializing PyPKE with step reactivity function
Output file : text only

+--------------------------------------------------------+
|                    Welcome to PyPKE!                   |
| A numerical analysis of the point kinetics equation.   |
| If you want more information about the program,        |
| please refer to the README.md or visit the GitHub URL. |
| https://github.com/ComputelessComputer/PyPKE           |
+--------------------------------------------------------+

These are the names for the various kinetic parameters serviced by PyPKE
========================================================================
AGN-201K
REFERENCE-1

Please enter the kinetics parameters model name:
```
3. By choosing AGN-201K, the next input for reactivity shows up.
```
Please enter the kinetics parameters model name: agn-201k
Kinetics parameters being used in PyPKE are the following,
Beta
>> [0.000331, 0.002198, 0.001963, 0.003972, 0.001156, 0.000465]
Lambda
>> [0.0124, 0.0305, 0.111, 0.301, 1.13, 3.0]
Prompt neutron life time
 0.0001

Please insert coefficients for reactivity function

Step function

Initial reactivity : 
```
4. By typing in arbitrary input values, the result will be created via current directory.
```
Initial reactivity : -.0001
100%|██████████████████████████████████████████████████████████████████████████████| 1000000/1000000 [00:07<00:00, 131821.78it/s]
```

## Graph output
PyPKE currently supports graphs for neutron-density ratio. (Will soon support precursor-density ratio plot.)
```
(untitled) C:\Users\John\PycharmProjects\untitled>python PyPKE.py -O 1
Initializing PyPKE with step reactivity function
Output file : graph only

+--------------------------------------------------------+
|                    Welcome to PyPKE!                   |
| A numerical analysis of the point kinetics equation.   |
| If you want more information about the program,        |
| please refer to the README.md or visit the GitHub URL. |
| https://github.com/ComputelessComputer/PyPKE           |
+--------------------------------------------------------+

These are the names for the various kinetic parameters serviced by PyPKE
========================================================================
AGN-201K
REFERENCE-1

Please enter the kinetics parameters model name: agn-201k
Kinetics parameters being used in PyPKE are the following,
Beta
>> [0.000331, 0.002198, 0.001963, 0.003972, 0.001156, 0.000465]
Lambda
>> [0.0124, 0.0305, 0.111, 0.301, 1.13, 3.0]
Prompt neutron life time
 0.0001

Please insert coefficients for reactivity function

Step function

Initial reactivity : -.0001
100%|██████████████████████████████████████████████████████████████████████████████| 1000000/1000000 [00:07<00:00, 131821.78it/s]
```
The graph will be stored in the current directory as .png format.
![alt text](https://github.com/ComputelessComputer/PyPKE/blob/[branch]/image.jpg?raw=true)
## To be continued...
