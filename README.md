# Amazon Personalize Langchain Extensions
This repo provides a set of utility classes to work with [Langchain](https://github.com/hwchase17/langchain/tree/master). It currently has a utility class `AmazonPersonalize` for working with a Amazon Personalize campaign/recommender and `AmazonPersonalizeChain` custom chain build to retrieve recommendations from Amazon Personalize and execute a default prompt (which can be overriden by the user).

## Installing

Clone the repository
```bash
git clone https://github.com/aws-samples/amazon-personalize-langchain-extensions.git
```

Move to the repo dir
```bash
cd amazon-personalize-langchain-extensions
```


Install the classes
```bash
pip install .
```

## Usage

### [Use-case-1] Setup Amazon Personalize Client and invoke Personalize Chain for summarizing results

```python
from aws_langchain import AmazonPersonalize

recommender_arn="<insert_arn>"

client=AmazonPersonalize(credentials_profile_name="default",region_name="us-west-2",recommender_arn=recommender_arn)
client.get_recommendations(user_id="1")
```

### [Use-case-2] Setup Amazon Personalize Client and invoke Personalize Chain for summarizing results

```python
from aws_langchain import AmazonPersonalize
from aws_langchain import AmazonPersonalizeChain
from langchain.llms.bedrock import Bedrock

recommender_arn="<insert_arn>"

bedrock_llm = Bedrock(model_id="anthropic.claude-v2", region_name="us-west-2")
client=AmazonPersonalize(credentials_profile_name="default",region_name="us-west-2",recommender_arn=recommender_arn)
# Create personalize chain
# Use return_direct=True if you do not want summary
chain = AmazonPersonalizeChain.from_llm(
    llm=bedrock_llm, 
    client=client,
    return_direct=False 
)
response = chain({'user_id': '1'})
print(response)
```

### [Use-Case-3] Invoke Amazon Personalize Chain using your own prompt

```python
from langchain.prompts.prompt import PromptTemplate
from aws_langchain import AmazonPersonalize
from aws_langchain import AmazonPersonalizeChain
from langchain.llms.bedrock import Bedrock

RANDOM_PROMPT_QUERY="""
You are a skilled publicist. Write a high-converting marketing email advertising several movies available in a video-on-demand streaming platform next week, 
    given the movie and user information below. Your email will leverage the power of storytelling and persuasive language. 
    The movies to recommend and their information is contained in the <movie> tag. 
    All movies in the <movie> tag must be recommended. Give a summary of the movies and why the human should watch them. 
    Put the email between <email> tags.

    <movie>
    {result} 
    </movie>

    Assistant:
    """

RANDOM_PROMPT = PromptTemplate(input_variables=["result"], template=RANDOM_PROMPT_QUERY)


recommender_arn="<insert_arn>"

bedrock_llm = Bedrock(model_id="anthropic.claude-v2", region_name="us-west-2")
client=AmazonPersonalize(credentials_profile_name="default",region_name="us-west-2",recommender_arn=recommender_arn)

chain=AmazonPersonalizeChain.from_llm(llm=bedrock_llm, client=client, return_direct=False, prompt_template=RANDOM_PROMPT)
chain.run({'user_id':'1', 'item_id':'234'})
```
### [Use-case-4] Invoke Amazon Personalize in a Sequential Chain 

```python
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from aws_langchain import AmazonPersonalize
from aws_langchain import AmazonPersonalizeChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts.prompt import PromptTemplate

RANDOM_PROMPT_QUERY_2="""
You are a skilled publicist. Write a high-converting marketing email advertising several movies available in a video-on-demand streaming platform next week, 
    given the movie and user information below. Your email will leverage the power of storytelling and persuasive language. 
    You want the email to impress the user, so make it appealing to them.
    The movies to recommend and their information is contained in the <movie> tag. 
    All movies in the <movie> tag must be recommended. Give a summary of the movies and why the human should watch them. 
    Put the email between <email> tags.

    <movie>
    {result}
    </movie>

    Assistant:
    """

recommender_arn="<insert_arn>"

bedrock_llm = Bedrock(model_id="anthropic.claude-v2", region_name="us-west-2")
client=AmazonPersonalize(credentials_profile_name="default",region_name="us-west-2",recommender_arn=recommender_arn)

RANDOM_PROMPT_2 = PromptTemplate(input_variables=["result"], template=RANDOM_PROMPT_QUERY_2)
personalize_chain_instance=AmazonPersonalizeChain.from_llm(llm=bedrock_llm, client=client, return_direct=True)
random_chain_instance = LLMChain(llm=bedrock_llm, prompt=RANDOM_PROMPT_2)
overall_chain = SequentialChain(chains=[personalize_chain_instance, random_chain_instance], input_variables=["user_id"], verbose=True)
overall_chain.run({'user_id':'1', 'item_id':'234'})
```

## Uninstall
```bash
pip uninstall aws-langchain
```

## Contributing
Create your GitHub branch and make a pull request.
See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License
This library is licensed under the MIT-0 License. See the LICENSE file.

