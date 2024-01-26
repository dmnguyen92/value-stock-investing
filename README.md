# Value Stock Investing
A toy model for analyzing the fundamental value of a stock

This work is inspired by [Vincent Tatan](https://github.com/VincentTatan) in his [Medium's post](https://towardsdatascience.com/value-investing-dashboard-with-python-beautiful-soup-and-dash-python-43002f6a97ca) and [github code](https://github.com/VincentTatan/ValueInvesting)

## Usage
* Install neccessary packages in ```requirements.txt```
* Go to ```main.py```, update the input variables
* Run ```main.py```, either from terminal, or using jupyter notebook

```python 
TICKER = 'TSLA'
DISCOUNT_RATE = 0.1 # think like inflation rate
MARGIN_RATE = 0.1 # accounted for error in the evaluation of stock price value
YEARS = 5
```

## Workflow
* Use ```yfinance``` library to extract financial data related to a certain stocks from [https://finance.yahoo.com/](https://finance.yahoo.com/).
* Use rule-based to extract potential red flags
* Estimate future stock price based on annual growth, earning per share (EPS), price-to-earning (PE), while taking into account inflation and calculation error
* Makes decision by comparing the estimated values with the current stock price

## Logic
The list is shamefully taken from this [repo](https://github.com/VincentTatan/ValueInvesting), with some adaptation

### Warning Signs List based on value investing logic
Given list of the companies, find out the feasibility to invest
* Have the track records (EPS per year)
* Can make good use of investment (ROE > 15%) -- Net income / shareholder equity
* Can generate revenue efficiently based on its capital (ROA > 7%) -- Net income / Total Asset
* Have small long term debt (Long term debt <5* total income)
* Low Debt to Equity
* Ability to pay interest: (Interest Coverage Ratio >3) -- EBIT / Interest expenses

## Decision Machine based on Marginal Price From Stocks EPS
Decision making from each company in terms of return rate given the value investing methodology
* Find EPS Annual Compounded Growth Rate
* Estimate EPS XXX years from now
* Estimate stock price XXX years from now (Stock Price EPS * Average PE)
* Determine target by price today based on returns(discount rate)
* Add margin of safety (Safety net)
