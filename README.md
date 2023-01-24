# Trading-Sim

Created a Flask finance dashboard that displays 2-month historical intraday (1-60min) candlestick chart with MAV &
Volume indicators & used Prophet, a time series forecasting machine learning model, to predict prices at a 95% confidence level.
Utilizing python’s requests module, I collected data through API calls and processed/formatted that data using pandas. Used WebSocket to stream live 1min candlestick bars, plotting in real time, & used TradingView’s API widgets to
display current financial news & market stats
