import sys
sys.path.append('../en_module_files')
import en_module as en
import re
async def send_response(message,reply):
    await en.log_conversation(message, reply)
    res = reply.split('.')
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    return res_final


async def send_response_with_LLM(message,prompt):
    prompts = [prompt]
    llm_result = en.llm_chain({"question": prompts})  
    generated_response = llm_result['text']
    generated_response = generated_response.rstrip('.;')
    await en.log_conversation(message, generated_response)
    res = generated_response.split('.')
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    return res_final

async def send_question_answer(message):
    prompts = [message]
    llm_result = en.llm_chain({"question": message})
    generated_response = llm_result['text']
    await en.log_conversation(message, generated_response)
    split_pattern = r'(?<!\d)\.(?!\d)'
    res = re.split(split_pattern, generated_response)
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    return res_final