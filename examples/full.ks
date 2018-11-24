; Color enum
[EColor]
_def = enum <byte> 
	{
		white,
		red(3),
		green,
		blue(-2),
		black
	}


; Parent class
[Parent]
_def = class
p1 = uint


# Child class
[Child]
_def = class(Parent)
c = string


# Test class
[Test]
_def = class
v0 = boolean
v1 = char
v2 = byte
v3 = ubyte
v4 = short
v5 = ushort
v6 = int
v7 = uint
v8 = long
v9 = ulong
v10 = float
v11 = double
v12 = string

v13 = EColor
v14 = Child

v15 = list<int>
v16 = list<list<char>>

v17 = map<string, int>
v18 = map<char, list<map<double, EColor>>>

v19 = array[10] <byte>
v20 = array[10][20] <list<string>>

v21 = list<array[4] <Child>>
v22 = map<string, Child>
v23 = array[5][10] <Child>
