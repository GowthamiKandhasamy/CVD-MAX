# CVD-MAX
CVD-MAX is an automated vulnerability detection system for C/C++ programs.
It combines static analysis, dynamic analysis, and deep learning to detect
vulnerabilities and predict CWE categories.

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
