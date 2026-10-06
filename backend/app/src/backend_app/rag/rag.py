import json
import os
from pathlib import Path
from typing import Any

import bm25s
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int


class Rag:
    def __init__(self):
        self.indexed = False
        self.cached_chunks = None
        self.index_files("/app/src/backend_app/rag/dataset/")
    
    def chunk_file(self, path: str, corpus: list[str], index_map: dict[str, dict[str, Any]], chunk_size: int = 2000) -> None:
        if "." not in path:
            raise Exception(f"Invalid/Unknown file extension: {path}") # noqa: TRY002
        ext = path.split(".")[-1].lower()
        if ext not in ["md", "txt"]:
            return
        try:
            with open(path, "r") as f:
                text = f.read()
            start_idx = len(corpus)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=int(0.1 * chunk_size),
                add_start_index=True,
            )
            docs = splitter.create_documents([text])
            index_map[path] = {
                "start": start_idx,
                "end": start_idx + len(docs),
                "chunks": [],
            }
            for _, doc in enumerate(docs):
                start_char = doc.metadata.get("start_index", 0)
                corpus += [doc.page_content]
                index_map[path]["chunks"].append(
                    {
                        "start": start_char,
                        "end": start_char + len(doc.page_content),
                    }
                )
        except Exception as e: # noqa: BLE001
            raise Exception(f"Could not open file: '{path}', reason: {e}") # noqa: TRY002


    def gather_files(self, path: str) -> list[str]:
        files = []
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                files.append(full_path)
        return files

    def index_files(self, path: str, chunk_size: int = 2000) -> None:
        output_dir = "data/processed/bm25_index"
        corpus: list[str] = []
        index_map: dict[str, dict[str, Any]] = {}

        if not os.access(path, 0):
            raise Exception("Could not find DataSet path") # noqa: TRY002

        files = self.gather_files(path)
        for file_path in files:
            self.chunk_file(file_path, corpus, index_map, chunk_size)

        corpus_tokens = bm25s.tokenize(corpus)
        retriever = bm25s.BM25(corpus=corpus)
        retriever.index(corpus_tokens)
        retriever.save(output_dir)

        Path("./data/processed/chunks/chunks.json").parent.mkdir(parents=True, exist_ok=True)
        try:
            with open("./data/processed/chunks/chunks.json", "w") as f:
                json.dump(index_map, f, indent=4)
        except Exception: # noqa: BLE001
            raise Exception("Could not write chunks manifest") # noqa: TRY002

        print(f"\nIngestion complete! Indices saved under {output_dir}")
        self.indexed = True


    def retrieve_chunks(self, query: str, found_files: list[MinimalSource], k: int = 3) -> list[str]:
        try:
            retriever = bm25s.BM25.load("data/processed/bm25_index", load_corpus=True)
            query_tokens = bm25s.tokenize(query)
            docs, _ = retriever.retrieve(query_tokens, k=k)
            chunks_ids = []
            if self.cached_chunks:
                data = self.cached_chunks
            else:
                with open("./data/processed/chunks/chunks.json") as f:
                    data = json.load(f)
                    self.cached_chunks = data

            for path, d in data.items():
                start = d.get("start", 0)
                end = d.get("end", 0)
                for chunk_id in [chunk["id"] for chunk in docs[0] if chunk["id"] not in chunks_ids]:
                    if start <= chunk_id < end:
                        chunk_indexes = d.get("chunks", [])[chunk_id - start]
                        relative_start = chunk_indexes.get("start", 0)
                        relative_end = chunk_indexes.get("end", 0)
                        found_files.append(
                            MinimalSource(
                                file_path=path,
                                first_character_index=relative_start,
                                last_character_index=relative_end,
                            )
                        )
                        chunks_ids.append(chunk_id)
            return [doc["text"] for doc in docs[0]]
        except Exception as e: # noqa: BLE001
            raise Exception(f"Could not find indexed chunks, please index before: \n{e}") # noqa: TRY002