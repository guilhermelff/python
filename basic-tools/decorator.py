def my_decorator(func):

    def wrapper(*args, **kwargs):

        print("Before function call")

        result = func(*args, **kwargs)

        print("After function call")

        return result

    return wrapper


@my_decorator
def greet(name):

    print(f"Hello, {name}!") 


greet("Alice") 
