import timeit
from typing import Callable


# KNUTH-MORRIS-PRATT ALGORITHM 
def compute_lps(pattern):
    M = len(pattern)
    lps = [0] * M
    length = 0
    i = 1

    while i < M:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    N = len(text)
    M = len(pattern)
    lps = compute_lps(pattern)
    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == M:
            return i - j
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# BOYER-MOORE ALGORITHM
def build_bad_char_table(pattern):
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table


def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    bad_char = build_bad_char_table(pattern)
    shift = 0

    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift
        else:
            bad_char_shift = bad_char.get(text[shift + j], m)
            shift += max(1, bad_char_shift)
    return -1


# RABIN-KARP ALGORITHM
def rabin_karp_search(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    h = pow(d, m - 1, q)
    hash_pattern = 0
    hash_window = 0

    for i in range(m):
        hash_pattern = (d * hash_pattern + ord(pattern[i])) % q
        hash_window = (d * hash_window + ord(text[i])) % q

    for i in range(n - m + 1):
        if hash_pattern == hash_window:
            if text[i:i+m] == pattern:
                return i

        if i < n - m:
            hash_window = (d * (hash_window - ord(text[i]) * h) + ord(text[i + m])) % q
            if hash_window < 0:
                hash_window += q
    return -1


def benchmark_algorithm(func: Callable, text: str, pattern: str, number: int = 100) -> float:
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=number)


def test_article(text, pattern_exists, pattern_fake, article_name):
    """Test both patterns on one article"""
    print(f"\n{'='*60}")
    print(f"{article_name}")
    print('='*60)
    
    results = {}
    
    # Test existing pattern
    print(f"\n1. Існуючий підрядок: '{pattern_exists}'")
    for name, func in [('KMP', kmp_search), ('Boyer-Moore', boyer_moore_search), ('Rabin-Karp', rabin_karp_search)]:
        time = benchmark_algorithm(func, text, pattern_exists)
        results[f'{name}_exists'] = time
        print(f"   {name:12} {time:.6f} сек")
    
    fastest_exists = min([('KMP', results['KMP_exists']), 
                          ('Boyer-Moore', results['Boyer-Moore_exists']), 
                          ('Rabin-Karp', results['Rabin-Karp_exists'])], 
                         key=lambda x: x[1])
    print(f"   → Найшвидший: {fastest_exists[0]}")
    
    # Test fake pattern
    print(f"\n2. Вигаданий підрядок: '{pattern_fake}'")
    for name, func in [('KMP', kmp_search), ('Boyer-Moore', boyer_moore_search), ('Rabin-Karp', rabin_karp_search)]:
        time = benchmark_algorithm(func, text, pattern_fake)
        results[f'{name}_fake'] = time
        print(f"   {name:12} {time:.6f} сек")
    
    fastest_fake = min([('KMP', results['KMP_fake']), 
                        ('Boyer-Moore', results['Boyer-Moore_fake']), 
                        ('Rabin-Karp', results['Rabin-Karp_fake'])], 
                       key=lambda x: x[1])
    print(f"   → Найшвидший: {fastest_fake[0]}")
    
    return results


def main():
    # Read files
    with open('article_1.txt', 'r', encoding='utf-8') as f:
        text1 = f.read()
    with open('article_2.txt', 'r', encoding='utf-8') as f:
        text2 = f.read()

    print(f"Стаття 1: {len(text1)} символів")
    print(f"Стаття 2: {len(text2)} символів")

    # Test patterns
    results1 = test_article(text1, "алгоритм", "неіснуючий патерн xyz", "СТАТТЯ 1")
    results2 = test_article(text2, "рекомендаційної системи", "фантастичний алгоритм 123", "СТАТТЯ 2")

    # Calculate totals
    total_kmp = results1['KMP_exists'] + results1['KMP_fake'] + results2['KMP_exists'] + results2['KMP_fake']
    total_bm = results1['Boyer-Moore_exists'] + results1['Boyer-Moore_fake'] + results2['Boyer-Moore_exists'] + results2['Boyer-Moore_fake']
    total_rk = results1['Rabin-Karp_exists'] + results1['Rabin-Karp_fake'] + results2['Rabin-Karp_exists'] + results2['Rabin-Karp_fake']

    totals = {'KMP': total_kmp, 'Boyer-Moore': total_bm, 'Rabin-Karp': total_rk}
    fastest_overall = min(totals, key=totals.get)

    # Print overall results
    print(f"\n{'='*60}")
    print("ЗАГАЛЬНІ РЕЗУЛЬТАТИ")
    print('='*60)
    print(f"\nЗагальний час:")
    for name, time in totals.items():
        print(f"   {name:12} {time:.6f} сек")
    print(f"\n→ Найшвидший в цілому: {fastest_overall}")

    # Generate markdown report
    report = f"""# Порівняння алгоритмів пошуку підрядка

## Стаття 1

### Існуючий підрядок "алгоритм"
| Алгоритм | Час виконання |
|----------|---------------|
| KMP | {results1['KMP_exists']:.6f} сек |
| Boyer-Moore | {results1['Boyer-Moore_exists']:.6f} сек |
| Rabin-Karp | {results1['Rabin-Karp_exists']:.6f} сек |

### Вигаданий підрядок
| Алгоритм | Час виконання |
|----------|---------------|
| KMP | {results1['KMP_fake']:.6f} сек |
| Boyer-Moore | {results1['Boyer-Moore_fake']:.6f} сек |
| Rabin-Karp | {results1['Rabin-Karp_fake']:.6f} сек |

---

## Стаття 2

### Існуючий підрядок "рекомендаційної системи"
| Алгоритм | Час виконання |
|----------|---------------|
| KMP | {results2['KMP_exists']:.6f} сек |
| Boyer-Moore | {results2['Boyer-Moore_exists']:.6f} сек |
| Rabin-Karp | {results2['Rabin-Karp_exists']:.6f} сек |

### Вигаданий підрядок
| Алгоритм | Час виконання |
|----------|---------------|
| KMP | {results2['KMP_fake']:.6f} сек |
| Boyer-Moore | {results2['Boyer-Moore_fake']:.6f} сек |
| Rabin-Karp | {results2['Rabin-Karp_fake']:.6f} сек |

---

## Загальні результати

| Алгоритм | Загальний час |
|----------|---------------|
| KMP | {total_kmp:.6f} сек |
| Boyer-Moore | {total_bm:.6f} сек |
| Rabin-Karp | {total_rk:.6f} сек |

## Висновки

**Найшвидший алгоритм в цілому: {fastest_overall}**

Алгоритм {fastest_overall} показав найкращі результати як для окремих текстів, 
так і в загальному підсумку. Він ефективно працює як з існуючими, так і з 
вигаданими підрядками.
"""

    with open('ВИСНОВКИ.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n✓ Результати збережено у файл ВИСНОВКИ.md")


if __name__ == "__main__":
    main()