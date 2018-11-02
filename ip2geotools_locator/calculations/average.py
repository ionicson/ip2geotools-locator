class Average():   

    @staticmethod
    def calculate(locations = []):
        __latitude  = 0.0
        __longitude = 0.0
        __items = 0.0
        
        for loc in locations:
            __latitude += loc.latitude
            __longitude += loc.longitude
            __items += 1

        return __latitude / __items, __longitude / __items
    