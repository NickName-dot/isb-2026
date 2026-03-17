import math
import os
from datetime import datetime

def erfc_approx(x):
    """NIST SP 800-22 точное приближение erfc(x)."""
    if x < 0: 
        return 2.0 - erfc_approx(-x)
    t = 1.0 / (1.0 + 0.5 * x)
    tau = t * math.exp(-x*x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * 
             (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + 
             t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))))
    return tau

def monobit_test(bits: str) -> float:
    """Частотный тест NIST SP 800-22."""
    n = len(bits)
    if n == 0:
        return 0.0
    ones = bits.count('1')
    zero = n - ones
    s = abs(ones - zero) / math.sqrt(n)
    p = erfc_approx(s / math.sqrt(2))
    return round(p, 4)

def runs_test(bits):
    """Тест на серии NIST SP 800-22. Проверяет независимость битов."""
    n = len(bits)
    V_N = sum(1 for i in range(1, n) if bits[i] != bits[i-1])
    V_N = V_N + 1
    ones = bits.count('1')
    zeta = ones / n
    if abs(zeta - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    numerator = abs(V_N - 2 * n * zeta * (1 - zeta))
    denominator = 2 * math.sqrt(2 * n) * zeta * (1 - zeta)
    if denominator == 0:
        return 0.0
    argument = numerator / denominator
    p = erfc_approx(argument / math.sqrt(2))
    return round(p, 4)

def longest_run_ones_test(bits):
    n = len(bits)
    M = 8
    N_blocks = n // M
    
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    v = [0, 0, 0, 0]
    
    for i in range(N_blocks):
        block = bits[i*M:(i+1)*M]
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        elif max_run >= 4:
            v[3] += 1
    
    chi_square = 0
    for i in range(4):
        expected = N_blocks * pi[i]
        chi_square += ((v[i] - expected) ** 2) / expected
    
    p = erfc_approx(math.sqrt(chi_square / 2))
    return round(p, 4)


def read_bits(filename):
    """Чтение битовой последовательности из файла."""
    if not os.path.exists(filename):
        return False, ""
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            bits = ''.join(c for c in content if c in '01')
        return True, bits
    except:
        return False, ""

if __name__ == "__main__":
    generator_files = [
        ("C", "c_gen_128.txt"),
        ("C++", "c++_gen_128.txt"),
        ("Java", "java_gen_128.txt")
    ]
    
    filename = f"NIST_ALL_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("NIST SP 800-22 REV 1-a STATISTICAL TEST RESULTS\n")
        f.write("=" * 60 + "\n\n")
        
        results = {}
        for gen_name, bit_file in generator_files:
            success, bits = read_bits(bit_file)
            if success and len(bits) >= 100:
                results[gen_name] = {
                    'monobit': monobit_test(bits),
                    'runs': runs_test(bits),
                    'longest_run_ones': longest_run_ones_test(bits)
                }
                
                p_monobit = results[gen_name]['monobit']
                p_runs = results[gen_name]['runs']
                p_longest = results[gen_name]['longest_run_ones']
                total_passed = sum(1 for p in [p_monobit, p_runs, p_longest] if p > 0.01)
                
                f.write(f"GENERATOR: {gen_name}\n")
                f.write(f"File: {bit_file} ({len(bits)} bits)\n")
                f.write("-" * 40 + "\n")
                f.write(f"Monobit Test          : p={p_monobit:7.4f} {'PASS' if p_monobit > 0.01 else 'FAIL'}\n")
                f.write(f"Runs Test             : p={p_runs:7.4f} {'PASS' if p_runs > 0.01 else 'FAIL'}\n")
                f.write(f"Longest Run of Ones   : p={p_longest:7.4f} {'PASS' if p_longest > 0.01 else 'FAIL'}\n")
                f.write(f"PASSED: {total_passed}/3 tests\n\n")
            else:
                f.write(f"{gen_name}: ERROR - insufficient bits\n\n")
        
        if results:
            f.write("FINAL RESULTS TABLE:\n")
            f.write("┌" + "─"*24 + "┬" + "─"*9 + "┬" + "─"*9 + "┬" + "─"*9 + "┐\n")
            f.write("│ Test                 │   C    │  C++   │ Java  │\n")
            f.write("├" + "─"*24 + "┼" + "─"*9 + "┼" + "─"*9 + "┼" + "─"*9 + "┤\n")
            
            tests = ['monobit', 'runs', 'longest_run_ones']
            for test in tests:
                c_val = results.get('C', {}).get(test, 0)
                cpp_val = results.get('C++', {}).get(test, 0)
                java_val = results.get('Java', {}).get(test, 0)
                f.write(f"│ {test:<21} │{c_val:8.4f}│{cpp_val:8.4f}│{java_val:8.4f}│\n")
            
            f.write("└" + "─"*24 + "┴" + "─"*9 + "┴" + "─"*9 + "┴" + "─"*9 + "┘\n")
    
    print(f"NIST report generated: {filename}")
