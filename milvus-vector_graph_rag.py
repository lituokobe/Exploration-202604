from vector_graph_rag import VectorGraphRAG

rag = VectorGraphRAG()  # reads OPENAI_API_KEY from environment

rag.add_texts([
    "Albert Einstein developed the theory of relativity.",
    "The theory of relativity revolutionized our understanding of space and time.",
    "Albert Einstein is a Jewish scientist living in Germany.",
    "Jewish people founded the country of Israel on the land of Palestine.",
    "Germany won the FIFA world cup in 2014",
    "Palestine is a Arabic country with Islamic religion.",
    "Saudi Arabia is a Arabic country with Islamic religion.",
    "Saudi Arabia represents Asia iin FIFA world cup in 2014"
])

result1 = rag.query("What are the countries in FIFA world cup in 2014?")
print(result1.answer)
print(type(result1))

result2 = rag.query("Will Albert Einstein support Palestine to reclaim the land?")
print(result2.answer)
print(result2)

result3 = rag.query("Name some Arabic countries.")
print(result3.answer)
print(result3)