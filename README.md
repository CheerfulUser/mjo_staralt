mjo_staralt
===========
Scripts to make a quick visibility plot for a given static target. Adapted from Aayushi Verma's code [NEOExchange-Observations-Planner](https://github.com/awesomecosmos/NEOExchange-Observations-Planner).

You can pip install mjo_staralt as:
```bash
pip install git+https://github.com/CheerfulUser/mjo_staralt.git
```

Once it is successfully installed, the visibility curve can be plotted for any target with just:
```python
from mjo_staralt import mjo_alt
mjo_alt(ra=44,dec=-11,date='2021-12-03')
```
If no date is provided then it defaults to the current date. 

Scripts can also be run through the commandline with mjo_alt.py which takes arguments of ra, dec, and date in the format of 'YYYY-mm-dd'. If a date is not specified then the current date is used.

Currently the output time is in reference to NZ local time, so might break if used in another timezone...
