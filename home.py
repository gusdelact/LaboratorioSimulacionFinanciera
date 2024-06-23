import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
import plotly.graph_objects as go

stock_symbols=None

def calculate_technical_indicators(df):
    """
    Calculate common technical indicators for the given DataFrame.
    """
    # Calculate 7-day and 21-day moving averages
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA21'] = df['Close'].rolling(window=21).mean()

    # Calculate MACD
    df['26EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['12EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['MACD'] = df['12EMA'] - df['26EMA']

    # Calculate Bollinger Bands
    df['20SD'] = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['MA21'] + (2 * df['20SD'])
    df['Lower_Band'] = df['MA21'] - (2 * df['20SD'])

    return df

def get_stock_data(ticker_symbol, start_date, end_date,attributes, include_indicators=False):
    """
    Fetch and display stock data for the given ticker symbol and date range.
    If include_indicators is True, also calculate and display technical indicators.
    """
    ticker = yf.Ticker(ticker_symbol)

    # Fetch price history
    price_history = ticker.history(period="1mo", start=start_date, end=end_date)
    
    if include_indicators:
        # Calculate technical indicators
        price_history = calculate_technical_indicators(price_history)

    placeholder = st.empty()
    with placeholder.container():
        st.subheader(f"Summary {ticker_symbol}")
        for attribute in attributes:
            st.write(f"{attribute}")
        # Display price history
        st.subheader(f"Price History for {ticker_symbol}")
        st.write(price_history)
# Create and display price chart
        st.subheader(f"Price Chart for {ticker_symbol}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=price_history.index, y=price_history['Close'], mode='lines', name='Closing Price'))

        if include_indicators:
            fig.add_trace(go.Scatter(x=price_history.index, y=price_history['MA7'], mode='lines', name='7-day MA'))
            fig.add_trace(go.Scatter(x=price_history.index, y=price_history['MA21'], mode='lines', name='21-day MA'))
            fig.add_trace(go.Scatter(x=price_history.index, y=price_history['MACD'], mode='lines', name='MACD'))
            fig.add_trace(go.Scatter(x=price_history.index, y=price_history['Upper_Band'], mode='lines', name='Upper Bollinger Band'))
            fig.add_trace(go.Scatter(x=price_history.index, y=price_history['Lower_Band'], mode='lines', name='Lower Bollinger Band'))

        fig.update_layout(title=f'Closing Price for {ticker_symbol}', xaxis_title='Date', yaxis_title='Price ($)')
        st.plotly_chart(fig)

        if st.button("Agregar a la Simulación"):
            print(st.session_state['stocks'].keys())
            if  not ticker_symbol in st.session_state['stocks'] :
                st.session_state['stocks'][ticker_symbol]=price_history
                st.sidebar.write("Agregado a la simulación")
            else:
                st.sidebar.write("Ya estaba agregado a la simulación")
            placeholder.empty()


    # # Display actions (dividends and splits)
    # st.subheader(f"Actions for {ticker_symbol}")
    # actions = ticker.actions
    # st.write(actions)

    # # Display balance sheet
    # st.subheader(f"Balance Sheet for {ticker_symbol}")
    # balance_sheet = ticker.balance_sheet
    # st.write(balance_sheet)
    # # Calendario de eventos
    # st.subheader("Calendario de Eventos")
    # calendar = ticker.calendar
    # st.write(calendar)

    # # Flujo de caja
    # st.subheader("Flujo de Caja")
    # cash_flow = ticker.cash_flow
    # st.write(cash_flow)

    # # Dividendos
    # st.subheader("Dividendos")
    # dividends = ticker.dividends
    # st.write(dividends)

    # # Fechas de ganancias
    # st.subheader("Fechas de Ganancias")
    # earnings_dates = ticker.earnings_dates
    # st.write(earnings_dates)

    # # Información rápida
    # st.subheader("Información Rápida")
    # fast_info = ticker.fast_info
    # st.write(fast_info)

    # # Estados financieros
    # st.subheader("Estados Financieros")
    # financials = ticker.financials
    # st.write(financials)

    # # Información de la compañía
    # st.subheader("Información de la Compañía")
    # info = ticker.info
    # st.write(info)

    # # Compras de insiders
    # st.subheader("Compras de Insiders")
    # insider_purchases = ticker.insider_purchases
    # st.write(insider_purchases)

    # # Roster de insiders
    # st.subheader("Roster de Insiders")
    # insider_roster_holders = ticker.insider_roster_holders
    # st.write(insider_roster_holders)

    # # Transacciones de insiders
    # st.subheader("Transacciones de Insiders")
    # insider_transactions = ticker.insider_transactions
    # st.write(insider_transactions)

    # # Holders institucionales
    # st.subheader("Holders Institucionales")
    # institutional_holders = ticker.institutional_holders
    # st.write(institutional_holders)

    # # ISIN
    # st.subheader("ISIN")
    # isin = ticker.isin
    # st.write(isin)

    # # Holders principales
    # st.subheader("Holders Principales")
    # major_holders = ticker.major_holders
    # st.write(major_holders)

    # # Holders de fondos mutuos
    # st.subheader("Holders de Fondos Mutuos")
    # mutualfund_holders = ticker.mutualfund_holders
    # st.write(mutualfund_holders)

    # # Noticias
    # st.subheader("Noticias")
    # news = ticker.news
    # st.write(news)

    # # Opciones disponibles
    # st.subheader("Opciones Disponibles")
    # options = ticker.options
    # st.write(options)

    # # Balance general trimestral
    # st.subheader("Balance General Trimestral")
    # quarterly_balance_sheet = ticker.quarterly_balance_sheet
    # st.write(quarterly_balance_sheet)

    # # Flujo de caja trimestral
    # st.subheader("Flujo de Caja Trimestral")
    # quarterly_cash_flow = ticker.quarterly_cash_flow
    # st.write(quarterly_cash_flow)

    # # Estados financieros trimestrales
    # st.subheader("Estados Financieros Trimestrales")
    # quarterly_financials = ticker.quarterly_financials
    # st.write(quarterly_financials)

    # # Recomendaciones
    # st.subheader("Recomendaciones")
    # recommendations = ticker.recommendations
    # st.write(recommendations)

    # # Resumen de recomendaciones
    # st.subheader("Resumen de Recomendaciones")
    # recommendations_summary = ticker.recommendations_summary
    # st.write(recommendations_summary)

    # # Splits
    # st.subheader("Splits")
    # splits = ticker.splits
    # st.write(splits)

    # # Actualizaciones y rebajas
    # st.subheader("Actualizaciones y Rebajas")
    # upgrades_downgrades = ticker.upgrades_downgrades
    # st.write(upgrades_downgrades)
def simulate():
    print(st.session_state['stocks'].keys())
    for the_tickersymbol in st.session_state['stocks'].keys():
       the_history=st.session_state['stocks'].get(the_tickersymbol)
       print(the_history.describe())
    st.session_state['stocks']={}

def main():
  if 'stocks' not in st.session_state:
      st.session_state['stocks'] = {} 

  with st.sidebar:
      #add this logo  to the sidebar
      st.image( "https://www.anahuac.mx/mexico/posgrados/sites/default/files/logo_60_3.png")
      # Selectbox for capital markets
      capital_markets = ['nyse','nasdaq', 'amex']
      capital_market = st.selectbox("Seleccione el mercado", options=capital_markets, index=None)
      if capital_market:
        # Leer el archivo Excel y la hoja 'nasdaq'
        df = pd.read_excel('listings.xlsx', sheet_name=capital_market)
        stock_symbols = df['Stock Symbol'].tolist()
        #sort stock_symbols in ascending
        stock_symbols.sort()
      
          #add two fields for start and end date for historic
          #current date
        ed=date.today()
        ed_10_years_ago = ed - timedelta(days=3650)  # 10 years * 365 days per year
        ed_5_years_ago = ed - timedelta(days=1825)  # 5 years * 365 days per year
        
        start_date = st.date_input("Start Date",min_value=ed_10_years_ago,value=ed_10_years_ago)
        end_date = st.date_input("End Date",min_value=ed)
        ticker_symbol = st.selectbox("Seleccione el símbolo del ticker", stock_symbols, index=None)
        st.write(f"Lista de tickers a simular:")
        for key in st.session_state['stocks'].keys():
             st.write(f"{key}")

        if st.button("Simular"):
            st.write("Simulando")
            simulate()

  if capital_market and ticker_symbol:
    df.set_index('Stock Symbol',inplace=True)
    list_attributes=[]
    for attribute in df.loc[ticker_symbol].index:
        list_attributes.append(f"{attribute}: {df.loc[ticker_symbol][attribute]}")
  
    get_stock_data(ticker_symbol, start_date, end_date,list_attributes, include_indicators=True)

if __name__ == "__main__":
    main()
