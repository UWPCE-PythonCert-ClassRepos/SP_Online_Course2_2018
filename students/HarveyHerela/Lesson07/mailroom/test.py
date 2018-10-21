def decorator_func(some_func):
  def wrapper_func(name):    
    output = some_func(name)
    print("Hello ", output)
    
  return wrapper_func

@decorator_func    
def get_name(name):
  return (name)