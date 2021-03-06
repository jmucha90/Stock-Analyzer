import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go


class lrmodel:
    '''
    Building class to develop the linear regression model to be used in the application.
    '''

    def __init__(self, ticker):
        ticker = ticker
        self.info = yf.Ticker(str(ticker)).info

    # Gets the stock historical data and ensures that no non-numerical data exists
    def history(self, ticker):
        ticker = ticker
        stock_history = yf.Ticker(str(ticker)).history(period='max')
        if stock_history.isnull().values.any():
            issues = stock_history[stock_history.isnull().values]
            issue_index = []
            for issue in issues.index:
                if issue not in issue_index:
                    issue_index.append(issue)
                    stock_history.drop([issue], inplace = True)
            return stock_history
        else:
            return stock_history

    # Builds the linear regression model
    def linearregression(self, ticker):
        stockdata = self.history(ticker)
        num_train_vals = round(len(stockdata) * .80)
        model = LinearRegression()
        X_train = stockdata[:num_train_vals]
        X_train = X_train.drop('Close', axis=1)
        X_test = stockdata[num_train_vals:]
        X_test = X_test.drop('Close', axis=1)
        y_train = stockdata[:num_train_vals]
        y_train = y_train[['Close']]
        y_test = stockdata[num_train_vals:]
        y_test = y_test[['Close']]
        model.fit(X_train, y_train)
        trainingpredictions = pd.DataFrame()
        trainingpredictions['Predictions'] = model.predict(X_train).flatten()
        trainingpredictions.index = X_train.index
        testpredictions = pd.DataFrame()
        testpredictions['Predictions'] = model.predict(X_test).flatten()
        testpredictions.index = X_test.index
        return testpredictions

    # Graphs the results of the linear regression on a Plotly graph
    def graphlrresults(self, ticker):
        stockdata = self.history(ticker)
        num_train_vals = round(len(stockdata) * .80)
        actualdatafortrain = stockdata[:num_train_vals]
        actualdatafortest = stockdata[num_train_vals:]
        testpredictions = self.linearregression(ticker)
        predfig = go.Figure()
        # Create and style traces
        predfig.add_trace(go.Scatter(x=actualdatafortrain.index, y=actualdatafortrain['Close'], name='Actual Training Set Price',
                                     line=dict(color='#003300', width=2)))
        predfig.add_trace(go.Scatter(x=actualdatafortest.index, y=actualdatafortest['Close'], name='Actual Test Set Price',
                                     line=dict(color='#1A0099', width=2)))
        predfig.add_trace(go.Scatter(x=testpredictions.index, y=testpredictions['Predictions'], name='Test Predictions',
                                     line=dict(color='#CC0000', width=2)))
        predfig.update_layout(title=str(ticker) + '\'s Stock Price Predicted by Linear Regression',
                              xaxis_title='Date',
                              yaxis_title='USD')
        fig = predfig.show()
        return fig
