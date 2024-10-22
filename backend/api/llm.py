import openai
import io
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
import time
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter

from task_assets import TASK_ASSETS

def create_chain_from_task_asset(task_asset, openai_key):
    """
    Converts a task_asset dictionary into a chain.

    Parameters:
    - task_asset (dict): A dictionary containing the keys 'prompt', 'model', 'temperature', 'max_tokens', and 'json_schema'.

    Returns:
    - A chain that can be invoked with the appropriate input.
    """
    
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', task_asset['task']),
        ('user', task_asset['prompt'])
    ])
    
    llm = ChatOpenAI(   
        model=task_asset.get('model', 'gpt-4o'),
        temperature=task_asset.get('temperature', 0.0),
        max_tokens=task_asset.get('max_tokens', 1024),
        openai_api_key=openai_key,
    )

    if 'json_schema' in task_asset:
        llm = llm.with_structured_output(task_asset['json_schema'])
    
    return prompt_template | llm

extraction_chain = create_chain_from_task_asset(
    TASK_ASSETS['ux_research_interview_analysis'], 
    os.environ['OPENAI_API_KEY']
)

summary_chain = create_chain_from_task_asset(
    TASK_ASSETS['ux_research_interview_analysis_summary'], 
    os.environ['OPENAI_API_KEY']
)
    

if __name__ == '__main__':
    dummy_transcript = '''
    ezd-rxwj-zoo (2024-10-21 13:38 GMT-4) - Transcript
Attendees
Alex, Jordan
Transcript
Alex: Hey, thanks so much for taking the time to chat today! I'm working on a new project to help people adopt pets, and I'm really curious about your experiences running your Instagram account. Can you tell me a bit about what motivated you to start it?
Jordan: Of course! I started the account about two years ago. I'm really passionate about helping pets find their forever homes, and Instagram felt like a great platform to connect with potential adopters and showcase pets from local shelters.
Alex: That's awesome! Have you noticed any particular challenges for people trying to adopt pets through the posts you share? Like, are there common pain points you hear about from your followers?
Jordan: Definitely. I'd say one of the biggest issues is the lack of information. People will fall in love with a pet I post, but then they have trouble getting in touch with the shelter or figuring out the adoption process. A lot of times, the shelters don't have updated websites, or the adoption requirements aren't clear.
Alex: That's really interesting. So, do you think there's a disconnect between the shelters and potential adopters when it comes to communication?
Jordan: For sure. And it's frustrating for both sides. I've had followers message me saying they tried to call the shelter but didn't hear back, or they didn't know what documents they needed for adoption. It's a big barrier when people are excited but can't get clear answers quickly.
Alex: Yeah, I can see how that would discourage someone from adopting. Have you seen any tools or platforms that help with this, or is it mostly people just trying to navigate it themselves?
Jordan: I've seen a few apps and websites, but none that really solve the problem well. They either focus on listing pets without offering much info about the adoption process, or they don't integrate well with shelters. A lot of it is still manual—people DM me to ask questions, and I end up acting like a go-between sometimes.
Alex: It sounds like there's a real need for a better system to bridge that gap! Do you think an app that helps streamline communication between shelters and adopters would be helpful? Maybe something that has up-to-date info on pets, plus clear adoption steps?
Jordan: That could be super useful! Especially if it could make things more transparent, like showing what the next steps are, what's required, or even helping people book appointments directly with the shelter. I think it would make the process a lot less stressful for both adopters and the shelters themselves.
Alex: That's great feedback. It sounds like simplifying that communication and making the process more user-friendly could really make a difference. Thanks so much for sharing all this—it's exactly the kind of insight I was hoping for!
Jordan: Glad I could help! I'm excited to see what you come up with. If you need any more input, feel free to reach out.
Alex: Will do, thanks again!
Meeting ended after 00:21:00
This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
    '''
    extraction_output = extraction_chain.invoke({'transcript': dummy_transcript})
    summary_output = summary_chain.invoke({'transcript': dummy_transcript})

    print(extraction_output)
    print(summary_output)