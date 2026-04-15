**Summary of Our Discussion on GraphRAG (as of April 2026)**

GraphRAG is Microsoft’s graph-enhanced version of Retrieval-Augmented Generation. Instead of just pulling similar text chunks like traditional (“naive” or vector) RAG, it first uses an LLM to extract entities, relationships, and claims from the corpus, builds a structured **knowledge graph**, runs community detection (Leiden algorithm) to create hierarchical clusters of related concepts, and has the LLM pre-write summaries of those communities at multiple levels. At query time it supports **global search** (big-picture synthesis using community summaries), **local search** (entity-focused graph traversal), and hybrids like DRIFT.

### Specialties Compared to Traditional Vector RAG
Traditional RAG relies on embedding chunks and doing top-k semantic similarity search. GraphRAG adds a **structured relational layer** on top:

- It excels at **multi-hop reasoning** and understanding connections across the entire dataset, not just isolated similar chunks.
- It pre-computes hierarchical summaries so the LLM can “see” the big picture without having to synthesize everything on-the-fly.
- Retrieval is **hybrid**: vector embeddings provide the initial “seed” entities (for speed), then graph traversal walks nodes/edges and pulls the original text units for rich context.
- Storage: graph data (nodes, edges, communities, text units) lives in efficient **Parquet files**; a lightweight **vector store** (LanceDB by default) holds only embeddings for fast semantic lookup. No full live graph database is required unless you export it.

This makes GraphRAG far better at questions that need relationships, causality, or holistic understanding, while traditional RAG is simpler and faster for single-fact lookups.

### Pros and Cons (from our discussion)
**Pros**:
- Significantly stronger on **global / multi-hop / relational questions** — produces more comprehensive, diverse, and coherent answers.
- Highly **explainable** — you can trace results back through graph paths and community reports.
- Excellent for unstructured or narrative private/enterprise data where traditional RAG loses context.
- Incremental updates are supported (add/delete/revise documents without a full rebuild, though some affected community summaries may refresh).

**Cons**:
- **Computationally expensive to build** — indexing requires multiple LLM passes (entity/relationship extraction + hierarchical summarization), so it costs more time and money than vector RAG’s single embedding pass.
- More complex to set up, tune prompts, and maintain.
- Still uses embeddings and a vector store underneath, so it’s a hybrid system rather than pure graph.
- For very simple factual or pure-calculation questions, the extra graph layer can add unnecessary overhead (traditional RAG is often sufficient and cheaper).
- Data changes trigger partial rebuilds of affected communities — not as trivial as a single upsert in vector RAG.

### Best Use Cases
GraphRAG shines when you need the LLM to act as a true “sensemaker” over a large, previously unseen corpus. Top scenarios we covered:

- **Enterprise knowledge bases** or private document collections where questions involve themes, trends, causal chains, or comparisons across many documents.
- **Research / scientific analysis** — e.g., synthesizing findings from papers or reports.
- **Narrative or unstructured data** — legal contracts, news archives, supply-chain reports, internal wikis.
- **Multi-hop or “global” queries** — “What are the key risk factors and how do they interconnect?” or “How does Product A compare to Product B across all regions and years?”
- **Hybrid setups** — use GraphRAG for the stable core knowledge and layer fast vector RAG for frequently changing fresh data.

It is **not** the best choice for:
- High-velocity, rapidly changing data (where pure vector RAG or simple vector stores win on cost/speed).
- Pure arithmetic calculations or single-fact lookups (traditional RAG or even no-RAG + tool calling is lighter).

**Bottom line from our conversation**: Traditional RAG is the quick, cheap, go-to tool for most everyday semantic search. GraphRAG is the more powerful (but heavier) upgrade when you need the LLM to deeply understand relationships and synthesize the “big picture” across your data. Many real-world systems today combine both.


In official Microsoft GraphRAG (as of April 2026):

- **The vector database (LanceDB by default) does *not* keep the detailed data.**  
  It stores **only embeddings** (vector representations) plus IDs and minimal metadata.  
  Specifically, it holds embeddings for:
  - Entity descriptions
  - Text unit content (the chunks)
  - Community report summaries  
  (and sometimes relationship descriptions).  

  Its size is **much smaller** than a typical traditional RAG vector database because it contains **no raw text** — just the vectors themselves.

- **The Parquet files (the “graph storage” layer) hold almost everything else, including the detailed content.**  
  This is where the bulk of the data lives:
  - `text_units.parquet` → contains the **full raw text of every chunk** (exactly like the chunks in traditional RAG).
  - `entities.parquet`, `relationships.parquet` → nodes, edges, plus rich descriptions.
  - `community_reports.parquet` → the LLM-generated hierarchical summaries.
  - Other metadata tables.

  So the Parquet layer is **larger** (it stores the actual text + structured graph data), while the vector store is the lightweight one used only for fast semantic seeding.

### Quick size comparison to traditional RAG
| Component              | Traditional Vector RAG                  | GraphRAG                                      | Relative size in GraphRAG |
|------------------------|-----------------------------------------|-----------------------------------------------|---------------------------|
| **Detailed content**  | Usually stored in the vector DB (or separate file/DB) | Stored in Parquet (`text_units.parquet`)     | Larger (Parquet)         |
| **Embeddings only**   | Main content of the vector DB          | Stored in LanceDB (entities + text units + communities) | Smaller (vector store)   |
| **Graph structure**   | None                                   | Nodes, edges, communities in Parquet         | Extra (but compact)      |

**Bottom line**: The vector store in GraphRAG is *smaller* and more specialized than a traditional RAG vector DB (because it skips the raw text). The Parquet files do the heavy lifting of storing the actual data and the graph. This design saves a lot of disk space compared to earlier GraphRAG versions (embeddings were moved out of Parquet in 2024–2025).