# An Engineer’s Guide to GEMM (Pete Warden, Oct 25, 2015) — Notes

This note distills key engineering takeaways from Pete Warden’s blog post **“An Engineer’s Guide to GEMM”**.

The post focuses less on GEMM optimization and more on **common correctness traps** engineers hit when implementing or integrating GEMM (especially around memory layout, transposes, argument order, and leading dimensions).

## Key Concepts (Distilled)

### Row-major vs column-major storage

Two common ways to lay out a matrix in memory:

- **Row-major**: contiguous memory walks left→right across each row.
- **Column-major**: contiguous memory walks top→bottom down each column.

The post emphasizes: these are storage conventions for the same underlying math, but you must match the convention expected by the library you call.

### Transpose as the “symptom” of a layout mismatch

If you pass a row-major matrix to a column-major API (or vice versa), a square matrix will often be interpreted as its **transpose**.

### Matrix multiplication order matters

Unlike scalar multiplication, `A * B` is not generally equal to `B * A`.

The post highlights a common identity:

- If `C = A * B`, then `C' = B' * A'`.

### “#Errors % 2 == 0” (cancellation traps)

Storage order, transposes, and argument ordering can **mask each other’s bugs**: two mistakes may cancel out and produce “working” but confusing code that later breaks under change.

### Leading dimensions (`lda`, `ldb`, `ldc`)

The post frames leading dimensions as **strides**: how far you move in memory when stepping to the next row/column (depending on storage convention). They enable working on sub-tiles inside larger matrices.

## Practical Debugging Advice (Distilled)

- Work through small examples with pen-and-paper until the conventions are unambiguous.
- Turn those examples into **unit tests** using hand-calculated expected results.
- Keep a simple **reference GEMM implementation** (unoptimized but readable) that you can step through and compare against optimized kernels.

## Appendix: Raw Notes (Preserved)

- “Row versus Column Major” (storage order conventions and why they matter).
- “Transpose” (layout mismatch often looks like a transpose).
- “Argument Ordering” (matrix multiply order matters; `C' = B' * A'`).
- “#Errors % 2 == 0” (storage order, transpose, and argument order can cancel).
- “Leading Dimensions” (`lda/ldb/ldc` as strides for tiles/submatrices).
- Debugging: pen-and-paper → unit tests; keep a simple reference GEMM.
