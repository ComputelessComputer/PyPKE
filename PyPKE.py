from tqdm import tqdm
import argparse
import sys

# The file path where you are going to save the *.dat file
# The default directory will be where you place your PyPKE.py at
# For example, if you run PyPKE.py on your Desktop directory,
# the *.dat file will be made there too
file_path = './'
parameters_file_name = 'kinetics_parameters.txt'

# constants for ramp function
super_small = -100000000
threshold = 0.000001

# This function reads the K.P. input text file
def read_kinetics_parameters(name):
    f = open(file_path + parameters_file_name, 'rt')
    beta_str_list, lda_str_list = [], []
    life = 0.0001
    name = '[' + name + ']'

    while True:
        line = f.readline()
        if '<END>' in line:
            sys.exit('There is no match!')
        if name in line:
            line = f.readline()
            if '<Beta>' in line:
                line = f.readline()
                beta_str_list = line.split()
            line = f.readline()
            if '<Lambda>' in line:
                line = f.readline()
                lda_str_list = line.split()
            line = f.readline()
            if '<Life-time>' in line:
                line = f.readline()
                life = float(line)
            break
    f.close()
    beta, lda = [], []
    for beta_str in beta_str_list:
        beta.append(float(beta_str))
    for lda_str in lda_str_list:
        lda.append(float(lda_str))
    print('Kinetics parameters being used in PyPKE are the following,\nBeta\n',beta,'\nLambda\n', lda, '\nPrompt neutron life time\n', life)
    return [beta, lda, life]


class PKE(object):
    def __init__(self, reactivity=0, mode_number=0):
        print('Welcome to PyPKE!\nIf you want more information about the program,\n'
              'please refer to the README.md or visit the GitHub URL.\n'
              'https://github.com/ComputelessComputer/PyPKE')
        # default kinetics parameters are based on AGN-201K from KHU
        print('\nThese are the names for the various kinetic parameters serviced by '
              'PyPKE\n========================================================================\n'
              'AGN-201K\n'
              'REFERENCE-1\n')
        self.name = input('Please enter the kinetics parameters model name: ')
        self.name = self.name.upper()
        self.beta, self.lda, self.life = read_kinetics_parameters(self.name)
        self.time_step = 0.0001
        self.rho = reactivity
        self.mode = mode_number
        self.gen = self.life * (1 - self.rho)
        self.neutron_density = 1
        self.precursor_density = []
        for i in range(6):
            precursor_initial = self.beta[i] / self.lda[i] / self.gen
            self.precursor_density.append(precursor_initial)

    # Update for ramp
    def reactivity_function(self, time):
        end_point = -4.624780 * sum(self.beta)
        if time < 47:
            self.rho = time * end_point / 47
        else:
            self.rho = end_point

    def neutron(self, time):
        time = time // self.time_step * self.time_step
        if time == 0:
            return self.neutron_density
        else:
            res = self.neutron_density * (1 + self.time_step * (self.rho - sum(self.beta)) / self.gen)
            for i in range(6):
                res += self.time_step * self.lda[i] * self.precursor_density[i]
            #self.update_neutron(res)
            return res

    def precursor(self, index, time):
        time = time // self.time_step * self.time_step
        if time == 0:
            return self.precursor_density[index]
        else:
            res = self.precursor_density[index] * (1 - self.time_step * self.lda[index]) \
                  + self.time_step * self.beta[index] / self.gen * self.neutron_density
            #self.update_precursor(res, index)
            return res

    def update_neutron(self, neutron):
        self.neutron_density = neutron

    def update_precursor(self, precursor, i):
        self.precursor_density[i] = precursor

    def run(self):
        rho_string = "{:.4f}".format(self.rho)
        file_name = ""
        if self.mode == 0:
            file_name += "[Step] "
        elif self.mode == 1:
            file_name += "[Ramp] "
        file_name += 'PyPKE_rho=' + rho_string + '_kp=' + self.name + '.dat'
        f = open(file_path + file_name, 'wt')
        print('Writing neutron and precursor data from 0s to 100s')
        for val in tqdm(range(int(100 / self.time_step))):
            t = val * self.time_step
            if self.mode == 1:
                self.reactivity_function(t)
            neutron_density = self.neutron(t)
            precursor_density = []
            for j in range(6):
                precursor_density.append(self.precursor(j, t))

            self.update_neutron(neutron_density)
            for i in range(6):
                self.update_precursor(precursor_density[i], i)

            if val % 100 == 0:
                f.write('%.4f' % t + " ")
                f.write('{:.4e}'.format(neutron_density) + " ")
                for j in range(6):
                    f.write('{:.4e}'.format(precursor_density[j]) + " ")
                f.write("\n")
        f.close()


def main(arg1, arg2):
    pke = PKE(arg1, arg2)
    pke.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", help="Multiplication factor", type=float)
    parser.add_argument("--r", help="Reactivity", type=float)
    parser.add_argument("--mode", help="default : step / 1 : ramp_dec / 2: ramp_inc", type=int)
    args = parser.parse_args()
    tmp = 0
    if args.k:
        print('Multiplication mode', end=' ')
        tmp = 1 - 1 / args.k
    if args.r:
        print('Reactivity mode', end=' ')
        tmp = args.r
    if args.mode == 0:
        print("+ step function\n")
    elif args.mode == 1:
        print("+ ramp function\n")
    main(tmp, args.mode)
