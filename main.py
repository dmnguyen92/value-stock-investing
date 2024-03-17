from model import eligibility_check, get_pred_price_df
from finance_report_yahoo import get_financial_report_yahoo, get_price_yahoo
from finance_report_macrotrend import get_financial_report_macro
import pandas as pd

##### Declare input variables #######
TICKER = 'SKX'
DISCOUNT_RATE = 0.12  # expected return
MARGIN_RATE = 0.1  # accounted for evaluation of stock price value
YEARS = 8
df_price = get_price_yahoo(TICKER, YEARS+1)
df_finance = get_financial_report_macro(TICKER)

######## Calculate key metrics #########
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

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df_pred)
