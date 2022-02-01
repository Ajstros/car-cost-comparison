# car-cost-comparison
Compare cost between cars over the number of miles driven using US EIA data.

# EIA
The U.S. Energy Information Administration has publicly available data on [fuel effiency](https://www.fueleconomy.gov/feg/findacar.shtml) as well as [gas prices](https://www.eia.gov/petroleum/gasdiesel/) and [electricity prices](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_06_b) throughout the United States. Using this data, we can determine the cost of using a car according to the number of miles one drives. This comparison can be helpful in purchase decisions, as well as showing the energy and economic efficiency of electric cars over gas-powered cars.

# Installation
Copy the repository onto your machine from [GitHub](https://github.com/Ajstros/car-cost-comparison).

# Dependencies
- pandas
- numpy
- matplotlib
- bs4
- requests
These can be installed from the requirements.txt file in this repository:
```sh
pip install -r requirements.txt
```

# Usage
After copying the repository, run gui.py to run the program. Choose your state by clicking on the button defaulting to "Alabama."  Enter the estimated number of miles driven per day rounded to the nearest integer in the box labeled "Miles per Day (int)." Click "Add Car" to add a car to your comparison. Click on the first and second buttons of the newly added row to choose the make and model of the car. Enter the price of the car in the box labeled "Initial Price" to include purchasing costs in your comparison. Add more cars with the "Add Car" button, filling out the added rows. When ready, click "Graph" to produce a graph of cost (USD) vs. time (days) comparing the selected cars.