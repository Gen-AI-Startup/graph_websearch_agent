import argparse
import json
from agent_graph.graph import create_graph, compile_workflow


def main():
    parser = argparse.ArgumentParser(description="Run the graph websearch agent.")
    parser.add_argument("--server", help="Server to use")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--model_endpoint", help="Model endpoint to use")
    parser.add_argument("--iterations", type=int, default=40, help="Number of iterations")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--config", help="Path to the configuration file")
    parser.add_argument("--temperature", type=float, help="Temperature to use")

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r") as f:
            config = json.load(f)
        server = config["server"]
        model = config["model"]
        model_endpoint = config.get("model_endpoint", None)
        iterations = config.get("iterations", 40)
        verbose = config.get("verbose", False)
        temperature = config.get("temperature", 0)
    else:
        server = args.server
        model = args.model
        model_endpoint = args.model_endpoint
        iterations = args.iterations if args.iterations else 40
        verbose = args.verbose
        temperature = args.temperature if args.temperature else 0

    if not server or not model:
        parser.error("Either --config or both --server and --model must be provided")

    print("Creating graph and compiling workflow...")
    graph = create_graph(server=server, model=model, model_endpoint=model_endpoint, temperature=temperature)
    workflow = compile_workflow(graph)
    print("Graph and workflow created.")

    while True:
        query = input("Please enter your research question: ")
        if query.lower() == "exit":
            break

        dict_inputs = {"research_question": query}
        result = None
        limit = {"recursion_limit": iterations}
        count = 0
        try:
            for event in workflow.stream(dict_inputs, limit):
                print(count)
                count += 1
                for key, value in event.items():
                    print(f"Node: {key}")
                    # print(f"Value: {value}")
                    print("-------------------------------------------")
                    result = value
                if verbose:
                    print("\nState Dictionary:", event)
                else:
                    print("\n")
        except Exception:
            result = None
            print("Recursion limit reached. Exiting.")
        return result


if __name__ == "__main__":
    main()
