from model import eligibility_check, get_pred_price_df
from finance_report import get_financial_report
import pandas as pd

##### Declare input variables #######
TICKER = 'TSLA'
DISCOUNT_RATE = 0.1  # inflation rate
MARGIN_RATE = 0.1  # accounted for evaluation of stock price value
YEARS = 5

######## Calculate key metrics #########
df_price, df_finance = get_financial_report(TICKER)
reasons = eligibility_check(df_finance)
df_pred = get_pred_price_df(ticker=TICKER,
                            df_price=df_price,
                            df_finance=df_finance,
                            discount_rate=DISCOUNT_RATE,
                            margin_rate=MARGIN_RATE,
                            years=YEARS)

print("Red flags: ")
if len(reasons) == 0:
    print("None")
else:
    for reason in reasons:
        print(reason)

print("---------------")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df_pred)
