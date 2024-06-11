from pyiron_workflow import Workflow

@Workflow.wrap.as_function_node()
def get_distance(start: str, end: str, vehicle: str) -> float:
    distance = 100.
    return distance
