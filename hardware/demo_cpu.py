import cpufreq

cpu_freq, kpu_freq = cpufreq.get_current_frequencies()

print(cpu_freq, kpu_freq)

