# CompArch-Project
SimpleScalar Simulator

## SMT
- `struct thread_t` : `regs`, `mem`, `pc`, `RUU`, `LSQ`, `ruu_fetch_issue_delay`, `icount`, etc. 
- all variables usage related the member variables in `struct thread_t` is modified to consider multithread
- `ruu_fetch` : use ICOUNT.2.8 scheduling policy for fetch
  - fetch dynamically from each thread
  - if high priority thread uses full fetch bandwidth, another thread cannot fetches any insn.
- `ruu_dispatch` : use RR policy for dispatch
- Q. if one thread is blocked due to I-cache/I-TLB miss, should other threads stop fetching?
  - I implemented if one thread is blocked, fetch other threads' instruction from I-cache/I-TLB
- for allocating separate address space for each program, change address space varibles as array variables such as `ld_*_base`, `ld_*_size`, `_prgram`, etc.
 - make new config `config/oo-smt.cfg` : big L1 I-cache / unified L2 cache for multiprocess
