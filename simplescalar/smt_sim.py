import os
import sys
import pandas as pd

sim = 'sim-outorder'
fastfwd = 2000000000 # 2B
ff = '2B'
max_inst = 1000000000 # 1B
mi = '1B' 
config = './config/oo-smt.cfg'

fetch_policy = [ "icount", "brcount", "mcount" ]

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

stat = { "workload" : [], "IPC" : [] }
fstats = []

def run_smt_sim():
    print(" **** Start SMT Simulation **** ")

    # fstat = ./stats/{workloads}_{nthread}_{fetch_policy}_smt.stats

    for fp in fetch_policy:
    # 1 thread : gcc / bzip2 / gromacs / mcf
        bf_gcc = bin_files["gcc"]
        ifs_gcc = input_files["gcc"]
        itags_gcc = input_tags["gcc"]
        fstat = f'./stats/gcc_1_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 1 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        bf_bzip2 = bin_files["bzip2"]
        ifs_bzip2 = input_files["bzip2"]
        itags_bzip2 = input_tags["bzip2"]
        fstat = f'./stats/bzip2_1_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 1 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_bzip2} {ifs_bzip2[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        bf_gromacs = bin_files["gromacs"]
        ifs_gromacs = input_files["gromacs"]
        itags_gromacs = input_tags["gromacs"]
        fstat = f'./stats/gromacs_1_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 1 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gromacs} {ifs_gromacs[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        bf_mcf = bin_files["mcf"]
        ifs_mcf = input_files["mcf"]
        itags_mcf = input_tags["mcf"]
        fstat = f'./stats/mcf_1_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 1 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_mcf} {ifs_mcf[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

    # 2 threads : gcc + bzip2 / gcc + mcf / bzip2 + mcf 
        fstat = f'./stats/gcc+bzip2_2_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 2 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_bzip2} {ifs_bzip2[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/gcc+mcf_2_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 2 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_mcf} {ifs_mcf[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/mcf+bzip2_2_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 2 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_mcf} {ifs_mcf[0]} + {bf_bzip2} {ifs_bzip2[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/bzip2+gromacs_2_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 2 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_bzip2} {ifs_bzip2[0]} + {bf_gromacs} {ifs_gromacs[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

    # 4 threads : 4 gcc / 4 bzip2 / 2 gcc + 2 bzip2 / gcc + bzip2 + gromacs + mcf
        fstat = f'./stats/gcc_4_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 4 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_gcc} {ifs_gcc[1]} + {bf_gcc} {ifs_gcc[2]} + {bf_gcc} {ifs_gcc[3]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/bzip2_4_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 4 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_bzip2} {ifs_bzip2[0]} + {bf_bzip2} {ifs_bzip2[1]} + {bf_bzip2} {ifs_bzip2[2]} + {bf_bzip2} {ifs_bzip2[3]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/gcc+bzip2_4_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 4 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_gcc} {ifs_gcc[1]} + {bf_bzip2} {ifs_bzip2[0]} + {bf_bzip2} {ifs_bzip2[1]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

        fstat = f'./stats/gcc+bzip2+gromacs+mcf_4_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 4 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_bzip2} {ifs_bzip2[0]} + {bf_gromacs} {ifs_gromacs[0]} + {bf_mcf} {ifs_mcf[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')

    # 8 threads
        fstat = f'./stats/gcc+bzip2+gromacs+mcf_8_{fp}_smt.stats'
        fstats.append(fstat)
        cmd = f'./{sim} -config {config} -smt:nthread 8 -smt:policy {fp} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf_gcc} {ifs_gcc[0]} + {bf_gcc} {ifs_gcc[1]} + {bf_gcc} {ifs_gcc[2]} + {bf_bzip2} {ifs_bzip2[0]} + {bf_bzip2} {ifs_bzip2[1]} + {bf_bzip2} {ifs_bzip2[2]} + {bf_gromacs} {ifs_gromacs[0]} + {bf_mcf} {ifs_mcf[0]}'
        if os.path.exists(fstat) == False:
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')
    
    print(" **** Finish SMT Simulation **** ")

def print_stat():
    for fstat in fstats:
        wl_name = fstat[8:-6]
        stat["workload"].append(wl_name)
        f = open(fstat, "r")
        lines = f.readlines()
        for l in lines:
            words = l.split()
            if "sim_IPC" in l:
                stat["IPC"].append(float(words[1]))

    excel_path = f'./stats/smt.xlsx'
    df = pd.DataFrame(stat)
    with pd.ExcelWriter(excel_path, mode='w', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    

def main():
    run_smt_sim()
    print_stat()

if __name__ == "__main__":
    main()

