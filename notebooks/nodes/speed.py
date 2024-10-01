from pyiron_workflow import Workflow

@Workflow.wrap.as_function_node("speed")
def get_speed(vehicle: str) -> float:
    return 60.
