class Person:
    name="dev"
    occupation="coder"
    def info (self):
        self.__game="goc"
        print(f"{self.name} is a {self.occupation} and loves {self.__game}")
    
a=Person()
b=Person()
a.name="shub"
a.occupation="leader"
print(a.info(),b.info() )
#print(help(a.info()))
#print(dir(a))
#print(dir(a))
import pandas as pd
import numpy as np
df = pd.DataFrame(
    {
        "one": pd.Series(np.random.randn(3), index=["a", "b", "c"]),
        "two": pd.Series(np.random.randn(4), index=["a", "b", "c", "d"]),
        "three": pd.Series(np.random.randn(3), index=["b", "c", "d"]),
    }
)
print(df.apply(lambda x: np.mean(x)))

arr = np.random.randn(20)
print(arr)

x = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 4, 5]})

x.iloc[1] = {'x': 9, 'y': 99}

print(x)