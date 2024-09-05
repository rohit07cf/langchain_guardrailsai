import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

os.environ['OPENAI_API_KEY']==''

model = ChatOpenAI(model="gpt-4", base_url='http://127.0.0.1:8000/guards/gibberish_guard/openai/v1')
prompt = ChatPromptTemplate.from_template("{question}")
output_parser = StrOutputParser()

async def getResult():
    print("Reached getResult()")
    print("Defined chain")
    chain = prompt | model | output_parser
    try:
        print("Run the chain async")
        result_string=""
        result = await chain.ainvoke({"question": "Make up some gibberish for me please!"})
        for chunk in result:
            result_string += f"{chunk}"
        print(result_string)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(getResult())
