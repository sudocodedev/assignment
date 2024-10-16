## 1. An instance of the Rectangle class requires length:int and width:int to be initialized.

```python
class Rectangle:
    def __init__(self, length:int, width:int):
        self.length = length
        self.width = width

    def __str__(self) -> str:
        return f"length - {self.length}, breadth - {self.width}
```


## 2.We can iterate over an instance of the Rectangle class
## 3. When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}

```python
class Rectangle:
    def __init__(self, length:int, width:int):
        self.length = length
        self.width = width

    def __str__(self) -> str:
        return f"length - {self.length}, breadth - {self.width}"

    def __iter__(self):
        yield '{' + f"'length': {self.length}" + '}'
        yield '{' + f"'width': {self.width}" + '}'

r1 = Rectangle(10, 20)

for i in r1:
    print(i)
```
