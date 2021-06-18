# CompArch-Project
SimpleScalar Simulator

## SMT
- Modified
  - `struct thread_t` : `regs`, `mem`, `pc`, `RUU`, `LSQ`, `ruu_fetch_issue_delay`, `icount`, etc,.. 
  - all variables usage related the member variables in `struct thread_t` is modified to consider multithread
  - `ruu_fetch` : use ICOUNT 2.8 scheduling policy for fetching
    - Q. if one thread is blocked due to I-cache/I-TLB miss, should other threads stop fetching?
