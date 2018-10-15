def OutFunction(inputString):
    def InFunction():
        print(inputString)
    return InFunction

testString = "Hello"
test = OutFunction(testString)
print("Original string:")
test()
testString = "World"
print("New string:")
test()
testString