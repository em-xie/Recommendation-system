from typing import Dict,List
import numpy as np
import faiss
from recall.dataset.embedding import get_one_user_embedding,get_all_item_embedding

class LSH:
    def __init__(self,embedding:Dict[int,List[float]]) ->None:
        # 分成一个元组
        items = embedding.items()
        # 第一个元素 id
        self.ids = [i[0]for i in items]
        #第二个元素 embedding
        vectors = [i[1] for i in items]

        d = len(vectors[0])
        print(f'd={d}')
        # 建立索引  向量维度embedding的长度 平面切割256
        self.index = faiss.IndexLSH(d,256)
        # 转化成向量
        array_vec = np.asarray(vectors,dtype=np.float32)
        # 加入训练
        self.index.add(array_vec)
        assert(self.index.is_trained)
        print(f'LSH index added {self.index.ntotal} vectors')

    def search(self,vec:List[float],n=20) ->List[int]:
        print(vec)
        # 下标检索 2个向量返回
        D,I = self.index.search(np.asarray([vec],dtype=np.float32),n)
        neighbors = I[0]
        res = [self.ids[i] for i in neighbors]
        print('D:')
        print(D)


def get_item_lsh():
    return LSH