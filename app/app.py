import argparse
import json
from agent_graph.graph import create_graph, compile_workflow


def main():
    parser = argparse.ArgumentParser(description="Run the graph websearch agent.")
    parser.add_argument("--server", help="Server to use")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--model_endpoint", help="Model endpoint to use")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations")
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
        iterations = config.get("iterations", 100)
        verbose = config.get("verbose", False)
        temperature = config.get("temperature", 0)
    else:
        server = args.server
        model = args.model
        model_endpoint = args.model_endpoint
        iterations = args.iterations if args.iterations else 100
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
        limit = {"recursion_limit": iterations}

        for event in workflow.stream(dict_inputs, limit):
            if verbose:
                print("\nState Dictionary:", event)
            else:
                print("\n")


if __name__ == "__main__":
    main()
