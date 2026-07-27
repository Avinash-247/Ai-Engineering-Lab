import hashlib

from langchain_core.documents import Document
from langchain_core.indexing import index
from langchain_classic.indexes import SQLRecordManager
from langchain_chroma import Chroma
from langchain_core.embeddings import DeterministicFakeEmbedding

def strategy_1_full_reindex(embeddings,all_documents, collection_name="rag_Full"):
    store= Chroma(
        collection_name=collection_name,
        embedding_function=embeddings
    )
    try:
        store.delete_collection()
    except Exception:
        pass

    store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings
    )
    store.add_documents(all_documents)
    return store

def stable_id(doc :Document)->str:
    return f"{doc.metadata['source']}: {doc.metadata['chunk_index']}"
def content_hash(doc:Document)-> str:
    return hashlib.sha256(doc.page_content.encode()).hexdigest()

def strategy_2_incremental_upsert(
        store : Chroma,
        new_documents: list[Document]):

    sources ={doc.metadata["source"] for doc in new_documents}
    existing=store.get(where={"source":{"$in": list(sources)}})
    existing_hashes={
        _id: meta.get("content_hash")
        for _id, meta.get in zip(existing["ids"],existing["metadatas"])
    }
    to_upsert,upsert_ids=[],[]
    new_ids =set()
    for doc in new_documents:
        _id =stable_id(doc)
        new_ids.add(_id)
        new_hash =content_hash(doc)
        doc.metadata['content_hash']=new_hash
        if existing_hashes.get(_id) !=new_hash:
            to_upsert.append(doc)
            upsert_ids.append(_id)
    if to_upsert:
        store.add_documents(to_upsert,ids=upsert_ids)

    stable =[i for i in existing_hashes if i not in new_ids]
    if stable :
        store.delete(stable)
    return {"upserted": len(to_upsert), "deleted":len(ids=stable)}

def strategy_3_record_manager(
        embeddings,
        documents,
        namespace="chroma/rag_managed",
        collection_name="rag_managed",
        db_url="sqlite:///rag_record_namaner.db",
        cleanup="full"):
    record_manager=SQLRecordManager(namespace,db_url=db_url)
    store=Chroma(
        collection_name=collection_name,
        embedding_function=embeddings
    )
    record_manager.create_schema()
    result=index(
        documents,
        record_manager,
        store,
        cleanup=cleanup,
        source_id_key="source",
        key_encoder="sha256"

    )
    return store, result
if __name__=="__main__":
    embedding=DeterministicFakeEmbedding(size=32)
    doc_v1=[
        Document(
            page_content="photosynthesis converts light to energy",
            metadata={"source":"biology","page": 11}
        ),
        Document(
            page_content="triangle have three sides",
            metadata={"source":"Math","page": 15}
        )
    ]

    store,r1=strategy_3_record_manager(
        embeddings=embedding,
        documents=doc_v1,
    )

    print("first index:", r1)

    _,r2=strategy_3_record_manager(
        embeddings=embedding,
        documents=doc_v1,
        db_url="sqlite:///demo_rm.db"
    )

    print(" reindex identical:", r2)

    docs_v2=[
        Document(
            page_content="photosynthesis converts sunlight to chemical energy",
            metadata={"source": "biology", "page" : 11}),

        Document(
            page_content="triangle have three  slides",
            metadata={"source" : "geomentry","page":5}
        )
    ]

    _, r3=strategy_3_record_manager(
        embeddings=embedding,
        documents=docs_v2,
        db_url="sqlite:///demo_rm.db"
    )

    print("Handle changes:", r3)

    