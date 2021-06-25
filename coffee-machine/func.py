class resources:
    _resources = {}
    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            self._resources[k]=v
    def get(self):
        return self._resources
    def findkey(self,k):
        return k in self._resources
    def getvalue(self,k):
        return self._resources[k]
    def putvalue(self,k,v):
        self._resources[k]=v
    def put(self,**kwargs):
        for k,v in kwargs.items():
            self._resources[k]=v
    def is_ingredient_available(self,K):
        return [x for x in K if x not in self._resources]
    def is_ingredient_sufficient(self,K,V):
        return [x for x,y in zip(K,V) if self._resources[x]-y<0]
    def print_resources(self):
        print(self._resources)
class resourcesNotFound(Exception):
    pass

class machine:
    outlets = 0
    res = resources()
    def __init__(self,outlets ,res):
        self.outlets = outlets
        self.res = res
    def get_beverage(self,beverage_type,**kwargs):
        # print(kwargs)
        availability  = self.res.is_ingredient_available(kwargs.keys())
        if availability:
           print(f"{beverage_type} can not be prepared beacause {' '.join(availability)} is not available ")
           return 
        insufficient = self.res.is_ingredient_sufficient(kwargs.keys(),kwargs.values())
        if insufficient:
            print(f"{beverage_type} can not be prepared beacause item {' '.join(insufficient)} is not sufficient")
            return
        for k,v in kwargs.items():            
            # print(k,type(k))
                if self.res.findkey(k):
                    if self.res.getvalue(k)-v>0:
                        self.res.putvalue(k,self.res.getvalue(k)-v)
        print(f"{beverage_type} is prepared")
        
            
    def print_resources(self):
        self.res.print_resources()



    

if __name__ == '__main__':
    data = {
        "machine": {
            "outlets": {
            "count_n": 4
            },
            "total_items_quantity": {
            "hot_water": 500,
            "hot_milk": 500,
            "ginger_syrup": 100,
            "sugar_syrup": 100,
            "tea_leaves_syrup": 100
            },
            "beverages": {
            "hot_tea": {
                "hot_water": 200,
                "hot_milk": 100,
                "ginger_syrup": 10,
                "sugar_syrup": 10,
                "tea_leaves_syrup": 30
            },
            "hot_coffee": {
                "hot_water": 100,
                "ginger_syrup": 30,
                "hot_milk": 400,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
            },
            "black_tea": {
                "hot_water": 300,
                "ginger_syrup": 30,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
            },
            "green_tea": {
                "hot_water": 100,
                "ginger_syrup": 30,
                "sugar_syrup": 50,
                "green_mixture": 30
            },
            }
        }
    }
    outlets = data['machine']['outlets']['count_n']
    res = resources(**data['machine']['total_items_quantity'])
    # res.print_resources()
    coffee_machine = machine(outlets,res)
    for k,v in data['machine']['beverages'].items():
        print(k,v)
        coffee_machine.get_beverage(k,**v)
        print()
        coffee_machine.print_resources()


