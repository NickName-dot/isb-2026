import math
import re
from datetime import datetime

def erfc(x):
    if x == 0:
        return 1.0
    t = 1.0 / (1.0 + 0.5 * x)
    tau = t * math.exp(-x*x - 1.26551223 + t * (1.00002368 + t * (0.3740916 + t * 
           (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398)))))))
    return tau / math.sqrt(math.pi)

def nist_tests(filename, report_file):
    
    try:
        with open(filename, 'r') as f:
            numbers = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"ОШИБКА: Файл {filename} не найден")
        return False
    
    bits = ''.join(str((num >> 63) & 1) for num in numbers)
    n = len(bits)
    
    ones = bits.count('1')
    s = abs(ones - n/2) * 2 / math.sqrt(n)
    p_monobit = erfc(s / math.sqrt(2))
    
    runs = 1 + sum(1 for i in range(1, n) if bits[i] != bits[i-1])
    z = abs(2*runs - n - 1) / math.sqrt(2*n + 1)
    p_runs = erfc(z / math.sqrt(2))
    
    max_run = max((len(match.group()) for match in re.finditer(r'1+', bits)), default=0)
    if max_run == 0:
        p_longest = 1.0
    else:
        p_longest = (n - max_run + 3) / (2**(n - max_run + 3))
    
    with open(report_file, 'a', encoding='utf-8') as rf:
        rf.write(f"\n{'='*80}\n")
        rf.write(f"ОТЧЕТ NIST STS ТЕСТОВ\n")
        rf.write(f"Файл: {filename}\n")
        rf.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        rf.write(f"Количество чисел: {len(numbers)}\n")
        rf.write(f"Количество бит: {n}\n")
        rf.write(f"{'='*80}\n\n")
        
        status_monobit = "ПРОЙДЕН" if p_monobit >= 0.01 else "ПРОВАЛЕН"
        rf.write(f"1. MONOBIT ТЕСТ (частотный)\n")
        rf.write(f"   Количество единиц: {ones}/{n} ({ones/n*100:.2f}%)\n")
        rf.write(f"   Статистика: {s:.6f}\n")
        rf.write(f"   p-value: {p_monobit:.10f}\n")
        rf.write(f"   Результат: {status_monobit}\n\n")
        
        status_runs = "ПРОЙДЕН" if p_runs >= 0.01 else "ПРОВАЛЕН"
        rf.write(f"2. RUNS ТЕСТ (тест серий)\n")
        rf.write(f"   Количество серий: {runs}\n")
        rf.write(f"   Статистика: {z:.6f}\n")
        rf.write(f"   p-value: {p_runs:.10f}\n")
        rf.write(f"   Результат: {status_runs}\n\n")
        
        status_longest = "ПРОЙДЕН" if p_longest >= 0.01 else "ПРОВАЛЕН"
        rf.write(f"3. LONGEST RUN OF ONES ТЕСТ\n")
        rf.write(f"   Максимальная серия единиц: {max_run}\n")
        rf.write(f"   p-value: {p_longest:.10f}\n")
        rf.write(f"   Результат: {status_longest}\n\n")
        
        passed = sum([p_monobit >= 0.01, p_runs >= 0.01, p_longest >= 0.01])
        total_status = "ПРОЙДЕН" if passed == 3 else f"ПРОВАЛЕН ({passed}/3)"
        rf.write(f"ИТОГОВЫЙ РЕЗУЛЬТАТ: {total_status}\n")
        rf.write(f"{'='*80}\n")
    
    print(f"{filename}: {passed}/3 тестов ПРОЙДЕНО")
    return passed == 3

if __name__ == "__main__":
    test_files = ['C_gen_1000.txt', 'C++_gen_1000.txt', 'java_gen_1000.txt']
    report_filename = f"NIST_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("ЛАБОРАТОРНАЯ РАБОТА №2: ПРОВЕРОКА КАЧЕСТВА ГПСЧ\n")
        f.write("Тесты NIST STS (Statistical Test Suite)\n")
        f.write("="*80 + "\n\n")
    
    print(f"Создан отчет: {report_filename}")
    all_passed = True
    
    for filename in test_files:
        if not nist_tests(filename, report_filename):
            all_passed = False
    
    with open(report_filename, 'a', encoding='utf-8') as f:
        f.write(f"\nФИНАЛЬНЫЙ ИТОГ:\n")
        status = "ВСЕ ГЕНЕРАТОРЫ КАЧЕСТВЕННЫЕ" if all_passed else "ОБНАРУЖЕНЫ ПРОБЛЕМЫ"
        f.write(f"{status}\n")
    
    print(f"\nПолный отчет сохранен: {report_filename}")
