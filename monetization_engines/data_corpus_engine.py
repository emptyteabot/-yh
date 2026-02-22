"""
执行1：结构化行业语料库生成器 (Data as a Service)
目标客户：开发垂直领域RAG和微调模型的AI团队
定价：$500-$2000/库
"""

import asyncio
import json
import re
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import hashlib

class DataCorpusEngine:
    """
    高价值行业数据抓取、清洗、向量化预处理引擎
    """
    
    def __init__(self, output_dir: str = "./data_products"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 高价值行业目标
        self.target_industries = {
            "medical_compliance": {
                "价值": "$2000/库",
                "数据源": [
                    "FDA公告",
                    "医疗器械注册文档",
                    "临床试验报告",
                    "药品说明书"
                ],
                "痛点": "医疗AI需要合规数据训练，但数据分散且格式混乱"
            },
            "legal_cases": {
                "价值": "$1500/库",
                "数据源": [
                    "法院判决书",
                    "法律法规",
                    "律师函模板",
                    "合同范本"
                ],
                "痛点": "法律AI需要案例数据，但爬取和结构化极其困难"
            },
            "financial_reports": {
                "价值": "$1000/库",
                "数据源": [
                    "上市公司财报",
                    "券商研报",
                    "行业分析报告",
                    "宏观经济数据"
                ],
                "痛点": "金融AI需要专业数据，但Bloomberg太贵"
            },
            "technical_docs": {
                "价值": "$800/库",
                "数据源": [
                    "API文档",
                    "技术白皮书",
                    "开源项目文档",
                    "Stack Overflow精选"
                ],
                "痛点": "代码助手需要高质量技术文档训练"
            }
        }
    
    async def crawl_industry_data(self, industry: str, max_docs: int = 10000) -> List[Dict]:
        """
        爬取特定行业数据
        """
        print(f"[数据抓取] 开始爬取 {industry} 行业数据...")
        
        # 模拟爬取逻辑（实际需要接入你的OpenClaw系统）
        raw_data = []
        
        if industry == "medical_compliance":
            raw_data = await self._crawl_fda_data(max_docs)
        elif industry == "legal_cases":
            raw_data = await self._crawl_legal_data(max_docs)
        elif industry == "financial_reports":
            raw_data = await self._crawl_financial_data(max_docs)
        elif industry == "technical_docs":
            raw_data = await self._crawl_technical_data(max_docs)
        
        print(f"[数据抓取] 完成，共抓取 {len(raw_data)} 条原始数据")
        return raw_data
    
    async def _crawl_fda_data(self, max_docs: int) -> List[Dict]:
        """爬取FDA数据（示例）"""
        # 实际实现：调用OpenClaw爬取FDA网站
        return [
            {
                "url": f"https://www.fda.gov/doc_{i}",
                "title": f"FDA Compliance Document {i}",
                "content": f"Sample FDA compliance content {i}...",
                "date": "2024-01-01",
                "category": "medical_device"
            }
            for i in range(min(100, max_docs))  # 示例数据
        ]
    
    async def _crawl_legal_data(self, max_docs: int) -> List[Dict]:
        """爬取法律数据（示例）"""
        return [
            {
                "url": f"https://court.gov/case_{i}",
                "title": f"判决书 {i}",
                "content": f"案件详情 {i}...",
                "date": "2024-01-01",
                "category": "civil_case"
            }
            for i in range(min(100, max_docs))
        ]
    
    async def _crawl_financial_data(self, max_docs: int) -> List[Dict]:
        """爬取金融数据（示例）"""
        return [
            {
                "url": f"https://finance.com/report_{i}",
                "title": f"研报 {i}",
                "content": f"分析内容 {i}...",
                "date": "2024-01-01",
                "category": "research_report"
            }
            for i in range(min(100, max_docs))
        ]
    
    async def _crawl_technical_data(self, max_docs: int) -> List[Dict]:
        """爬取技术文档（示例）"""
        return [
            {
                "url": f"https://docs.example.com/api_{i}",
                "title": f"API Documentation {i}",
                "content": f"Technical content {i}...",
                "date": "2024-01-01",
                "category": "api_docs"
            }
            for i in range(min(100, max_docs))
        ]
    
    def clean_and_structure(self, raw_data: List[Dict]) -> List[Dict]:
        """
        数据清洗和结构化
        这是核心价值：AI团队最痛恨的脏活
        """
        print(f"[数据清洗] 开始清洗 {len(raw_data)} 条数据...")
        
        cleaned_data = []
        for item in raw_data:
            cleaned = {
                "id": self._generate_id(item),
                "title": self._clean_text(item.get("title", "")),
                "content": self._clean_text(item.get("content", "")),
                "metadata": {
                    "source_url": item.get("url", ""),
                    "date": item.get("date", ""),
                    "category": item.get("category", ""),
                    "word_count": len(item.get("content", "").split()),
                    "quality_score": self._calculate_quality_score(item)
                },
                "processed_at": datetime.now().isoformat()
            }
            
            # 只保留高质量数据
            if cleaned["metadata"]["quality_score"] > 0.6:
                cleaned_data.append(cleaned)
        
        print(f"[数据清洗] 完成，保留 {len(cleaned_data)} 条高质量数据")
        return cleaned_data
    
    def _generate_id(self, item: Dict) -> str:
        """生成唯一ID"""
        content = f"{item.get('url', '')}{item.get('title', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _clean_text(self, text: str) -> str:
        """文本清洗"""
        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()（）。，！？；：]', '', text)
        return text.strip()
    
    def _calculate_quality_score(self, item: Dict) -> float:
        """计算数据质量分数"""
        score = 0.0
        content = item.get("content", "")
        
        # 长度检查
        if len(content) > 100:
            score += 0.3
        
        # 结构化程度
        if item.get("title") and item.get("date"):
            score += 0.2
        
        # 内容丰富度
        if len(content.split()) > 50:
            score += 0.3
        
        # 来源可靠性
        if any(domain in item.get("url", "") for domain in ["gov", "edu", "org"]):
            score += 0.2
        
        return min(score, 1.0)
    
    def vectorize_for_rag(self, cleaned_data: List[Dict]) -> Dict[str, Any]:
        """
        向量化预处理（为RAG准备）
        这是第二层价值：直接可用于向量数据库
        """
        print(f"[向量化] 开始向量化 {len(cleaned_data)} 条数据...")
        
        vectorized_corpus = {
            "documents": [],
            "metadata": {
                "total_docs": len(cleaned_data),
                "avg_length": sum(d["metadata"]["word_count"] for d in cleaned_data) / len(cleaned_data),
                "created_at": datetime.now().isoformat(),
                "format": "ready_for_embedding",
                "recommended_models": ["text-embedding-3-large", "bge-large-zh"]
            }
        }
        
        for doc in cleaned_data:
            # 分块处理（Chunking）
            chunks = self._chunk_text(doc["content"], chunk_size=512, overlap=50)
            
            for i, chunk in enumerate(chunks):
                vectorized_corpus["documents"].append({
                    "doc_id": doc["id"],
                    "chunk_id": f"{doc['id']}_chunk_{i}",
                    "text": chunk,
                    "metadata": {
                        **doc["metadata"],
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })
        
        print(f"[向量化] 完成，生成 {len(vectorized_corpus['documents'])} 个文本块")
        return vectorized_corpus
    
    def _chunk_text(self, text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """文本分块"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def package_as_product(self, industry: str, vectorized_corpus: Dict) -> str:
        """
        打包为可售卖的数据产品
        """
        product_name = f"{industry}_corpus_{datetime.now().strftime('%Y%m%d')}"
        product_dir = self.output_dir / product_name
        product_dir.mkdir(exist_ok=True)
        
        # 保存数据
        data_file = product_dir / "corpus.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(vectorized_corpus, f, ensure_ascii=False, indent=2)
        
        # 生成README
        readme = self._generate_product_readme(industry, vectorized_corpus)
        readme_file = product_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        # 生成使用示例
        example = self._generate_usage_example(industry)
        example_file = product_dir / "usage_example.py"
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(example)
        
        print(f"[打包完成] 数据产品已保存至: {product_dir}")
        return str(product_dir)
    
    def _generate_product_readme(self, industry: str, corpus: Dict) -> str:
        """生成产品说明文档"""
        info = self.target_industries.get(industry, {})
        
        return f"""# {industry.upper()} 行业语料库

## 产品信息
- **行业**: {industry}
- **文档数量**: {corpus['metadata']['total_docs']}
- **文本块数量**: {len(corpus['documents'])}
- **平均长度**: {corpus['metadata']['avg_length']:.0f} 词
- **生成时间**: {corpus['metadata']['created_at']}
- **定价**: {info.get('价值', 'N/A')}

## 数据来源
{chr(10).join(f"- {source}" for source in info.get('数据源', []))}

## 客户痛点
{info.get('痛点', '')}

## 数据格式
```json
{{
  "doc_id": "唯一文档ID",
  "chunk_id": "文本块ID",
  "text": "已清洗的文本内容",
  "metadata": {{
    "source_url": "原始URL",
    "date": "发布日期",
    "category": "分类",
    "quality_score": "质量分数"
  }}
}}
```

## 推荐使用场景
1. RAG系统训练数据
2. 领域模型微调
3. 知识图谱构建
4. 语义搜索引擎

## 推荐向量模型
- OpenAI: text-embedding-3-large
- 开源: bge-large-zh / bge-large-en

## 技术支持
购买后提供30天技术支持，包括数据更新和定制化清洗。
"""
    
    def _generate_usage_example(self, industry: str) -> str:
        """生成使用示例代码"""
        return f'''"""
{industry} 语料库使用示例
"""

import json
from openai import OpenAI

# 1. 加载语料库
with open('corpus.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"加载了 {{len(corpus['documents'])}} 个文本块")

# 2. 向量化（使用OpenAI Embedding）
client = OpenAI(api_key="your-api-key")

embeddings = []
for doc in corpus['documents'][:10]:  # 示例：只处理前10个
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=doc['text']
    )
    embeddings.append({{
        'chunk_id': doc['chunk_id'],
        'embedding': response.data[0].embedding,
        'metadata': doc['metadata']
    }})

print(f"生成了 {{len(embeddings)}} 个向量")

# 3. 存入向量数据库（以Pinecone为例）
import pinecone

pinecone.init(api_key="your-pinecone-key")
index = pinecone.Index("{industry}_index")

# 批量插入
vectors = [
    (e['chunk_id'], e['embedding'], e['metadata'])
    for e in embeddings
]
index.upsert(vectors=vectors)

print("向量已存入Pinecone")

# 4. RAG查询示例
query = "你的查询问题"
query_embedding = client.embeddings.create(
    model="text-embedding-3-large",
    input=query
).data[0].embedding

results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

for match in results['matches']:
    print(f"相似度: {{match['score']}}")
    print(f"内容: {{match['metadata']}}")
    print("-" * 50)
'''
    
    async def generate_full_product(self, industry: str, max_docs: int = 10000) -> str:
        """
        一键生成完整数据产品
        """
        print(f"\n{'='*60}")
        print(f"开始生成 {industry} 行业数据产品")
        print(f"{'='*60}\n")
        
        # 步骤1：爬取
        raw_data = await self.crawl_industry_data(industry, max_docs)
        
        # 步骤2：清洗
        cleaned_data = self.clean_and_structure(raw_data)
        
        # 步骤3：向量化
        vectorized_corpus = self.vectorize_for_rag(cleaned_data)
        
        # 步骤4：打包
        product_path = self.package_as_product(industry, vectorized_corpus)
        
        print(f"\n{'='*60}")
        print(f"✅ 数据产品生成完成！")
        print(f"📦 产品路径: {product_path}")
        print(f"💰 建议售价: {self.target_industries[industry]['价值']}")
        print(f"{'='*60}\n")
        
        return product_path
    
    def get_sales_pitch(self, industry: str) -> str:
        """
        生成销售话术（用于冷邮件）
        """
        info = self.target_industries.get(industry, {})
        
        return f"""
主题：{industry} 行业高质量训练数据 - 为您的AI节省3个月数据工程时间

您好，

我注意到您的团队正在开发 {industry} 领域的AI产品。

我们提供已清洗、结构化、向量化预处理的 {industry} 行业语料库：

✅ {info.get('数据源', [])[0] if info.get('数据源') else '专业数据源'}
✅ 10,000+ 高质量文档
✅ 直接可用于RAG/微调
✅ 节省您3个月的数据工程时间

痛点：{info.get('痛点', '')}

定价：{info.get('价值', '')}（含30天技术支持）

提供免费样本数据（100条），回复即可获取。

最佳，
[您的名字]
"""


# ============================================
# 使用示例
# ============================================

async def main():
    engine = DataCorpusEngine()
    
    # 生成医疗合规数据产品
    product_path = await engine.generate_full_product(
        industry="medical_compliance",
        max_docs=10000
    )
    
    # 获取销售话术
    pitch = engine.get_sales_pitch("medical_compliance")
    print(pitch)


if __name__ == "__main__":
    asyncio.run(main())

