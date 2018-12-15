# lesson 05 debugging exercise
# !/usr/bin/env python3

# In very general terms, use a couple of sentences to address the problem with our code. For example, give your best guess or insight on the following questions:

# What is wrong with our logic?
there is no condition to return false and stop calling my_fun(n/2) 

# Why doesn't the function stop calling itself?
if the number is not a power of 2, the code keeps calling itself via my_fun(n/2) 
for 1000 tries (standard recursion limit) and never results in a True 
condition to stop 

# What's happening to the value of 'n' as the function gets deeper and deeper into recursion?
n is becoming smaller and smaller by half and becomes a horizontal asymptote 
approaching 0 but never reaching a resolution to the function call because it 
will never equal 2 once n is smaller than 2




# A copy-and-paste of your terminal debugging activity:

(pythree) C:\Users\ckastner\UW\practice>python -m pdb recursive.py 15
> c:\users\ckastner\uw\practice\recursive.py(1)<module>()
-> import sys
(Pdb) n
> c:\users\ckastner\uw\practice\recursive.py(3)<module>()
-> def my_fun(n):
(Pdb) n
> c:\users\ckastner\uw\practice\recursive.py(9)<module>()
-> if __name__ == '__main__':
(Pdb) n
> c:\users\ckastner\uw\practice\recursive.py(10)<module>()
-> n = int(sys.argv[1])
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(11)<module>()
-> print(my_fun(n))
(Pdb) s
--Call--
> c:\users\ckastner\uw\practice\recursive.py(3)my_fun()
-> def my_fun(n):
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(4)my_fun()
-> if n == 2:
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(7)my_fun()
-> return my_fun(n/2)
(Pdb) pp n
15
(Pdb) s
--Call--
> c:\users\ckastner\uw\practice\recursive.py(3)my_fun()
-> def my_fun(n):
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(4)my_fun()
-> if n == 2:
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(7)my_fun()
-> return my_fun(n/2)
(Pdb) pp n
7.5
(Pdb) ll
  3     def my_fun(n):
  4         if n == 2:
  5             return True
  6
  7  ->     return my_fun(n/2)
(Pdb) b 7
Breakpoint 1 at c:\users\ckastner\uw\practice\recursive.py:7
(Pdb) condition 1 (n/2) < 2
New condition set for breakpoint 1.
(Pdb) c
> c:\users\ckastner\uw\practice\recursive.py(7)my_fun()
-> return my_fun(n/2)
(Pdb) pp n
3.75
(Pdb) s
--Call--
> c:\users\ckastner\uw\practice\recursive.py(3)my_fun()
-> def my_fun(n):
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(4)my_fun()
-> if n == 2:
(Pdb) s
> c:\users\ckastner\uw\practice\recursive.py(7)my_fun()
-> return my_fun(n/2)
(Pdb) pp n
1.875