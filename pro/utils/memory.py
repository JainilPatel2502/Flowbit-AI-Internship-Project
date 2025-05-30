import redis
from langchain.memory import RedisEntityStore
from langchain.schema.runnable import RunnableLambda
import time
import json
redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)

# Entity store for memory
entity_store = RedisEntityStore(redis_client=redis_client)

def get_memory_fn(inputs: dict) -> dict:
    email_id = inputs["email"]
    new_input = inputs["data"]

    raw = entity_store.get(email_id)
    history_json = []
    history_text_lines = []

    if raw:
        history_json = json.loads(raw)
        for h in history_json:
            line = "User: " + h["input"] + "\nAssistant: " + str(h["output"])
            history_text_lines.append(line)

    history_text = "\n".join(history_text_lines)
    print("history read")
    return {
        "email": email_id,
        "input": new_input,
        "history": history_text,
        "raw_history": history_json
    }



get_memory = RunnableLambda(get_memory_fn)

def set_memory_fn(inputs: dict) -> dict:
    output = inputs["output"]
    if hasattr(output, "dict"):
        output = output.dict()

    new_entry = {
        "input": inputs["input"],
        "output": output,
        "timestamp": time.time()
    }

    raw_history = inputs["raw_history"]
    raw_history.append(new_entry)

    entity_store.set(inputs["email"], json.dumps(raw_history))
    print("Memory written")
    print(raw_history)
    return output

set_memory = RunnableLambda(set_memory_fn)