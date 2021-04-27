import ctypes

libc = ctypes.cdll.LoadLibrary("./libc.so")
number_solutions = libc.mainC(9,1)
number_solutions += libc.mainC(9,2)
number_solutions += libc.mainC(9,3)
number_solutions += libc.mainC(9,4)
print("Number of found solutions is %d" %number_solutions)