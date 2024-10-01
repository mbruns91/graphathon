from pyiron_workflow import Workflow

@Workflow.wrap.as_function_node("vehicle")
def get_vehicle(vehicle: str) -> str:
    return vehicle
