from concurrent.futures import ThreadPoolExecutor, wait
import re
import time
from typing import Any, Dict, Iterable, List, TypedDict, Union

from langchain_core.messages import BaseMessage, ToolMessage, FunctionMessage

from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import chain as as_runnables

from agent.src.output_parser import Task

def _get_observations(messages: List[BaseMessage]) -> Dict[int, Any]:
    # Get all previous tool response
    results = {}

    for message in messages[::-1]: 
        if isinstance(message, FunctionMessage):
            results[int(message.additional_kwargs["idx"])] = message.content
    return results

class SchedulerInput(TypedDict):
    messages: List[BaseMessage]
    tasks: Iterable[Task]


def _execute_task(
    task: Task,
    observations: Dict[int, Any], 
    config: RunnableConfig,
) -> Any:
    tool_to_use = task["tool"]
    if isinstance(tool_to_use, str):
        return tool_to_use
    args = task["args"]
    try:
        if isinstance(args, str):
            resolved_args = _resolve_args(args, observations)
        elif isinstance(args, dict):
            resolved_args = {
                key: _resolve_args(val, observations) for key, val in args.items()
            }
        else:
            # This will likely fail 
            resolved_args = args
    except Exception as e:
        return (
            f"Error(failed to call {tool_to_use.name} with args {args}.)",
            f"Args could not be resolved. Error {repr(e)}.",
        )
    try:
        return tool_to_use.invoke(resolved_args, config) # type: ignore # check the type later
    except Exception as e:
        return (
            f"Error(failed to call {tool_to_use.name} with args {args}.",
            f"Tool execution failed. Error {repr(e)}.",
        )
    
def _resolve_args(
        arg: Union[str, Any],
        observations: Dict[int, Any],
):
    ID_PATTERN = r"\$\{?(\d+)\}?"

    def replace_match(match):
        # If the string id ${123}, match.group(0) == ${123} and match.group(1) == 123

        # return the match group, in this case the index of the string.
        # This is the index number we get back
        idx = int(match.group(1))
        return str(observations.get(idx, match.group(0)))
    
    # For dependencies on other task
    if isinstance(arg, str):
        return re.sub(ID_PATTERN, replace_match, arg)
    elif isinstance(arg, list):
        return [_resolve_args(a, observations) for a in arg]
    else:
        return str(arg)
    

@as_runnables # type: ignore
def schedule_task(
    task_input,
    config : RunnableConfig,
):
    task: Task = task_input["tasks"]
    observations : Dict[int, Any] = task_input["observations"]
    try:
        observation = _execute_task(task, observations, config)
    except Exception:
        import traceback

        observation = traceback.format_exception() # type: ignore # repr(e)? || need to pass some args
    observations[task["idx"]] = observation

def schedule_pending_task(
    task : Task,
    observations : Dict[int, Any],
    retry_after : float = 0.2
):
    while True:
        deps = task["dependencies"]
        if (
            deps 
            and (any(dep not in observations for dep in deps))):
            time.sleep(retry_after)
            continue
        schedule_task.invoke({"tasks": task, "observations": observations})
        break

@as_runnables
def schedule_tasks(
    scheduler_input: SchedulerInput,
) -> List[FunctionMessage]:
    """Group the tasks into a DAG schedule"""
    # For streaming, we are making a few simplifying assumption:
    # 1. The LLM does not create cyclic dependencies
    # 2. That the LLM will not generate tasks with future deps
    # If this ceases to be a good assumption, you can either
    # adjust to do a proper topological sort (not-stream)
    # or use a more complicated data structure
    tasks = scheduler_input["tasks"]
    args_for_tasks = {}
    messages = scheduler_input["messages"]
    # If we are replanning, we may have call that are dependant to the previous plan.
    # Start with those
    observations = _get_observations(messages)
    task_names = {}
    originals = set(observations)
    # We assume each task inserts a unique key above to avoid race condition
    futures = []
    retry_after = 0.25 # retry after quarter of second
    with ThreadPoolExecutor() as executor: 
        for task in tasks:
            deps = task["dependencies"]
            task_names[task["idx"]] = (
                task["tool"] if isinstance(task["tool"], str) else task["tool"].name
            )
            args_for_tasks[task["idx"]] = task["args"]
            if (
                # Depends on other tasks
                deps # has dependencies
                and (dep not in observations for dep in deps) # dependencies not finish
            ):
                futures.append(
                    executor.submit(
                        schedule_pending_task, task, observations, retry_after
                    )
                )
            else:
                # No deps or all deps satisfied
                # can schedule now
                schedule_task.invoke(dict(
                   tasks=task,
                   observations=observations, 
                ))
                # futures.append(executor.submit(schedule_tasks.invoke())) # dont mind this part, will check later

        # should Finish queuing possible tasks
        # Wait for all futures to complete
        wait(futures)
    
    # Convert observation into new tool message to add to the state
    new_observation = {
        k: (task_names[k], args_for_tasks[k], observations[k])
        for k in sorted(observations.keys() - originals)
    }
    tool_messages = [
        FunctionMessage(
            name=name,
            content=str(obs),
            additional_kwargs={"idx": k, "args": task_args},            
        )
        for k, (name, task_args, obs) in new_observation.items()
    ]
    return tool_messages


        


    
