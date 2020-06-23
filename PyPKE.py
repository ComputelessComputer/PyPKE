from tqdm import tqdm
import argparse
import sys

# file path where you are going to save the *.dat file
file_path = 'C:/Users/John/Desktop/PKE_data/RodDrop/'

# constants for ramp function
super_small = -100000000
threshold = 0.000001


class PKE(object):
    def __init__(self, reactivity=0, mode_number=0):
        self.beta = [0.000331, 0.002198, 0.001963, 0.003972, 0.001156, 0.000465]
        self.lda = [0.0124, 0.0305, 0.1110, 0.3010, 1.1300, 3.0000]
        #self.beta = [0.000266, 0.001491, 0.001316, 0.002849, 0.000896, 0.000182]
        #self.lda = [0.0127, 0.0317, 0.155, 0.311, 1.4, 3.87]
        self.time_step = 0.0001
        self.rho = reactivity
        self.life = 1E-4
        #self.life = 0.00002
        self.mode = mode_number
        self.gen = self.life * (1 - self.rho)
        #self.gen = 0.00002
        self.neutron_density = 1
        self.precursor_density = []
        for i in range(6):
            tmp = self.beta[i] / self.lda[i] / self.gen
            self.precursor_density.append(tmp)

    # Update for ramp
    def reactivity_function(self, time):
        end_point = -4.624780 * sum(self.beta)
        if time < 47:
            self.rho = time * end_point / 47
        else:
            self.rho = end_point

    def neutron(self, time):
        time = time // self.time_step * self.time_step
        if time - self.time_step == 0:
            return self.neutron_density
        else:
            res = self.neutron_density * (1 + self.time_step * (self.rho - sum(self.beta)) / self.gen)
            for i in range(6):
                res += self.time_step * self.lda[i] * self.precursor_density[i]
            #self.update_neutron(res)
            return res

    def precursor(self, index, time):
        time = time // self.time_step * self.time_step
        if time - self.time_step == 0:
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
            file_name += "[Step]"
        elif self.mode == 1:
            file_name += "[Ramp]"
        file_name += 'PyPKE_rho=' + rho_string + '.dat'
        f = open(file_path + file_name, 'wt')
        # data until 300s
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
        tmp = 1 - 1 / args.k
    if args.r:
        tmp = args.r
    if args.mode == 0:
        print("Mode 0 : step function")
    elif args.mode == 1:
        print("Mode 1 : ramp function")
    main(tmp, args.mode)
