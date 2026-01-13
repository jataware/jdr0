import json
from vertexai.generative_models import FunctionDeclaration

from .search import *
from .scrape import *
from .arxiv import *

# --
# Wrapper class

def _fix_keys(x):
    return {(k if k != 'type_' else 'type') : (_fix_keys(v) if isinstance(v, dict) else v) for k, v in x.items()}

def _function_to_dict(fn):
    _function = _fix_keys(FunctionDeclaration.from_func(fn).to_dict())
    assert _function['parameters']['type'] == 'OBJECT'
    _function['parameters']['type'] = 'object'
    return {
        "type"        : "function",
        "function"    : _function,
    }

def _recursive_lowercase(x):
    """ some LLMs are case-sensitive, so we lowercase everything """
    if isinstance(x, dict):
        return {k.lower() : _recursive_lowercase(v) for k, v in x.items()}
    elif isinstance(x, list):
        return [_recursive_lowercase(v) for v in x]
    else:
        return x.lower()

class ToolBox:
    def __init__(self, tools, force_lowercase=False):
        self.tools = tools
        self.sigs  = [_function_to_dict(tool) for tool in tools.values()]
        if force_lowercase:
            self.sigs = _recursive_lowercase(self.sigs)
    
    async def arun(self, tool_call):
        assert tool_call["type"] == "function"
        tool_name   = tool_call.function.name
        tool_args   = json.loads(tool_call.function.arguments)
        tool_result = await self.tools[tool_name](**tool_args)
        if not isinstance(tool_result, str):
            tool_result = tool_result.to_txt()
        
        assert isinstance(tool_result, str), f"Tool {tool_name} returned {type(tool_result)}"
        
        return {
            "role"          : "tool",
            "name"          : tool_call.function.name,
            "tool_call_id"  : tool_call.id,
            "content"       : tool_result
        }