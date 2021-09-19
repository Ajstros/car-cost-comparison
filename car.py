"""Car class for representing cars and their cost."""

import pandas as pd


class Car:
    """Car class for representing cars and their cost."""

    ELECTRIC = 'Electric'
    GAS = 'Gas'
    vehicles = None
    make_model_dict = None

    def __init__(self, name, type, mileage, initial_price=0):
        self.name = name
        self.type = type
        self.initial_price = initial_price
        self.mileage = mileage

    def __str__(self):
        return self.name

    def get_info(self):
        if type == Car.ELECTRIC:
            units = 'kWh/mile'
        else:
            units = 'miles/gallon'

        return f'{self.name}; {self.type}; ${self.initial_price}, {self.mileage} {units}'

    @classmethod
    def get_vehicles_csv(cls):
        if cls.vehicles is None:
            cls.vehicles = pd.read_csv('vehicles.csv', low_memory=False)
        return cls.vehicles

    @classmethod
    def get_make_model_dict(cls):
        if cls.make_model_dict is None:
            vehicles = cls.get_vehicles_csv()
            make_model_df = vehicles[['make', 'model']]
            make_model_dict = {}
            # Set model to index when we make dict to keep the different models for the same make
            make_model_df.set_index('model', inplace=True)
            model_make_dict = make_model_df.to_dict()['make']
            for model in model_make_dict:
                make = model_make_dict[model]
                if make_model_dict.get(make) is None:
                    make_model_dict[make] = [model]
                else:
                    make_model_dict[make].append(model)
            for value in make_model_dict.values():
                value.sort()
            cls.make_model_dict = make_model_dict
        return cls.make_model_dict


    @classmethod
    def get_car(cls, make, model):
        vehicles = cls.get_vehicles_csv()
        data = vehicles.loc[(vehicles['make'] == make) & (
            vehicles['model'] == model)]
        if data.empty:
            # No cars match
            return None
        else:
            # Treat data as a Series rather than a DataFrame
            data = data.iloc[0]
        name = ' '.join((make, model))
        if data['fuelType'] == 'Electricity':
            fuel_type = cls.ELECTRIC
            # Table gives in kWh per 100 miles, we want per mile
            mileage = data['combE'] / 100
        else:
            fuel_type = cls.GAS
            # Table gives mpg, we want gallons/mile
            mileage = 1 / data['comb08']
        return cls(name=name, type=fuel_type, mileage=mileage)

    @classmethod
    def get_all_cars(cls):
        vehicles = Car.get_vehicles_csv
        cars = []
        for row_number in range(len(vehicles)):
            data = vehicles.iloc[row_number]
            make = data['make']
            model = data['model']
            name = ' '.join((make, model))
            if data['fuelType'] == 'Electricity':
                fuel_type = Car.ELECTRIC
                # Table gives in kWh per 100 miles, we want per mile
                mileage = data['combE'] / 100
            else:
                fuel_type = Car.GAS
                # Table gives mpg, we want gallons/mile
                mileage = 1 / data['comb08']
            cars.append(Car(name=name, type=fuel_type, mileage=mileage))
        return cars
