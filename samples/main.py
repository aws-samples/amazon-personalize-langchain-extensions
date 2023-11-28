from aws_langchain import AmazonPersonalizeChain
from aws_langchain import AmazonPersonalize
from langchain.llms.bedrock import Bedrock


if __name__ == "__main__":

    recommender_arn="<insert_arn>"
    user_id = '0001'

    # Create Amazon personalize client
    client = AmazonPersonalize(
        credentials_profile_name="default",
        region_name="us-west-2",
        recommender_arn=recommender_arn
    )

    input_list = ["METADATA_COL1"]
    metadataMap = {"ITEMS": input_list}

    response = client.get_recommendations(
        user_id=user_id,
        metadataColumns=metadataMap
    )

    print(response['itemList'])

    # create llm
    llm = Bedrock(model_id="anthropic.claude-v2", region_name="us-west-2")
    
    # Create personalize chain
    chain = AmazonPersonalizeChain.from_llm(
        llm=llm,
        client=client,
        return_direct=False
    )
    response = chain({'user_id': user_id, 'metadata_columns': metadataMap})
    print(response['result'])


