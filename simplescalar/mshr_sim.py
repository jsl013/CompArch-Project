import os
import sys
import pandas as pd

# SimpleScalar's cache is ideal non-blocking cache. It assumes that the number of  MSHR entries is inf.
# So, the goal of this sub-project is to implement available MSHR
# the number of MSHR entries = nmshr, the acceptable number of misses per MSHR entry = mshr_nmisses

# * n:m {nmshr:mshr_nmisses}
# Compare four cases : 1) original SimpleScalar, 2) 1:1 MSHR, 3) 4:2 MSHR, 4) 4:4 MSHR
# The evaluation standard is IPC

sim = 'sim-outorder'
fastfwd = 200000000
max_inst = 200000000
config = './config/oo-default.cfg'

mshr_stat_tags = [ "sim_IPC" ]

spec_bm = [ "bzip2", "gcc", "gromacs", "mcf" ]

bin_files = {
        "bzip2" : "../spec_alpha/bzip2/bzip2_base.alpha",
        "gcc" : "../spec_alpha/gcc/gcc.alpha",
        "gromacs" : "../spec_alpha/gromacs/gromacs_base.alpha",
        "mcf" : "../spec_alpha/mcf/mcf_base.alpha"
# "zeusmp" : "../spec_alpha/zeusmp/zeusmp_base.alpha"
        }

input_files = {
        "bzip2": [
            "../spec_alpha/bzip2/bzip2_input/chicken.jpg 30",
            "../spec_alpha/bzip2/bzip2_input/liberty.jpg 30",
            "../spec_alpha/bzip2/bzip2_input/input.program 280",
            "../spec_alpha/bzip2/bzip2_input/text.html 280",
            "../spec_alpha/bzip2/bzip2_input/input.combined 200",
            ],

        "gcc": [
            "../spec_alpha/gcc/gcc_input/166.i -o ../spec_alpha/gcc/gcc_input/166.s",
            "../spec_alpha/gcc/gcc_input/200.i -o ../spec_alpha/gcc/gcc_input/200.s",
            "../spec_alpha/gcc/gcc_input/c-typeck.i -o ../spec_alpha/gcc/gcc_input/c-typeck.s",
            "../spec_alpha/gcc/gcc_input/cp-decl.i -o ../spec_alpha/gcc/gcc_input/cp-decl.s",
            "../spec_alpha/gcc/gcc_input/expr.i -o ../spec_alpha/gcc/gcc_input/expr.s",
            "../spec_alpha/gcc/gcc_input/expr2.i -o ../spec_alpha/gcc/gcc_input/expr2.s",
            "../spec_alpha/gcc/gcc_input/g23.i -o ../spec_alpha/gcc/gcc_input/g23.s",
            "../spec_alpha/gcc/gcc_input/s04.i -o ../spec_alpha/gcc/gcc_input/s04.s",
            "../spec_alpha/gcc/gcc_input/scilab.i -o ../spec_alpha/gcc/gcc_input/scilab.s"
            ],

        "gromacs":[
            "-silent -deffnm ../spec_alpha/gromacs/gromacs_base.alpha -nice 0"
            ],

        "mcf":[
            "../spec_alpha/mcf/mcf_input/inp.in"
            ]
        }

input_tags = {
        "bzip2": ["chicken_jpg", "liberty_jpg", "input_program", "text_html", "input_combined"],
        "gcc": ["166", "200", "c-typeck", "cp-decl", "expr", "expr2", "g23", "s04", "scilab"],
        "gromacs":["gromacs"],
        "mcf": ["inp"]
        }

stat = { "IPC" : [], "Origin" : [], "2:2 MSHR" : [], "4:2 MSHR" : [], "8:4 MSHR" : [] }

mshr_opt = ["0:0", "2:2", "4:2", "8:4"]

def run_mshr_sim():
    print(" **** Start MSHR Simulation **** ")
    for bm in spec_bm:
        bf = bin_files[bm]
        ifs = input_files[bm]
        itags = input_tags[bm]
        for i in range(len(ifs)):
            for opt in mshr_opt: # 0:0 = original simplescalar
                fstat = f'./stats/{bm}_{itags[i]}_mshr_{opt}.stats'
# if os.path.exists(fstat):
# continue
                cmd = f'./{sim} -config {config} -fastfwd {fastfwd} -max:inst {max_inst} -cache:mshr {opt} -redir:sim {fstat} {bf} {ifs[i]}'
                fail = os.system(cmd)
                if fail:
                    print(f'Command fail: {cmd}')
    print(" **** Finish MSHR Simulation **** ")

def print_stat():
    stat["IPC"] = []
    for bm in spec_bm:
        itags = input_tags[bm]
        for it in itags:
            stat["IPC"].append(f'{bm}-{it}')
            for opt in mshr_opt:
                if opt == "0:0":
                    stat_name = "Origin"
                if opt == "2:2":
                    stat_name = "2:2 MSHR"
                if opt == "4:2":
                    stat_name = "4:2 MSHR"
                if opt == "8:4":
                    stat_name = "8:4 MSHR"
                fstat = f'./stats/{bm}_{it}_mshr_{opt}.stats'
                f = open(fstat, "r")
                lines = f.readlines()
                for l in lines:
                    words = l.split()
                    if "sim_IPC" in l:
                        stat[stat_name].append(float(words[1]))

    excel_path = f'./stats/mshr.xlsx'
    df = pd.DataFrame(stat)
    with pd.ExcelWriter(excel_path, mode='w', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

def main():
    run_mshr_sim()
    print_stat()

if __name__ == "__main__":
    main()

