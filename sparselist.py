from collections.abc import MutableSequence


class SparseList(MutableSequence):
    def __init__(self, lst=None):
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
            self._data = {k - (k > index): v for k, v in self._data.items()}
            self._len -= 1

        elif isinstance(index, slice):
            start, stop, step = index.indices(self._len)
            if step > 0:
                start, stop, step = stop - 1, start - 1, -step
            for i in range(start, stop, step):
                del self[i]

        else:
            raise TypeError

    def __len__(self):
        return self._len

    def insert(self, index, n):
        if not isinstance(n, (int, float)):
            raise TypeError('can\'t insert not int or float')
        if not isinstance(index, int):
            raise TypeError('position must be int')

        if index < 0:
            index += self._len
            if index < 0:
                index = 0
        self._data = {k + (k >= index): v for k, v in self._data.items()}
        self._data[index] = n
        self._len += 1

    def __repr__(self):
        return '[' + ', '.join(map(str, (self._data.get(i, 0) for i in range(self._len)))) + ']'