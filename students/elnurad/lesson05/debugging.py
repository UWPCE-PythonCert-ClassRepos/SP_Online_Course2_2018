#!/usr/bin/python
import sys

def my_fun(n):
    if n == 2:
        return True

    return my_fun(n/2)

if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))


# The function keeps calling itself without stopping because its termination condition was not set very clearly. It only stops by returning True
# if n equals 2 or another number that is a power of 2, e.g. 8, 16, 32, 64. Otherwise, no termination condition is implemented and as a result, 
# the function keeps calling itself endlessly. The value of n keeps decreasing with each recursion of the recursive function
# since the function doesn't know when to stop and keeps calling itself. 

# Below is my debugging log:

# PS C:\Users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05> python -m pdb debugging.py 15
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(2)<module>()
# -> import sys
# (Pdb) ll
#   1     #!/usr/bin/python
#   2  -> import sys
#   3
#   4     def my_fun(n):
#   5         if n == 2:
#   6             return True
#   7
#   8         return my_fun(n/2)
#   9
#  10     if __name__ == '__main__':
#  11         n = int(sys.argv[1])
#  12         print(my_fun(n))
#  13
#  14
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)<module>()
# -> def my_fun(n):
# (Pdb) pp n
# *** NameError: name 'n' is not defined
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(10)<module>()
# -> if __name__ == '__main__':
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(11)<module>()
# -> n = int(sys.argv[1])
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(12)<module>()
# -> print(my_fun(n))
# (Pdb) pp n
# 15
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 15
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) pp n
# 7.5
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 3.75
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 1.875
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.9375
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.46875
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.234375
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.1171875
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.05859375
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.029296875
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.0146484375
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.00732421875
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) s
# --Call--
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(4)my_fun()
# -> def my_fun(n):
# (Pdb) s
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(5)my_fun()
# -> if n == 2:
# (Pdb) pp n
# 0.003662109375
# (Pdb) n
# > c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py(8)my_fun()
# -> return my_fun(n/2)
# (Pdb) n
# Traceback (most recent call last):
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\pdb.py", line 1667, in main
#     pdb._runscript(mainpyfile)
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\pdb.py", line 1548, in _runscript
#     self.run(statement)
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\bdb.py", line 434, in run
#     exec(cmd, globals, locals)
#   File "<string>", line 1, in <module>
#   File "c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py", line 12, in <module>
#     print(my_fun(n))
#   File "c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py", line 8, in my_fun
#     return my_fun(n/2)
#   File "c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py", line 8, in my_fun
#     return my_fun(n/2)
#   File "c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py", line 8, in my_fun
#     return my_fun(n/2)
#   [Previous line repeated 980 more times]
#   File "c:\users\elnura\documents\pythoncert\sp_online_course2_2018\students\elnurad\lesson05\debugging.py", line 4, in my_fun
#     def my_fun(n):
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\bdb.py", line 53, in trace_dispatch
#     return self.dispatch_call(frame, arg)
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\bdb.py", line 79, in dispatch_call
#     if not (self.stop_here(frame) or self.break_anywhere(frame)):
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\bdb.py", line 176, in break_anywhere
#     return self.canonic(frame.f_code.co_filename) in self.breaks
#   File "C:\Users\elnura\AppData\Local\Programs\Python\Python36\lib\bdb.py", line 32, in canonic
#     if filename == "<" + filename[1:-1] + ">":
# RecursionError: maximum recursion depth exceeded in comparison
# Uncaught exception. Entering post mortem debugging
# Running 'cont' or 'step' will restart the program
