# Quantum Tech — Coverage Guide

This README is an outline/checklist for what the Quantum Tech section should cover as it grows.

## Scope

- Quantum computing (near-term + fault-tolerant roadmaps)
- Quantum networking / communications
- Quantum sensing / metrology
- Practical engineering: control systems, error budgets, benchmarking, deployment, and “what’s real vs hype”

## What this section should cover

### 1) Fundamentals (reader should internalize)

- Qubits and quantum states (Bloch sphere intuition)
- Measurement, collapse, and why quantum is probabilistic
- Entanglement and non-classical correlations
- Noise models (decoherence, T1/T2, depolarizing, readout error)
- Circuit model vs analog/continuous-time approaches

### 2) Hardware modalities (how QPUs differ)

- Superconducting qubits (control, cryogenics, scaling constraints)
- Trapped ions (gates, connectivity, speed trade-offs)
- Neutral atoms (Rydberg gates, arrays, scaling)
- Photonics (sources, interferometers, error models)
- Spin/semiconductor qubits (CMOS adjacency, challenges)
- Comparative table: connectivity, fidelities, gate times, operating environment, scaling bottlenecks

### 3) Quantum software stack (from circuits to pulses)

- Circuit representation and compilation (routing, transpilation, optimization)
- Control stack basics (pulse-level control, calibration loops)
- Simulation (statevector vs tensor network vs stabilizer; limits)
- SDKs and ecosystems (Qiskit, Cirq, PennyLane, etc.) and how to choose
- Cloud QPU access patterns; job queues; hybrid workflows

### 4) Algorithms and workloads (what’s “useful work”?)

- Canonical algorithms: Shor, Grover (what they do and when they matter)
- NISQ-era variational algorithms: VQE, QAOA (pros/cons, failure modes)
- Quantum simulation (chemistry/materials) and where it is credible
- Hybrid workflows (classical optimizer loops; data movement constraints)
- Quantum ML: what is actually promising vs mostly marketing

### 5) Error correction and fault tolerance (road to scale)

- Why logical qubits are expensive; surface code intuition
- Thresholds, code distance, syndrome extraction
- Resource estimation: physical → logical qubits, time-to-solution
- Magic state distillation (high-level role) and cost drivers
- How to read FTQC roadmaps critically

### 6) Benchmarking and evaluation (avoid bad metrics)

- Fidelity/infidelity: single- and two-qubit gate, readout
- Noise characterization: RB/XEB, tomography (limits), drift
- Higher-level metrics: quantum volume, CLOPS, algorithmic qubits, utility metrics
- “Advantage” framing: speedup vs cost vs accuracy vs energy

### 7) Quantum networking and cryptography

- QKD: what it provides, what it doesn’t
- Entanglement distribution and repeaters (high-level architecture)
- Post-quantum cryptography (PQC): migration priorities and timelines
- Threat modeling: “harvest now, decrypt later” and data retention

### 8) Sensing and metrology (often nearer-term than computing)

- Quantum clocks and timing
- Magnetometry / gravimetry use cases (navigation, geology)
- Imaging/sensing trade-offs (precision, bandwidth, environmental constraints)

### 9) Productization and adoption (how teams should think)

- Identify workloads where quantum could plausibly help (and where it can’t)
- Build decision trees: “simulate classically first”, “error budgets”, “data movement”
- Vendor evaluation checklist and red flags
- Governance and security considerations (key management, PQC readiness)

## Suggested structure (planned)

- `fundamentals/` — core mental models + glossary
- `hardware/` — modality deep dives and comparisons
- `algorithms/` — algorithm notes, toy examples, resource estimates
- `error-correction/` — FTQC concepts and estimators
- `networking/` — QKD, repeaters, architectures
- `sensing/` — applied sensing and metrology
- `benchmarks/` — metrics, how to compare claims
- `security/` — PQC migration and quantum threat models

## First pages to write (recommended)

- Fundamentals overview + glossary
- “How to read quantum vendor claims” (metrics + red flags)
- PQC migration checklist for practitioners

