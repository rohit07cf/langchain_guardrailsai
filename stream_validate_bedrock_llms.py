import boto3, os
import asyncio
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.bedrock import BedrockChat

import guardrails as gd
from guardrails.hub import CompetitorCheck


competitors_list = ["Nvidia","Apple"] 
guard = gd.Guard().use(CompetitorCheck,competitors_list,stream=True)

load_dotenv()

# Store your keys in env variables


client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = 'us-east-1',
)

# get the model id here : https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
model_kwargs = {
    "max_tokens": 512,
    "temperature": 0.0,
    "top_p": 1,
    "top_k": 1,
}

llm_bedrock = BedrockChat(
    client=client,
    model_id=model_id,
    model_kwargs=model_kwargs,
    streaming=True
)

template = '''
    {question}
'''

prompt = PromptTemplate(input_variables=['question'], template=template)


async def getResult():
    print("Reached getResult()")
    print("Defined chain")
    chain = prompt | llm_bedrock | guard.to_runnable() | StrOutputParser()
    try:
        print("Run the chain async")
        result_string=""
        result = await chain.ainvoke({"question": "Can you provide some information on Microsoft!"})
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
