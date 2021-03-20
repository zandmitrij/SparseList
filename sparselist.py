class SparseList():
    """
    Class SparseList for sequnces which contains about 90-95% of zeroes.
    That class have behaviour equals of list, but non-zero elements is in dictionary
    """


    def __init__(self, lst = None):
        self._data = {}
        self._len = 0
        if lst is not None:
            if isinstance(lst, (list, tuple)):
                for i in lst:
                    self.append(i)
            elif isinstance(lst, SparseList):
                    self._data = lst._data.copy()
                    self._len = lst._len
            else:
                raise TypeError
	
	
    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += self._len
            if not (0 <= index < self._len):
                raise IndexError('list index out of range')
            return self._data.get(index, 0)

        if isinstance(index, slice):
            start, stop, step = index.indices(self._len)
            return SparseList([self._data.get(i, 0) for i in range(start, stop, step)])
        raise TypeError
        
    	
    def __setitem__(self, index, obj):
        if isinstance(index, int):
            if index < 0:
                index += self._len
            if not (0 <= index < self._len):
                raise IndexError('list index out of range')
            if not isinstance(obj, (int, float)):
                raise TypeError('Only int and float types are allowed to SparseList')
            if obj != 0:
                self._data[index] = obj
            else:
                try:
                    self._data.pop(index)
                except KeyError:
                    pass

        elif isinstance(index, slice):
            start, stop, step = index.indices(self._len)

            if step == 1:
                if isinstance(obj, (int, float)):
                    del self[start:stop]
                    self.insert(start, obj)
                elif isinstance(obj, (list, SparseList)):
                    del self[start:stop]
                    for i in reversed(obj):
                        self.insert(start, i)
                else:
                    raise TypeError('not valid type!')

            else:
                if isinstance(obj, (list, SparseList)):

                    if len(range(start, stop, step)) != len(obj):
                        raise ValueError('attempt to assign sequence to extended slice with not same size')
                    else:
                        it_obj = iter(obj)
                        for i in range(start, stop, step):
                            del self[i]
                            self.insert(i, next(it_obj))

                else:
                    raise TypeError('only list and SparseList types is allowed')

        else:
            raise TypeError
	
	
    def __delitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index += self._len
            if not (0 <= index < self._len):
                raise IndexError('list index out of range')
            if self[index] != 0:
                del self._data[index]
            self._data = {k - (k>index):v for k, v in self._data.items()}
            self._len -= 1

        elif isinstance(index, slice):
            start, stop, step = index.indices(self._len)
            if step > 0:
                start, stop, step = stop-1, start-1, -step
            for i in range(start, stop, step):
                del self[i]

        else:
            raise TypeError
        
	
    def __iter__(self):
        for i in range(self._len):
            yield self._data.get(i, 0)
	
	
    def __contains__(self, i):
        if i == 0:
            return len(self._data) != self._len
        return i in self._data.values()
	
	
    def __len__(self):
        return self._len
	
        
    def __reversed__(self):
        a = self.copy()
        a.reverse()
        return iter(a)
        
	
    def __repr__(self):
	return '[' + ', '.join(map(str, (self._data.get(i, 0) for i in range(self._len)))) + ']'
        
        
    # перегрузим арифметические операторы
        
    def __add__(self, other, /):
        if not isinstance(other, (list, SparseList)):
            raise TypeError('can\'t concatenate')
        a = self.copy()
        a.extend(other)
        return a
        
        
    def __radd__(self, other, /):
        if not isinstance(other, (list, SparseList)):
            raise TypeError('can\'t concatenate')
        a = self.copy()
        for i, n in enumerate(other):
            a.insert(i, n)
        return a
        
        
    def __iadd__(self, other, /):
        if not isinstance(other, (list, SparseList)):
            raise TypeError('can\'t concatenate')
        self.extend(other)
        return self
        
        
    def __mul__(self, other, /):
        if not isinstance(other, int):
            raise TypeError('can\'t multiply sequence by not int type')
        a = SparseList()
        for _ in range(other):
            a.extend(self)
        return a

        
    def __rmul__(self, other, /):
        return self * other
        
        
    def __imul__(self, other, /):
        if not isinstance(other, int):
            raise TypeError('can\'t multiply sequence by not int type')
        a = self.copy()
        for _ in range(other-1):
            self.extend(a)
        return self
        
    # перегрузим операторы сравнения
        
    def __eq__(self, other, /):
        if isinstance(other, (list, SparseList)):
            if self._len == len(other):
                for i in range(self._len):
                    if not self[i] == other[i]:
                        break
                else:
                    return True
        return False
        
        
    def __gt__(self, other, /):
        if isinstance(other, (list, SparseList)):
            s = min(self._len, len(other))
            for i in range(s):
                if self[i] == other[i]:
                    continue
                return self[i] > other[i]
            else:
                return self._len > len(other)
        else:
            raise TypeError(f'can\'t compare SparseList and {type(other)}')
        
        
    def __lt__(self, other, /):
        if isinstance(other, (list, SparseList)):
            s = min(self._len, len(other))
            for i in range(s):
                if self[i] == other[i]:
                    continue
                return self[i] < other[i]
            else:
                return self._len < len(other)
        else:
            raise TypeError(f'can\'t compare SparseList and {type(other)}')
        
        
    def __ge__(self, other, /):
        return not self < other
        
        
    def __le__(self, other, /):
        return not self > other
        
        
    # Здесь перегрузим немагические методы
        
    def append(self, n, /):
        if not isinstance(n, (int, float)):
            raise TypeError('can\'t append not int or float type')
        if n != 0:
            self._data[self._len] = n
        self._len += 1

    def clear(self):
        self._data = {}
        self._len = 0
        
        
    def copy(self, /):
        return SparseList(self)
        
        
    def count(self, value):
        if value == 0:
            return self._len - len(self._data)
        c = 0
        for i in self._data.values():
            if i == value:
                c += 1
        return c
        
        
    def extend(self, ob):
        for i in ob:
          self.append(i)
        
        
    def index(self, n, start=None, stop=None):
        if not isinstance(n, (int, float)):
            raise TypeError
        if start is None:
            start = 0
        elif start < 0:
            start = 0
        if stop is None:
            stop = self._len
        elif stop > self._len:
            stop = self._len
        
        for i in range(start, stop):
            if self._data.get(i, 0) == n:
                return i
        raise ValueError(f'{n} not in list')
        
        
    def insert(self, index, n):
        if not isinstance (n, (int, float)):
            raise TypeError('can\'t insert not int or float')
        if not isinstance (index, int):
            raise TypeError('position must be int')
        
        if index >= self._len:
            self.append(n)
        else:
            if index < 0:
                index += self._len
                if index < 0:
                    index = 0
            self._data = {k + (k>=index):v for k, v in self._data.items()}
            self._data[index] = n
            self._len += 1
        
        
    def pop(self, index=None):
        if self._len == 0:
            raise IndexError('pop from empty list')
        if index is None:
            index = self._len - 1
        if index < 0:
            index += self._len
        if not (0 <= index < self._len):
            raise IndexError('pop index out of range')
        
        val = self[index]
        del self[index]
        return val
        
        
    def remove(self, n):
        if not isinstance(n, (int, float)):
            raise TypeError
        for i in range(self._len):
            if self._data.get(i, 0) == n:
                self.pop(i)
                return
        raise ValueError(f'{n} not in list')
        
        
    def reverse(self):
        self._data = {self._len-1 - k: v for k, v in self._data.items()}
        
        
    def sort(self, key=None, reverse=False):
        if key is None:
            key = lambda x: x
        vals = self._data.values()
        vals = list(zip(map(key, vals), vals))
        vals.sort(key=lambda x: x[0])
        
        negatives = [i for k_i, i in vals if k_i < 0]
        positives = [i for k_i, i in vals if k_i > 0]
        zeros = self._len - len(self._data)
        
        dt = {}
        c = 0
        while c < self._len:
            while negatives:
                dt[c] = negatives.pop(0)
                c += 1
            c += zeros
            while positives:
                dt[c] = positives.pop(0)
                c += 1
        
        self._data = dt
        if reverse:
            self.reverse()
