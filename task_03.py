import timeit
from typing import Callable


# KNUTH-MORRIS-PRATT ALGORITHM 
def compute_lps(pattern):
    """Compute LPS (Longest Proper Prefix which is also Suffix) array for KMP"""
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

    i = 0  # index for text
    j = 0  # index for pattern

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            return i - j  # Found! Return position
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1  # Not found


# BOYER-MOORE ALGORITHM
def build_bad_char_table(pattern):
    """Build bad character table"""
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

        # Compare from right to left
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return shift  # Found!
        else:
            # Calculate shift
            bad_char_shift = bad_char.get(text[shift + j], m)
            shift += max(1, bad_char_shift)

    return -1  # Not found


# RABIN-KARP ALGORITHM
def rabin_karp_search(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)

    if m > n:
        return -1

    # Calculate d^(m-1) % q
    h = pow(d, m - 1, q)

    # Calculate hash of pattern and first window
    hash_pattern = 0
    hash_window = 0

    for i in range(m):
        hash_pattern = (d * hash_pattern + ord(pattern[i])) % q
        hash_window = (d * hash_window + ord(text[i])) % q

    # Slide window over text
    for i in range(n - m + 1):
        # If hashes match - verify character by character
        if hash_pattern == hash_window:
            # Check for collision
            if text[i:i+m] == pattern:
                return i  # Found!

        # Recalculate hash for next window
        if i < n - m:
            hash_window = (d * (hash_window - ord(text[i]) * h) + ord(text[i + m])) % q

            if hash_window < 0:
                hash_window += q

    return -1  # Not found


# Measure algorithm execution time
def benchmark_algorithm(func: Callable, text: str, pattern: str, number: int = 100) -> float:
    timer = timeit.Timer(lambda: func(text, pattern))
    time = timer.timeit(number=number)
    return time


