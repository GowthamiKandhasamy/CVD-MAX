# CVD-MAX
CVD-MAX is an automated vulnerability detection system for C/C++ programs.
It combines static analysis, dynamic analysis, and deep learning to detect
vulnerabilities and predict CWE categories.

## Branches
- main -> Stable branch
- dev -> integration
- ingestion (for eg) -> Gowthami's branch
- cfg (for eg) -> Gaby's branch

### Note: 
Please work on your own branches and commit it to dev first. Only after discussion, shall we ever commit to the main branch. And update your commits to dev/main in the group.

## Project Structure

```text
CVD-MAX/
│
├── data/          # All datasets (raw code, fuzz inputs, traces, processed data)
├── demo/          # Demo scripts for panel / end-to-end runs
├── docker/        # Dockerfiles and container configurations
├── docs/          # Documentation (methodology, architecture, explanations, base papers, presentations)
├── experiments/   # Local experiments, tests, LLVM IR, CFGs
├── src/           # Core implementation code (pipeline, analysis, models)
│
├── README.md      
├── requirements.txt
├── LICENSE
└── .gitignore

## Input
- C/C++ source code or firmware

## Output
- Vulnerability present: Yes / No
- CWE category (if vulnerable)

## Pipeline
1. Code ingestion
2. Coverage-guided fuzzing (libFuzzer)
3. Sanitizer instrumentation
4. LLVM IR & CFG extraction
5. Static analysis with GAT
6. Dynamic analysis with runtime tracing
7. Static–Dynamic fusion via attention
8. Classification

## Demo
```bash
bash demo/run_demo.sh samples/vulnerable.c
