class Average():   

    @staticmethod
    def calculate(locations = []):
        __latitude  = 0.0
        __longitude = 0.0
        __items = 0.0
        
        for loc in locations:
            try:
                __latitude += loc.latitude
                __longitude += loc.longitude
                __items += 1
            except AttributeError as e:
                print(e)

        try:
            return __latitude / __items, __longitude / __items
        except ZeroDivisionError as e:
            print(e)
    