"""
MongoDB Knowledge Base for Policy Compliance Monitor
Stores policy documents, regulations, and guidelines with vector embeddings
"""
import sys
import os
from typing import List, Dict, Optional, Any
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import MONGODB_URI, MONGODB_DB_NAME

class MongoPolicyKB:
    """MongoDB-based knowledge base with vector search for policy documents"""
    
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB_NAME]
        self.collection = self.db["policy_documents"]
        
        # Initialize embeddings using HuggingFace sentence transformers
        # Using all-MiniLM-L6-v2: fast, efficient, good quality embeddings
        print("[INFO] Initializing HuggingFace embeddings (all-MiniLM-L6-v2)...")
        self.embeddings = None
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("  [OK] Embeddings initialized successfully")
        except Exception as e:
            print(f"  [WARNING] Embeddings initialization failed: {e}")
            print("  Documents will be stored without embeddings.")
        
        # Initialize text splitter for document processing
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Try to initialize vector search (requires Atlas with vector search index)
        self.vector_store = None
        if self.embeddings and MONGODB_URI.startswith("mongodb+srv://"):
            try:
                self.vector_store = MongoDBAtlasVectorSearch(
                    collection=self.collection,
                    embedding=self.embeddings,
                    index_name="vector_index"
                )
                print("[OK] MongoDB Atlas vector search client initialized")
            except Exception as e:
                print(f"[WARNING] Vector search not initialized: {e}")
                print("  Falling back to local embedding/text search.")
        else:
            print("[INFO] Atlas vector index unavailable; using local embedding/text search.")
    
    def add_document(self, content: str, metadata: Dict, doc_id: str = None) -> bool:
        """Add a document to the knowledge base"""
        try:
            # Split document into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Add each chunk with embeddings
            for i, chunk in enumerate(chunks):
                doc_data = {
                    "content": chunk,
                    "metadata": metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                
                if doc_id:
                    doc_data["document_id"] = f"{doc_id}_chunk_{i}"
                
                # Generate embedding if embeddings are available
                if self.embeddings and self.vector_store:
                    try:
                        embedding = self.embeddings.embed_query(chunk)
                        doc_data["embedding"] = embedding
                    except Exception as e:
                        print(f"  [WARNING] Skipping embedding generation: {e}")
                
                # Insert into MongoDB
                self.collection.insert_one(doc_data)
            
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def semantic_search(self, query: str, k: int = 5, 
                       filter: Dict = None) -> List[Document]:
        """Perform semantic search using vector embeddings"""
        if self.vector_store:
            try:
                # Use vector search if available
                results = self.vector_store.similarity_search(
                    query, 
                    k=k,
                    pre_filter=filter
                )
                if results:
                    return results
            except Exception as e:
                print(f"Vector search failed: {e}. Falling back to text search.")

        # Fallback to local embedding similarity when Atlas vector search is unavailable
        if self.embeddings:
            embedding_results = self._embedding_search(query, k, filter)
            if embedding_results:
                return embedding_results
        
        # Fallback to text search
        return self._text_search(query, k, filter)

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Compute cosine similarity between two embedding vectors."""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return -1.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5

        if norm_a == 0 or norm_b == 0:
            return -1.0

        return dot_product / (norm_a * norm_b)

    def _embedding_search(self, query: str, k: int = 5,
                         filter: Dict = None) -> List[Document]:
        """Local embedding similarity search over stored document embeddings."""
        try:
            query_embedding = self.embeddings.embed_query(query)
        except Exception as e:
            print(f"Embedding generation failed: {e}. Falling back to text search.")
            return []

        mongo_filter = {"embedding": {"$exists": True}}
        if filter:
            mongo_filter.update(filter)

        # Scan a bounded set for relevance ranking in local/non-Atlas environments
        candidates = self.collection.find(mongo_filter).limit(1000)
        scored_docs = []

        for item in candidates:
            embedding = item.get("embedding")
            if not embedding:
                continue

            score = self._cosine_similarity(query_embedding, embedding)
            if score < 0:
                continue

            scored_docs.append((score, item))

        if not scored_docs:
            return []

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_items = scored_docs[:k]

        documents = []
        for _, result in top_items:
            documents.append(Document(
                page_content=result.get("content", ""),
                metadata=result.get("metadata", {})
            ))

        return documents
    
    def _text_search(self, query: str, k: int = 5, 
                    filter: Dict = None) -> List[Document]:
        """Fallback text-based search"""
        documents = []

        # 1) Try MongoDB text index search first
        query_filter = {"$text": {"$search": query}}
        if filter:
            query_filter.update(filter)

        try:
            results = self.collection.find(query_filter).limit(k)
            for result in results:
                documents.append(Document(
                    page_content=result.get("content", ""),
                    metadata=result.get("metadata", {})
                ))

            if documents:
                return documents
        except Exception:
            pass

        # 2) Fallback: token-based regex search on content/metadata fields
        tokens = [token for token in query.split() if len(token) > 2][:8]
        if tokens:
            regex_conditions = [
                {"content": {"$regex": token, "$options": "i"}} for token in tokens
            ] + [
                {"metadata.title": {"$regex": token, "$options": "i"}} for token in tokens
            ] + [
                {"metadata.name": {"$regex": token, "$options": "i"}} for token in tokens
            ]

            regex_filter = {"$or": regex_conditions}
            if filter:
                regex_filter.update(filter)

            results = self.collection.find(regex_filter).limit(k)
            for result in results:
                documents.append(Document(
                    page_content=result.get("content", ""),
                    metadata=result.get("metadata", {})
                ))

            if documents:
                return documents

        # 3) Final fallback: return latest documents so responses remain KB-grounded
        latest_filter = filter or {}
        results = self.collection.find(latest_filter).sort("_id", -1).limit(k)
        for result in results:
            documents.append(Document(
                page_content=result.get("content", ""),
                metadata=result.get("metadata", {})
            ))

        return documents
    
    def hybrid_search(self, query: str, k: int = 5, 
                     user_filter: Dict = None) -> List[Document]:
        """Hybrid search combining semantic and keyword search"""
        # Get semantic results
        semantic_results = self.semantic_search(query, k=k, filter=user_filter)
        
        # For now, return semantic results
        # In production, combine with keyword search and re-rank
        return semantic_results
    
    def get_by_category(self, category: str, limit: int = 10) -> List[Document]:
        """Get documents by category"""
        results = self.collection.find(
            {"metadata.category": category}
        ).limit(limit)
        
        documents = []
        for result in results:
            doc = Document(
                page_content=result.get("content", ""),
                metadata=result.get("metadata", {})
            )
            documents.append(doc)
        
        return documents
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        total_docs = self.collection.count_documents({})
        
        # Get category breakdown
        pipeline = [
            {"$group": {
                "_id": "$metadata.category",
                "count": {"$sum": 1}
            }}
        ]
        category_stats = list(self.collection.aggregate(pipeline))
        
        return {
            "total_documents": total_docs,
            "categories": {stat["_id"]: stat["count"] for stat in category_stats if stat["_id"]}
        }
    
    def delete_all(self):
        """Delete all documents (use with caution)"""
        self.collection.delete_many({})
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
    
    # ========== Policy-specific Methods ==========
    
    def add_policy_document(self, title: str, content: str, category: str,
                           organization: str, effective_date: str,
                           authority: str = "", version: str = "1.0", tags: List[str] = None) -> bool:
        """Add a policy document to the knowledge base"""
        metadata = {
            "type": "policy",
            "category": category,
            "title": title,
            "organization": organization,
            "effective_date": effective_date,
            "authority": authority,
            "version": version
        }
        
        if tags:
            metadata["tags"] = tags
        
        return self.add_document(content, metadata, doc_id=f"policy_{title[:20]}")
    
    def add_regulation(self, regulation_id: str = None, title: str = None, name: str = None, 
                      summary: str = None, content: str = None, jurisdiction: str = "",
                      authority: str = "", category: str = "", requirements: List[str] = None) -> bool:
        """Add a regulation to the knowledge base"""
        # Handle both old and new parameter names for backwards compatibility
        reg_name = title or name or regulation_id or "Unknown Regulation"
        reg_content = summary or content or ""
        
        if requirements:
            full_content = f"Regulation: {reg_name}\n\n"
            if authority:
                full_content += f"Authority: {authority}\n\n"
            if jurisdiction:
                full_content += f"Jurisdiction: {jurisdiction}\n\n"
            if category:
                full_content += f"Category: {category}\n\n"
            full_content += f"Requirements:\n" + "\n".join(f"- {req}" for req in requirements)
            full_content += f"\n\n{reg_content}"
        else:
            full_content = reg_content
        
        metadata = {
            "type": "regulation",
            "name": reg_name,
            "jurisdiction": jurisdiction
        }
        
        if category:
            metadata["category"] = category
        if authority:
            metadata["authority"] = authority
        if regulation_id:
            metadata["regulation_id"] = regulation_id
        
        return self.add_document(full_content, metadata, doc_id=f"regulation_{reg_name[:20]}")
    
    def add_guideline(self, title: str, content: str, category: str,
                     issuing_body: str = "", applicable_regulations: List[str] = None, 
                     version: str = "1.0") -> bool:
        """Add a compliance guideline to the knowledge base"""
        metadata = {
            "type": "guideline",
            "category": category,
            "title": title,
            "version": version
        }
        
        if issuing_body:
            metadata["issuing_body"] = issuing_body
        if applicable_regulations:
            metadata["applicable_regulations"] = applicable_regulations
        
        return self.add_document(content, metadata, doc_id=f"guideline_{title[:20]}")
    
    def search_policies(self, query: str, category: str = None,
                       organization: str = None) -> List[Document]:
        """Search for policy documents"""
        filter = {"metadata.type": "policy"}
        if category:
            filter["metadata.category"] = category
        if organization:
            filter["metadata.organization"] = organization
        
        return self.semantic_search(query, k=5, filter=filter)
    
    def search_regulations(self, query: str, jurisdiction: str = None) -> List[Document]:
        """Search for regulations"""
        filter = {"metadata.type": "regulation"}
        if jurisdiction:
            filter["metadata.jurisdiction"] = jurisdiction
        
        return self.semantic_search(query, k=5, filter=filter)
    
    def search_guidelines(self, category: str = None) -> List[Document]:
        """Search for compliance guidelines"""
        filter = {"metadata.type": "guideline"}
        if category:
            filter["metadata.category"] = category
        
        return self.get_by_category("guideline") if not category else self.semantic_search("", k=10, filter=filter)
