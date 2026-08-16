Student Information
Full name: JERONIMO RESTREPO CARDONA
Class number: C2666-SI2002-4855
Environment
Operating System: Windows 11
Programming language: Python 3.12.3
Tools used: No external libraries required (only the Python standard library, sys).
How to Run
Make sure Python 3 is installed. On Linux/macOS it is usually available as python3; on Windows it is usually python.
Place the input file (e.g. input.txt) in the same directory as minimizar.py, following the input format described in the assignment.
Run the program, feeding the input file into standard input.

On Linux / macOS (bash/zsh):

bash
python3 minimizar.py < input.txt

To save the output to a file instead of printing it to the console:

bash
python3 minimizar.py < input.txt > output.txt

On Windows (PowerShell):

PowerShell does not support the < redirection operator, so Get-Content is used together with a pipe instead:

powershell
Get-Content input.txt | python minimizar.py

To save the output to a file:

powershell
Get-Content input.txt | python minimizar.py > output.txt

On Windows (cmd.exe / Command Prompt):

The classic Windows Command Prompt does support <, so the same syntax as bash works:

Algorithm Explanation

This program implements the table-filling algorithm for DFA minimization, as presented in Kozen (1997), Automata and Computability, Lecture 14.

Given a DFA M = (Q, Σ, δ, s, F) with no inaccessible states, the goal is to find every pair of states (p, q) that are equivalent — that is, states that cannot be distinguished by any input string. Formally, p and q are equivalent if and only if, for every string x ∈ Σ*, δ̂(p, x) ∈ F exactly when δ̂(q, x) ∈ F.

The algorithm works by doing the opposite: instead of directly proving equivalence, it iteratively marks pairs of states as distinguishable, and whatever remains unmarked at the end is equivalent.

Step 1 — Base case. For every pair of states (p, q), if exactly one of them is a final state, mark the pair as distinguishable. This is because the empty string ε already tells them apart: one reaches a final state and the other does not.

Step 2 — Inductive step (propagation). Repeat the following until no new pair gets marked in a full pass: For every still-unmarked pair (p, q) and every symbol a in the alphabet, look at where each state goes: δ(p, a) and δ(q, a). If the resulting pair (δ(p, a), δ(q, a)) is already marked as distinguishable, then (p, q) must also be marked as distinguishable. Intuitively, this means: reading a and then a string that distinguishes the two destination states is itself a string that distinguishes p from q.

This step is repeated to a fixed point — that is, until an entire pass over all pairs produces no new marks — because marking a new pair in one round can enable marking additional pairs in the next round.

Step 3 — Result. Once the fixed point is reached, every pair (p, q) that was never marked is equivalent: no string of any length can distinguish them, since if one existed, the propagation step would eventually have marked the pair.

Complexity. For a DFA with n states and an alphabet of size k, the algorithm considers O(n²) pairs, and the propagation loop revisits all pairs and all symbols until convergence, giving a worst-case time complexity of O(n² · k) (in the straightforward implementation used here, without additional optimizations such as the linked-list based partition refinement).

Implementation Notes
Input is read line by line: number of cases, then for each case the number of states, the alphabet, the final states, and one line per state containing the state's id followed by its transitions (in the same order as the alphabet).
Equivalence is represented with a boolean matrix marcados[p][q] (for p < q), where True means the pair is known to be distinguishable.
The output only prints pairs (p, q) with p < q that remain unmarked after the algorithm converges, sorted in lexicographical order (guaranteed naturally by iterating p and q in increasing order).
