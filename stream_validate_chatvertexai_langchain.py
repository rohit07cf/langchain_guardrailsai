import asyncio
import guardrails as gd
from google.cloud import aiplatform
from guardrails.hub import CompetitorCheck
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

aiplatform.init(project="", location="")

model = ChatVertexAI(
    model_name="gemini-1.5-flash-001",
    streaming=True
)

competitors_list = ["Nvidia","Apple"]
guard = gd.Guard().use(CompetitorCheck,competitors_list,stream=True)
prompt = ChatPromptTemplate.from_template("{question}")
output_parser = StrOutputParser()

async def getResult():
    print("REACHED getResult")

    print("Defined chain: Convert a Guard to a LangChain Runnable.")
    chain = prompt | model | guard.to_runnable() | output_parser

    try:
        print("Run the chain asynchronously")
        result_string = ""
        result = await chain.ainvoke({"question":"Could you share some information on Pfizer and Moderna"})
        print(result)
        async for chunk in result:
            print("==============CHUNK===============")
            print(f"========> {chunk}")
            result_string += f"{chunk}"
        print(result_string)
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    asyncio.run(getResult())
    error_spans = guard.error_spans_in_output()
    print("===========================ERROR SPANS====================================")
    print(error_spans)
    #print(type(guard.history[0].iteration[0].outputs))
    #print(guard.history[0].iteration[0].outputs.validator_logs[0].validation_result.error_spans)
    print("==================================================================")