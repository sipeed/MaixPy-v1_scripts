from Maix import freq

cpu_freq, kpu_freq = freq.get()
print(cpu_freq, kpu_freq)

freq.set(cpu = 400, pll1=400, kpu_div = 1)



