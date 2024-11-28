import guardrails as gd
from guardrails.hub import CompetitorCheck


competitors_list = ["Nvidia","Apple"] 
guard = gd.Guard().use(CompetitorCheck,competitors_list,stream=True)

llm_azure = AzureChatOpenAI(azure_endpoint="",api_version="",model="gpt-4o-mini-2",temperature=0,api_key="")

template = '''
    {question}
'''
prompt = PromptTemplate(input_variables=['question'], template=template)


async def getResult():
    print("Reached getResult()")
    print("Defined chain")
    chain = prompt | llm_azure | guard.to_runnable() | StrOutputParser()
    try:
        print("Run the chain async")
        result_string=""
        result = await chain.ainvoke({"question": "Can you provide some information on Pfizer!"})
        for chunk in result:
            result_string += f"{chunk}"
        print(result_string)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(getResult())
    error_spans = guard.error_spans_in_output()
    print("===========================ERROR SPANS====================================")
    print(error_spans)
    #print(type(guard.history[0].iteration[0].outputs))
    #print(guard.history[0].iteration[0].outputs.validator_logs[0].validation_result.error_spans)
    print("==================================================================")
