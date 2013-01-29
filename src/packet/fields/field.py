import sys
sys.path.append(sys.path[0][:-18])

class Field:
    def __init__(self,name,value):
        self._name = name
        self._value = value
        
    def value(self):
        return self._value
    
    def set_value(self,value):
        self._value = value
    
    def name(self):
        return self._name
    
    def __str__(self):
        return self._name + ": " + str(self._value)
    



        
    

    
    
