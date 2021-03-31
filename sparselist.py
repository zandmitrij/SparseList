from collections.abc import MutableSequence

class SparseList(MutableSequence):
    
    def _indexcheck(f):
        def inner(self, *args):
            index = args[0]
            if isinstance(index, int):
                if index < 0:
                    index += self._len
                if not (0 <= index < self._len):
                    raise IndexError('list index out of range') 
            elif isinstance(index, slice):
                index = index.indices(self._len)
            else:
                raise TypeError('Not valid type of index')
            
            args = list(args)
            args[0] = index
            return f(self, *args)        
        return inner
    
    
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
    
    @_indexcheck
    def __getitem__(self, index):
        if isinstance(index, int):
            return self._data.get(index, 0)
        else:   # if index is tuple of indices
            return SparseList([self[i] for i in range(*index)])
        
    @_indexcheck
    def __setitem__(self, index, obj):
        if isinstance(index, int):
            if not isinstance(obj, (int, float)):
                raise TypeError('Only int and float types are allowed to SparseList')
            if obj != 0:
                self._data[index] = obj
            else:
                try:
                    self._data.pop(index)
                except KeyError:
                    pass
                
        else:   # if index is slice
            start, stop, step = index
            
            if step == 1:
                if not isinstance(obj, (int, float, list, SparseList)):
                    raise TypeError('not valid type!')
                if isinstance(obj, (int, float)):
                    obj = [obj]
                del self[start:stop]
                for i in reversed(obj):
                    self.insert(start, i)
                             
            else:   # if step not equals 1
                if not isinstance(obj, (list, SparseList)):
                    raise TypeError('only list and SparseList types is allowed')
                if len(range(*index)) != len(obj):
                    raise ValueError('attempt to assign sequence to extended slice with not same size')
                it_obj = iter(obj)
                for i in range(*index):
                    del self[i]
                    self.insert(i, next(it_obj))
                    
            
    @_indexcheck
    def __delitem__(self, index):
        if isinstance(index, int):
            if self[index] != 0:
                del self._data[index]
            self._data = {k-(k>index) : v for k, v in self._data.items()}
            self._len -= 1
            
        else:
            start, stop, step = index
            if step > 0:
                index = stop-1, start-1, -step 
            for i in range(*index):
                del self[i]
    
        
    def __len__(self):
        return self._len
    
    def insert(self, index, n):
        if not isinstance (n, (int, float)):
            raise TypeError('can\'t insert not int or float')
        if not isinstance (index, int):
            raise TypeError('position must be int')
                            
        if index < 0:
            index += self._len
        index = max(index, 0)
        index = min(index, self._len)
        self._data = {k + (k>=index):v for k, v in self._data.items()}
        if n != 0:
            self._data[index] = n
        self._len += 1
    
    
    def __repr__(self):
        return '[' + ', '.join(map(str, (self._data.get(i, 0) for i in range(self._len)))) + ']'
    
