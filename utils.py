class VisitedStack(object):
    def __init__(self,size):
        self.stack = []
        self.stack_size = size

    def push(self,obj):
        self.stack.append(obj)
        if len(self.stack) >= self.stack_size: # limit the size so it wont grow
            del self.stack[0]
    def pop(self):
        v = None
        if len(self.stack):
            v=self.stack.pop()
        return v
    def clear(self):
        self.stack.clear()