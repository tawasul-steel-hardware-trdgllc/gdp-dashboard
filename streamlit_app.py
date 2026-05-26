import openai
import requests
import json
import streamlit as st
import os

openai.api_key =os.environ.get("OPENAI_API_KEY")
#openai.api_key = st.secrets["OPENAI_API_KEY"]


def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}
        ]
    )
    return completion.choices[0].message.content

st.title("ChatGPT advanced prompting with python")
st.subheader("Example: Crypto trading analysis with ChatGPT")


def GetBitCoinPrices():
    # define the api endpoint and query parameters
    url="https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring={"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"7d"}
    
    # define the headers with the API key and host
    headers={
        "x-rapidapi-key":"e760a9215amsh52936875b678e9ap166f34jsn8461b6dbc6fb",
        "x-rapidapi-host":"coinranking1.p.rapidapi.com",
        "Content-Type":"application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)

    #parse the response data as a json object
    JSONResult = json.loads(response.text)
    #extract the history field from the json response
    history = JSONResult["data"]["history"]
    #extract the price field from each item in the history list and store it in a new list
    prices=[]
    for change in history:
        prices.append(change["price"])
        
        # joing he list of prices into a single string with commas as separators
        
        pricesList = ",".join(prices)
        
    return pricesList


if st.button("Get Bitcoin Analysis"):
    with st.spinner("Analyzing Bitcoin prices..."):
        bitcoinPrices= GetBitCoinPrices()
        st.success("Done!")
    with st.spinner("Generating analysis with ChatGPT..."):
        chatGPTPrompt = """You are an expert crypto trader with more than 10 years of experience, 
                        I will provide you with the bitcoin prices for the last 7days
                        can you provide me with a technical analysis of
                        Bitcoin based on these prices. here is what I want:
                        Prices Overview,
                        Moving Averages,
                        relative Strength Index (RSI),
                        Moving Average Convergence Divergence (MACD),
                        advice and suggestions,
                        Do I buy, sell or hold,
                        Please be as detailed as possible and explain in a way that a beginner can understand and 
                        here is the price list: {bitcoinPrices}"""

        analysis = BasicGeneration(chatGPTPrompt)
        st.text_area(" Analysis", analysis, height=500 )
        st.success('Done!')

# print(analysis)
