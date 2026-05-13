from app.agent.graph import build_graph
from loguru import logger

def main():
    logger.info("Iniciando o agente...")
    graph = build_graph()

    file_path = input("Document path (CSV or PDF): ").strip()
    question = input("Your question: ").strip()

    result = graph.invoke({
        "question": question,
        "file_path": file_path,
        "file_type": "",
        "answer": ""
    })

    logger.success("Resposta gerada!")
    print(f"\n📄 Resposta: {result['answer']}")

if __name__ == "__main__":
    main()