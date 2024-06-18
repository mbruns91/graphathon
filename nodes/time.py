from pyiron_workflow import Workflow

@Workflow.wrap.as_function_node("travel_time")
def get_time(distance: float, speed: float) -> float:
    return 42.
