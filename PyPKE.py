from tqdm import tqdm
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np

# The file path where you are going to save the *.dat file
# The default directory will be where you place your PyPKE.py at
# For example, if you run PyPKE.py on your Desktop directory,
# the *.dat file will be made there too
file_path = './'
parameters_file_name = 'kinetics_parameters.txt'


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
    print('Kinetics parameters being used in PyPKE are the following,\nBeta\n>>', beta, '\nLambda\n>>', lda,
          '\nPrompt neutron life time\n', life)
    return [beta, lda, life]


class PKE(object):
    def __init__(self, mode_number=0, output_number=0):
        print("+--------------------------------------------------------+\n"
              "|                    Welcome to PyPKE!                   |\n"
              "| A numerical analysis of the point kinetics equation.   |\n"
              "| If you want more information about the program,        |\n"
              "| please refer to the README.md or visit the GitHub URL. |\n"
              "| https://github.com/ComputelessComputer/PyPKE           |\n"
              "+--------------------------------------------------------+")
        # default kinetics parameters are based on AGN-201K from KHU
        print("\nThese are the names for the various kinetic parameters serviced by "
              "PyPKE\n========================================================================\n"
              "AGN-201K\n"
              "REFERENCE-1\n")
        self.name = input("Please enter the kinetics parameters model name: ")
        self.name = self.name.upper()
        self.beta, self.lda, self.life = read_kinetics_parameters(self.name)
        self.time_step = 0.0001
        self.output_number = output_number
        # mode number decides the reactivity function modes
        self.mode = mode_number
        self.rho = 0
        # For ramp
        self.rho_initial, self.rho_final, self.time_taken = 0, 0, 0
        self.rho_input()

        # coefficients determined by rho
        self.gen = self.life * (1 - self.rho)
        self.neutron_density = 1
        self.precursor_density = []
        for i in range(6):
            precursor_initial = self.beta[i] / self.lda[i] / self.gen
            self.precursor_density.append(precursor_initial)

    def rho_input(self):
        print("\nPlease insert coefficients for reactivity function\n")
        if self.mode == 0:
            print("Step function\n")
            self.rho = float(input("Initial reactivity : "))
        elif self.mode == 1:
            print("Ramp function\n")
            self.rho_initial = float(input("Initial reactivity : "))
            self.rho_final = float(input("Final reactivity   : "))
            self.time_taken = float(input("Time taken         : "))
            self.rho = self.rho_initial

    # Update for ramp decline
    def ramp_reactivity(self, time):
        if time < self.time_taken:
            self.rho = self.rho_initial + (self.rho_final - self.rho_initial) / self.time_taken * time
        else:
            self.rho = self.rho_final

    def neutron(self, time):
        time = time // self.time_step * self.time_step
        if time == 0:
            return self.neutron_density
        else:
            res = self.neutron_density * (1 + self.time_step * (self.rho - sum(self.beta)) / self.gen)
            for i in range(6):
                res += self.time_step * self.lda[i] * self.precursor_density[i]
            return res

    def precursor(self, index, time):
        time = time // self.time_step * self.time_step
        if time == 0:
            return self.precursor_density[index]
        else:
            res = self.precursor_density[index] * (1 - self.time_step * self.lda[index]) \
                  + self.time_step * self.beta[index] / self.gen * self.neutron_density
            return res

    def update_neutron(self, neutron):
        self.neutron_density = neutron

    def update_precursor(self, precursor, i):
        self.precursor_density[i] = precursor

    def run(self):
        # Decision of file name and opening it
        rho_string = "{:.6f}".format(self.rho)
        file_name = ""
        if self.mode == 0:
            file_name += "[Step] "
        elif self.mode == 1:
            file_name += "[Ramp] "
        file_name += 'PyPKE_rho_init=' + rho_string + '_kp=' + self.name

        if self.output_number == 0 or self.output_number == 2:
            dat_file_name = file_name
            dat_file_name += '.dat'
            f = open(file_path + file_name, 'wt')

            # Writing neutron and precursor density data from 0s to 100s
            print('\nWriting neutron and precursor data from 0s to 100s\n')
            for val in tqdm(range(int(100 / self.time_step))):
                t = val * self.time_step
                if self.mode == 1:
                    self.ramp_reactivity(t)
                neutron_density = self.neutron(t)
                precursor_density = []
                for j in range(6):
                    precursor_density.append(self.precursor(j, t))

                self.update_neutron(neutron_density)
                for i in range(6):
                    self.update_precursor(precursor_density[i], i)

                if val % 100 == 0:
                    f.write('%.6f' % t + " ")
                    f.write('{:.6e}'.format(neutron_density) + " ")
                    for j in range(6):
                        f.write('{:.6e}'.format(precursor_density[j]) + " ")
                    f.write("\n")
            f.close()

        if self.output_number == 1 or self.output_number == 2:
            plt_file_name = file_name
            plt_file_name += '.png'

            neutron_density_record = []
            for val in tqdm(range(int(100 / self.time_step))):
                t = val * self.time_step
                if self.mode == 1:
                    self.ramp_reactivity(t)
                neutron_density = self.neutron(t)
                precursor_density = []
                for j in range(6):
                    precursor_density.append(self.precursor(j, t))

                self.update_neutron(neutron_density)
                for i in range(6):
                    self.update_precursor(precursor_density[i], i)

                neutron_density_record.append(neutron_density)

            neutron_density_record = np.array(neutron_density_record)
            plt.title(file_name)
            plt.grid(True)
            plt.xlabel('Time [s]')
            plt.ylabel('Neutron density ratio')
            plt.xlim([0, 100])
            plt.plot(np.arange(0, 100, self.time_step), neutron_density_record, 'b-')
            plt.savefig(plt_file_name, dpi=300)


def main(arg1, arg2):
    pke = PKE(arg1, arg2)
    pke.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', "--function", help="0(default) : step / 1 : ramp", type=int)
    parser.add_argument('-O', "--output", help="0(default) : *.dat only / 1 : graph only / 2 : both", type=int)
    args = parser.parse_args()
    arg1, arg2 = 0, 0

    if args.function == 0 or args.function is None:
        print("Initializing PyPKE with step reactivity function")
    elif args.function == 1:
        arg1 = 1
        print("Initializing PyPKE with ramp reactivity function")
    else:
        sys.exit('There is no such reactivity function!')

    if args.output == 0 or args.output is None:
        print("Output file : text only\n")
    elif args.output == 1:
        arg2 = 1
        print("Output file : graph only\n")
    elif args.output == 2:
        arg2 = 2
        print("Output file : text and graph\n")
    else:
        sys.exit('There is no such output mode!')

    main(arg1, arg2)
