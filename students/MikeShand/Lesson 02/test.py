def OutFunction():
    def InFunction(inputString):
        print(inputString)
    return InFunction

testString = "Hello"
test = OutFunction()
print("Original string:")
test(testString)
testString = "World"
print("New string:")
test(testString)
testString