import os
import logging
from nano_graphrag.base import BaseKVStorage
from nano_graphrag._utils import compute_args_hash

logging.basicConfig(level=logging.WARNING)
logging.getLogger("nano-graphrag").setLevel(logging.INFO)

token = 'f97b28aa71892d6d515007ef44ee5de6.WvLXD1MsFsGklOZa'

MODEL = "glm4-flash"

from zhipuai import ZhipuAI
client = ZhipuAI(api_key=token)

async def glm4_flash_if_cache(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:

    
    messages = []
    
    # Get the cached response if having-------------------
    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(MODEL, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]
    # -----------------------------------------------------
    response = client.chat.completions.create(
    model="glm-4-flash",
    messages=
        messages
        )
    # Cache the response if having-------------------
    if hashing_kv is not None:
        await hashing_kv.upsert(
            {args_hash: {"return": response.choices[0].message.content, "model": MODEL}}
        )
    # -----------------------------------------------------
    return response.choices[0].message.content
    

import numpy as np
from nano_graphrag import GraphRAG, QueryParam
from nano_graphrag._utils import wrap_embedding_func_with_attrs
# We're using Sentence Transformers to generate embeddings for the BGE model
@wrap_embedding_func_with_attrs(
    embedding_dim=2048,
    max_token_size=2028,
)
async def local_embedding(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(
        model="embedding-3",  # 填写需要调用的模型编码
        input=texts,
    )
    response = response.data
    response = sorted(response,key=lambda x:x.index)
    return np.array([i.embedding for i in response])


def remove_if_exist(file):
    if os.path.exists(file):
        os.remove(file)


WORKING_DIR = "./heishenhua_cache_glm_flash_TEST"


def query():
    rag = GraphRAG(
        working_dir=WORKING_DIR,
        best_model_func=glm4_flash_if_cache,
        cheap_model_func=glm4_flash_if_cache,
         embedding_func=local_embedding
    )
    print(
        rag.query(
            "我要获得最佳体验，需要什么电脑配置？", param=QueryParam(mode="global")
        )
    )


def insert():
    from time import time

    with open("./tests/mock_data.txt", encoding="utf-8-sig") as f:
        FAKE_TEXT = f.read()[:1000]
    FAKE_TEXT = ['{"title": "《黑神话悟空》变身技能怎么玩 变身技能获取玩法攻略", "content": "\n\n在《黑神话：悟空》的实机演示视频中，为我们演示了许多技能的效果，变身就是其中之一，并且演示了两次。玩家“大写的维特”带来了《黑神话：悟空》变身技能介绍以及实际情况猜想，感兴趣的小伙伴就来看看吧。\n\n![《黑神话：悟空》变身技能介绍](https://image.9game.cn/2020/8/24/171404101.jpg)\n\n**《黑神话：悟空》变身技能介绍：**\n\n演示提供的信息是击杀会掉落法宝的怪物，通过拾取法宝来获得的能力。\n\n当然“猿”，可能是自带，差不多等于原始暴怒。\n\n变身狼教头，获得其能力，武器，攻击方式，技能，并回复血量。\n\n可以推测，以后玩家通过击杀怪物能获得的法宝或者说变身道具应该不少(大爱)。\n\n但是，玩家能携带的应该有限，只能从收藏中选几个携带。\n\n而且，每一章节每个变身只能使用一次(用完猿后没看到CD)。\n\n或者说，在你拾取到一定数量的法宝之后，想再拾取你就必须舍弃前面拾取的。\n\n[\n![](https://media.9game.cn/gamebase/20230809/1/1/1e0607b83da04ea1906f874ab120e76f.jpg?x-oss-\nprocess=image/resize,w_120,m_lfit)](https://www.9game.cn/hshwk/)\n**[黑神话悟空](https://www.9game.cn/hshwk/)** 类型: _角色扮演_ 平台: _安卓_ 状态: _运营_\n\n安卓版下载 苹果版暂无下载\n\n"}']
    FAKE_TEXT = open('heishenhua.txt').readlines()[:200]
    print(FAKE_TEXT[0], len(FAKE_TEXT))
    remove_if_exist(f"{WORKING_DIR}/vdb_entities.json")
    remove_if_exist(f"{WORKING_DIR}/kv_store_full_docs.json")
    remove_if_exist(f"{WORKING_DIR}/kv_store_text_chunks.json")
    remove_if_exist(f"{WORKING_DIR}/kv_store_community_reports.json")
    remove_if_exist(f"{WORKING_DIR}/graph_chunk_entity_relation.graphml")

    rag = GraphRAG(
        working_dir=WORKING_DIR,
        enable_llm_cache=True,
        best_model_func=glm4_flash_if_cache,
        cheap_model_func=glm4_flash_if_cache,
        embedding_func=local_embedding
    )
    start = time()
    rag.insert(FAKE_TEXT)
    print("indexing time:", time() - start)
    # rag = GraphRAG(working_dir=WORKING_DIR, enable_llm_cache=True)
    # rag.insert(FAKE_TEXT[half_len:])

if __name__ == "__main__":
    #insert()
    query()

