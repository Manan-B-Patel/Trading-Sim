import requests
import pandas as pd
import json
from alpaca.data import StockHistoricalDataClient, StockBarsRequest, TimeFrame
from datetime import datetime
import time
from prophet import Prophet

def api_call(stock, interval):
    
    modifiedInterval2 = interval.replace("min", "")
    start = int((time.time()*1000) - (3500000*2*1000))
    end = int(time.time()*1000)
    
    url = "https://api.polygon.io/v2/aggs/ticker/" + stock + "/range/" + modifiedInterval2 + "/minute/" + str(start) + "/" + str(end) + "?adjusted=true&sort=asc&limit=50000&apiKey=k1Sgvnez8vKrpDvJwST4mphutWBzZkr4"
    df = requests.get(url)
    print(df)
    df = json.loads(df.text)
    df = df['results']
    
    stock_client = StockHistoricalDataClient("PKVKLLJKRAFKYNB1CVNU", "do0dh8LL62VtNwCB4Y0cUV0vvlJwkcYMrDl8ro1g")
    request_params = StockBarsRequest(
                        symbol_or_symbols=[stock],
                        timeframe=TimeFrame.Minute,
                    )
    
    bars = stock_client.get_stock_bars(request_params)
    global date
    global close
    try:
        df2 = pd.DataFrame(bars[stock])
        bars = df2.to_dict('records')
        
        df2 = []
        for data in bars:
            bar = {
            "o": "",
            "h": "",
            "l": "",
            "c": "",
            "v": "",
            "vw": "",
            "count":"",
            "t": "",
            }
            t = pd.Timestamp(data[1][1])
            d = int((time.mktime(t.timetuple())*1000) - (28800*1000))
            bar["o"] = data[2][1]
            bar["h"] = data[3][1]
            bar["l"] = data[4][1]
            bar["c"] = data[5][1]
            bar["t"] = d
            bar["v"] = data[6][1]
            bar["vw"] = data[8][1]
            bar["count"] = data[7][1]
            df2.append(bar)
            
        data = pd.DataFrame(df)
        data2 = pd.DataFrame(df2)
        date = (data["t"].tolist()) + (data2["t"].tolist())
        close = (data["c"].tolist()) + (data2["c"].tolist())
    except: 
        data = pd.DataFrame(df)
        df2 = None
        data2 = pd.DataFrame()
        date = (data["t"].tolist())
        close = (data["c"].tolist())
    
    return df, df2

def future():
    dateList = []
    for d in date:
        val = datetime.fromtimestamp(d/1000)
        dateList.append(val)
         
    dataValue = pd.DataFrame(dateList, close)
    dataValue.reset_index(inplace=True)
    dataValue.rename(columns= ({"index": "y", 0: "ds"}), inplace=True)
    
    m = Prophet(interval_width=0.95)
    m.fit(dataValue)
    future = m.make_future_dataframe(periods = 2880, freq = 'Min')
    forecast = m.predict(df = future)
    fut = forecast.iloc[len(dateList):,:]
    fut = fut.to_dict('records')
    values = []
    for data in fut:
        bar = {
        "ds": "",
        "trend": "",
        "yhatLower": "",
        "yhatUpper": "",
        "trendLower": "",
        "trendUpper": "",
        "additiveTerms":"",
        "additiveTerms_lower": "",
        "additiveTerms_upper": "",
        "yhat": ""        
        }
        t = pd.Timestamp(data["ds"])
        d = int((time.mktime(t.timetuple())*1000) - (28800*1000))
        bar["trend"] = data["trend"]
        bar["yhatLower"] = data["yhat_lower"]
        bar["yhatUpper"] = data["yhat_upper"]
        bar["trendLower"] = data["trend_lower"]
        bar["ds"] = d
        bar["trendUpper"] = data["trend_upper"]
        bar["additiveTerms"] = data["additive_terms"]
        bar["additiveTerms_lower"] = data["additive_terms_lower"]
        bar["additiveTerms_upper"] = data["additive_terms_upper"]
        bar["yhat"] = data["yhat"]
        values.append(bar)
    return values
    
if __name__ == '__main__':
    api_call('TSLA', '1min')
    future()


    
