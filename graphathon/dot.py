import pydot
from IPython.display import SVG
from collections import defaultdict
from pathlib import Path


class EmptyGraph:
    def __init__(self, text_input):
        self.graph = pydot.graph_from_dot_data(text_input)[0]
        self.graph.set_type("digraph")

    def return_svg(self):
        return SVG(self.graph.create_svg())

    @staticmethod
    def _parse_label(label):
        label = label.strip()
        if label.startswith("\"") or label.startswith("'"):
            label = label[1:-1]
        result = {"variable": label.split(":")[0].strip()}
        if ":" in label:
            result.update({"type": label.split(":")[1].strip()})
        return result

    @staticmethod
    def _group_output_nodes(labels):
        if len(set([ll["variable"] for ll in labels])) == 1:
            return labels[0]
        v = ", ".join(list(set([ll["variable"] for ll in labels])))
        d = {"variable": v}
        if any(["type" not in ll for ll in labels]):
            return d
        t = ", ".join(list(set([ll["type"] for ll in labels])))
        d.update({"type": f"tuple[{t}]"})
        return d

    @property
    def _nodes(self):
        node_outputs = defaultdict(list)
        node_inputs = defaultdict(list)
        for edge in self.graph.get_edges():
            label = self._parse_label(edge.get_label())
            if edge.get_destination().lower() != "output":
                node_inputs[edge.get_destination()].append(label)
            if edge.get_source().lower() != "input":
                node_outputs[edge.get_source()].append(label)
        return [
            {
                "method": key,
                "input": value,
                "output": self._group_output_nodes(node_outputs[key])
            }
            for key, value in node_inputs.items()
        ]

    @staticmethod
    def _to_input_arg(label):
        if "type" in label:
            return f"{label['variable']}: {label['type']}"
        return f"{label['variable']}"

    @property
    def _node_py(self):
        for node in self._nodes:
            output_type = ""
            if "type" in node["output"]:
                output_type = f"-> {node['output']['type']}"
            input_args = ", ".join([
                self._to_input_arg(ll) for ll in node['input']
            ])
            yield {
                "method": node["method"],
                "text": (
                    "from pyiron_workflow import Workflow\n\n\n"
                    "@Workflow.wrap.as_function_node()\n"
                    f"def {node['method']}({input_args}) {output_type}:\n"
                    f"    return {node['output']['variable']}\n"
                )
            }

    def _get_init(self, directory="nodes"):
        directory = directory.replace("\\", "/").replace("/", ".")
        return "\n".join([
            f"from {directory}.{node['method']} import {node['method']}"
            for node in self._nodes
        ])

    def export(self, directory="nodes"):
        for node in self._node_py:
            with open(Path(directory) / Path(node["method"] + ".py"), "w") as f:
                f.write(node["text"])
        with open("__init__.py", "w") as f:
            f.write(self._get_init(directory=directory))
