import os
import sys
import pandas as pd

sim = 'sim-outorder'
fastfwd = 2000000000 # 2B
ff = '2B'
max_inst = 1000000000 # 1B
mi = '1B' 
config = './config/oo-fmt.cfg'
n_stack = 3 # naive, FMT, sFMT

fmt_stat_tags = [ "FMT_il1", "FMT_il2", "FMT_itlb", "FMT_dl1", "FMT_dl2", "FMT_dtlb", "FMT_bpenalty" ]
sfmt_stat_tags = [ "sFMT_il1", "sFMT_il2", "sFMT_itlb", "sFMT_dl1", "sFMT_dl2", "sFMT_dtlb", "sFMT_bpenalty" ]
naive_stat_tags = [ "il1.misses", "ul2.misses", "itlb.misses", "dl1.misses", "dtlb.misses", "naive_bpenalty" ]
# naive_stats = [ "naive_il1", "naive_il2", "naive_itlb", "naive_dl1", "naive_dl2", "naive_dtlb", "naive_bpenalty" ]
naive_penalty = { "il1.misses" : 9, "ul2.misses" : 250, "itlb.misses" : 30,
                  "dl1.misses" : 9, "dtlb.misses" : 30,
                  "naive_bpenalty" : 5 }

spec_bm = [ "bzip2", "gcc", "gromacs", "mcf" ]

bin_files = {
        "bzip2" : "../spec_alpha/bzip2/bzip2_base.alpha",
        "gcc" : "../spec_alpha/gcc/gcc.alpha",
        "gromacs" : "../spec_alpha/gromacs/gromacs_base.alpha"
        "mcf" : "../spec_alpha/mch/mcf_base.alpha"
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
        "bzip2": [
            "chicken_jpg",
            "liberty_jpg",
            "input_program",
            "text_html",
            "input_combined",
            ],

        "gcc": [
            "166",
            "200",
            "c-typeck",
            "cp-decl",
            "expr",
            "expr2",
            "g23",
            "s04",
            "scilab"
            ],

        "gromacs":[
            "gromacs"
            ],

        "mcf":[
            "inp"
            ]
        }

stat = {}

def get_cpi_stack():
    sim_cycle = stat["sim_cycle"]
    fmt_base = [1 for i in range(len(sim_cycle))]
    sfmt_base = [1 for i in range(len(sim_cycle))]
    naive_base = [1 for i in range(len(sim_cycle))]
    stat["FMT_base"] = [] 
    for tag in fmt_stat_tags:
        s = stat[tag]
        stat[f'{tag}_rate'] = [float(x / y) for x, y in zip(s, sim_cycle)]  
# print(f'{tag}_rate :', stat[f'{tag}_rate'])
        fmt_base = [x - y for x, y in zip(fmt_base, stat[f'{tag}_rate'])]
    stat["FMT_base"] = [] 
    for tag in sfmt_stat_tags:
        s = stat[tag]
        stat[f'{tag}_rate'] = [float(x / y) for x, y in zip(s, sim_cycle)]  
        sfmt_base = [x - y for x, y in zip(sfmt_base, stat[f'{tag}_rate'])]
# print(f'{tag}_rate :', stat[f'{tag}_rate'])
    stat["FMT_base"] = [] 
    for tag in naive_stat_tags:
        s = stat[tag]
        stat[f'{tag}_rate'] = [float(x / y)*naive_penalty[tag] for x, y in zip(s, sim_cycle)]  
        naive_base = [x - y for x, y in zip(naive_base, stat[f'{tag}_rate'])]
# print(f'{tag}_rate :', stat[f'{tag}_rate'])
    stat["FMT_base"] = fmt_base
    stat["sFMT_base"] = sfmt_base
    stat["naive_base"] = naive_base
# print(stat)
    

def run_fmt_sim():
    print(" **** Start FMT Simulation **** ")
    for bm in spec_bm:
        bf = bin_files[bm]
        ifs = input_files[bm]
        itags = input_tags[bm]
        for i in range(len(ifs)):
            fstat = f'./stats/{bm}_{itags[i]}_{ff}_{mi}.stats'
# if os.path.exists(fstat):
# continue
            cmd = f'./{sim} -config {config} -fastfwd {fastfwd} -max:inst {max_inst} -redir:sim {fstat} {bf} {ifs[i]}'
            fail = os.system(cmd)
            if fail:
                print(f'Command fail: {cmd}')
    print(" **** Finish FMT Simulation **** ")

def print_stat():
    stat["workload"] = []
    stat["sim_cycle"] = []
    for tag in naive_stat_tags:
        stat[tag] = []
    for tag in fmt_stat_tags:
        stat[tag] = []
    for tag in sfmt_stat_tags:
        stat[tag] = []
    for bm in spec_bm:
        itags = input_tags[bm]
        for it in itags:
            stat["workload"].append(f'{bm}-{it}')
            fstat = f'./stats/{bm}_{it}_{ff}_{mi}.stats'
            f = open(fstat, "r")
            lines = f.readlines()
            for l in lines:
                words = l.split()
                if "sim_cycle" in l:
                    stat["sim_cycle"].append(int(words[1]))
                for tag in fmt_stat_tags:
                    if tag in l and (f's{tag}' not in l):
                        stat[tag].append(int(words[1]))
                for tag in sfmt_stat_tags:
                    if tag in l:
                        stat[tag].append(int(words[1]))
                for tag in naive_stat_tags:
                    if tag in l:
                        stat[tag].append(int(words[1]))
    cpi_stack = get_cpi_stack()

# for key in stat.keys():
# print(key, len(stat[key]))

    excel_path = f'./stats/fmt.xlsx'
    df = pd.DataFrame(stat)
    with pd.ExcelWriter(excel_path, mode='w', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)


def main():
    run_fmt_sim()
    print_stat()

if __name__ == "__main__":
    main()