# Main function to compare algorithms
def main():
    # Read files
    print("Reading files...")

    with open('article_1.txt', 'r', encoding='utf-8') as f:
        text1 = f.read()

    with open('article_2.txt', 'r', encoding='utf-8') as f:
        text2 = f.read()

    print(f"Article 1: {len(text1)} characters")
    print(f"Article 2: {len(text2)} characters")
    print()

    # Choose substrings for search
    # Existing substrings (present in articles)
    pattern1_exists = "алгоритм"  # exists in article 1
    pattern2_exists = "рекомендаційної системи"  # exists in article 2

    # Non-existing substrings
    pattern1_fake = "неіснуючий патерн xyz"
    pattern2_fake = "фантастичний алгоритм 123"
    

    # Test on article 1
    print("ARTICLE 1")
    print("-" * 80)

    # Existing substring
    print(f"\nSearching for existing substring: '{pattern1_exists}'")

    # Verify all algorithms find the substring
    kmp_pos = kmp_search(text1, pattern1_exists)
    bm_pos = boyer_moore_search(text1, pattern1_exists)
    rk_pos = rabin_karp_search(text1, pattern1_exists)

    print(f"   KMP found at position: {kmp_pos}")
    print(f"   Boyer-Moore found at position: {bm_pos}")
    print(f"   Rabin-Karp found at position: {rk_pos}")
    print()

    # Measure time
    time_kmp = benchmark_algorithm(kmp_search, text1, pattern1_exists)
    time_bm = benchmark_algorithm(boyer_moore_search, text1, pattern1_exists)
    time_rk = benchmark_algorithm(rabin_karp_search, text1, pattern1_exists)

    print(f"   KMP:         {time_kmp:.6f} sec")
    print(f"   Boyer-Moore: {time_bm:.6f} sec")
    print(f"   Rabin-Karp:  {time_rk:.6f} sec")

    # Determine the winner
    times_1_exists = {'KMP': time_kmp, 'Boyer-Moore': time_bm, 'Rabin-Karp': time_rk}
    fastest_1_exists = min(times_1_exists, key=times_1_exists.get)
    print(f"\n   Fastest: {fastest_1_exists} ({times_1_exists[fastest_1_exists]:.6f} sec)")

    # Non-existing substring
    print(f"\nSearching for NON-existing substring: '{pattern1_fake}'")

    time_kmp_fake = benchmark_algorithm(kmp_search, text1, pattern1_fake)
    time_bm_fake = benchmark_algorithm(boyer_moore_search, text1, pattern1_fake)
    time_rk_fake = benchmark_algorithm(rabin_karp_search, text1, pattern1_fake)

    print(f"   KMP:         {time_kmp_fake:.6f} sec")
    print(f"   Boyer-Moore: {time_bm_fake:.6f} sec")
    print(f"   Rabin-Karp:  {time_rk_fake:.6f} sec")

    times_1_fake = {'KMP': time_kmp_fake, 'Boyer-Moore': time_bm_fake, 'Rabin-Karp': time_rk_fake}
    fastest_1_fake = min(times_1_fake, key=times_1_fake.get)
    print(f"\n   Fastest: {fastest_1_fake} ({times_1_fake[fastest_1_fake]:.6f} sec)")

    print("\n" + "=" * 80)

    # Test on article 2
    print("\nARTICLE 2")
    print("-" * 80)

    # Existing substring
    print(f"\nSearching for existing substring: '{pattern2_exists}'")

    kmp_pos2 = kmp_search(text2, pattern2_exists)
    bm_pos2 = boyer_moore_search(text2, pattern2_exists)
    rk_pos2 = rabin_karp_search(text2, pattern2_exists)

    print(f"   KMP found at position: {kmp_pos2}")
    print(f"   Boyer-Moore found at position: {bm_pos2}")
    print(f"   Rabin-Karp found at position: {rk_pos2}")
    print()

    time_kmp2 = benchmark_algorithm(kmp_search, text2, pattern2_exists)
    time_bm2 = benchmark_algorithm(boyer_moore_search, text2, pattern2_exists)
    time_rk2 = benchmark_algorithm(rabin_karp_search, text2, pattern2_exists)

    print(f"   KMP:         {time_kmp2:.6f} sec")
    print(f"   Boyer-Moore: {time_bm2:.6f} sec")
    print(f"   Rabin-Karp:  {time_rk2:.6f} sec")

    times_2_exists = {'KMP': time_kmp2, 'Boyer-Moore': time_bm2, 'Rabin-Karp': time_rk2}
    fastest_2_exists = min(times_2_exists, key=times_2_exists.get)
    print(f"\n   Fastest: {fastest_2_exists} ({times_2_exists[fastest_2_exists]:.6f} sec)")

    # Non-existing substring
    print(f"\nSearching for NON-existing substring: '{pattern2_fake}'")

    time_kmp2_fake = benchmark_algorithm(kmp_search, text2, pattern2_fake)
    time_bm2_fake = benchmark_algorithm(boyer_moore_search, text2, pattern2_fake)
    time_rk2_fake = benchmark_algorithm(rabin_karp_search, text2, pattern2_fake)

    print(f"   KMP:         {time_kmp2_fake:.6f} sec")
    print(f"   Boyer-Moore: {time_bm2_fake:.6f} sec")
    print(f"   Rabin-Karp:  {time_rk2_fake:.6f} sec")

    times_2_fake = {'KMP': time_kmp2_fake, 'Boyer-Moore': time_bm2_fake, 'Rabin-Karp': time_rk2_fake}
    fastest_2_fake = min(times_2_fake, key=times_2_fake.get)
    print(f"\n   Fastest: {fastest_2_fake} ({times_2_fake[fastest_2_fake]:.6f} sec)")

    print("\n" + "=" * 80)

    # OVERALL CONCLUSIONS
    print("\nOVERALL CONCLUSIONS")
    print("=" * 80)

    # Total time across all tests
    total_kmp = time_kmp + time_kmp_fake + time_kmp2 + time_kmp2_fake
    total_bm = time_bm + time_bm_fake + time_bm2 + time_bm2_fake
    total_rk = time_rk + time_rk_fake + time_rk2 + time_rk2_fake

    print("\nTotal time across all tests:")
    print(f"   KMP:         {total_kmp:.6f} sec")
    print(f"   Boyer-Moore: {total_bm:.6f} sec")
    print(f"   Rabin-Karp:  {total_rk:.6f} sec")

    total_times = {'KMP': total_kmp, 'Boyer-Moore': total_bm, 'Rabin-Karp': total_rk}
    overall_fastest = min(total_times, key=total_times.get)

    print(f"\nOVERALL FASTEST: {overall_fastest}")
    print(f"   Time: {total_times[overall_fastest]:.6f} sec")

    # Relative speed
    print("\nRelative speed (compared to KMP):")
    for algo, time in total_times.items():
        relative = (time / total_kmp) * 100
        print(f"   {algo}: {relative:.1f}%")

    print("\n" + "=" * 80)

    # Analysis by search type
    print("\nANALYSIS BY SEARCH TYPE")
    print("=" * 80)

    print("\n1. Existing substrings:")
    avg_kmp_exists = (time_kmp + time_kmp2) / 2
    avg_bm_exists = (time_bm + time_bm2) / 2
    avg_rk_exists = (time_rk + time_rk2) / 2

    print(f"   KMP:         {avg_kmp_exists:.6f} sec (average)")
    print(f"   Boyer-Moore: {avg_bm_exists:.6f} sec (average)")
    print(f"   Rabin-Karp:  {avg_rk_exists:.6f} sec (average)")

    exists_times = {'KMP': avg_kmp_exists, 'Boyer-Moore': avg_bm_exists, 'Rabin-Karp': avg_rk_exists}
    fastest_exists = min(exists_times, key=exists_times.get)
    print(f"   Best: {fastest_exists}")

    print("\n2. Non-existing substrings:")
    avg_kmp_fake = (time_kmp_fake + time_kmp2_fake) / 2
    avg_bm_fake = (time_bm_fake + time_bm2_fake) / 2
    avg_rk_fake = (time_rk_fake + time_rk2_fake) / 2

    print(f"   KMP:         {avg_kmp_fake:.6f} sec (average)")
    print(f"   Boyer-Moore: {avg_bm_fake:.6f} sec (average)")
    print(f"   Rabin-Karp:  {avg_rk_fake:.6f} sec (average)")

    fake_times = {'KMP': avg_kmp_fake, 'Boyer-Moore': avg_bm_fake, 'Rabin-Karp': avg_rk_fake}
    fastest_fake = min(fake_times, key=fake_times.get)
    print(f"   Best: {fastest_fake}")


if __name__ == "__main__":
    main()