# Substring Search Algorithm Comparison

## Overview

This project compares the efficiency of three classic substring search algorithms:
- **Knuth-Morris-Pratt (KMP)**
- **Boyer-Moore**
- **Rabin-Karp**

The algorithms are tested on two Ukrainian text articles, searching for both existing and non-existing substrings.

## Test Data

- **Article 1**: 12,655 characters - about algorithms in programming language libraries
- **Article 2**: 17,590 characters - about data structures for recommendation systems

### Search Patterns

| Pattern Type | Article 1 | Article 2 |
|-------------|-----------|-----------|
| Existing | "алгоритм" | "рекомендаційної системи" |
| Non-existing | "неіснуючий патерн xyz" | "фантастичний алгоритм 123" |

## Results

### Article 1 Results

#### Existing substring ("алгоритм")
| Algorithm | Time (sec) | Position Found |
|-----------|------------|----------------|
| KMP | 0.002871 | 206 |
| Boyer-Moore | 0.000619 | 206 |
| Rabin-Karp | 0.002979 | 206 |

**Fastest: Boyer-Moore**

#### Non-existing substring
| Algorithm | Time (sec) |
|-----------|------------|
| KMP | 0.131125 |
| Boyer-Moore | 0.012026 |
| Rabin-Karp | 0.155716 |

**Fastest: Boyer-Moore**

---

### Article 2 Results

#### Existing substring ("рекомендаційної системи")
| Algorithm | Time (sec) | Position Found |
|-----------|------------|----------------|
| KMP | 0.000951 | 52 |
| Boyer-Moore | 0.000279 | 52 |
| Rabin-Karp | 0.000904 | 52 |

**Fastest: Boyer-Moore**

#### Non-existing substring
| Algorithm | Time (sec) |
|-----------|------------|
| KMP | 0.190678 |
| Boyer-Moore | 0.015196 |
| Rabin-Karp | 0.228747 |

**Fastest: Boyer-Moore**

---

## Overall Conclusions

### Total Time Across All Tests

| Algorithm | Total Time (sec) | Relative Speed (vs KMP) |
|-----------|------------------|------------------------|
| KMP | 0.325625 | 100.0% |
| Boyer-Moore | 0.028120 | 8.6% |
| Rabin-Karp | 0.388346 | 119.3% |

### Winner by Category

| Category | Fastest Algorithm |
|----------|-------------------|
| Article 1 - Existing | Boyer-Moore |
| Article 1 - Non-existing | Boyer-Moore |
| Article 2 - Existing | Boyer-Moore |
| Article 2 - Non-existing | Boyer-Moore |
| **Overall Winner** | **Boyer-Moore** |

### Analysis by Search Type

#### Existing Substrings (Average)
| Algorithm | Avg Time (sec) |
|-----------|----------------|
| KMP | 0.001911 |
| Boyer-Moore | 0.000449 |
| Rabin-Karp | 0.001941 |

**Best: Boyer-Moore**

#### Non-existing Substrings (Average)
| Algorithm | Avg Time (sec) |
|-----------|----------------|
| KMP | 0.160902 |
| Boyer-Moore | 0.013611 |
| Rabin-Karp | 0.192232 |

**Best: Boyer-Moore**

---

## Key Findings

1. **Boyer-Moore is the clear winner** in all test scenarios, being approximately **11x faster** than KMP overall.

2. **Performance on non-existing substrings**: Boyer-Moore shows the biggest advantage when searching for patterns that don't exist in the text. This is due to its ability to skip large portions of text using the bad character heuristic.

3. **Rabin-Karp performed the slowest** in these tests, even slightly slower than KMP. This is because:
   - The hash calculation overhead doesn't pay off for single pattern search
   - Rabin-Karp is more efficient for multiple pattern search scenarios

4. **Why Boyer-Moore excels**:
   - Compares from right to left, allowing larger jumps
   - The bad character table enables skipping many characters at once
   - Works especially well with longer patterns and larger alphabets

## Files

- `task_03.py` - Main comparison script with all three algorithm implementations
- `article_1.txt` - First test article (Ukrainian)
- `article_2.txt` - Second test article (Ukrainian)
- `README.md` - This file
