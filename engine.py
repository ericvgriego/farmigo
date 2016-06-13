import pandas as pd
import time
import redis
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def info(msg):
    current_app.logger.info(msg)


class ContentEngine(object):

    SIMKEY = 'p:smlr:%s'

    def __init__(self):
        self._r = redis.StrictRedis.from_url(current_app.config['REDIS_URL'])

    def train(self, data_source):
        start = time.time()
        ds = pd.read_csv(data_source)
        info("Training data ingested in %s seconds." % (time.time() - start))

        # Flush the stale training data from redis
        self._r.flushdb()

        start = time.time()
        self._train(ds)
        info("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds):
        
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        tf_matrix = tf.fit_transform(ds['text'])
        sim_measure = linear_kernel(tf_matrix, tf_matrix)

        for idx, row in ds.iterrows():
            sim_idx = sim_measure[idx].argsort()[:-12:-1]
            sim_item_id = [(sim_measure[idx][i], test['item_id'][i])
            sim_top10 = sum(sim_item_id[1:], ())
            self._r.zadd(self.SIMKEY % row['item_id'], *sim_top10)

    def predict(self, item_n, num):
        return self._r.zrange(self.SIMKEY % item_n, 0, num-1, withscores=True, desc=True)


content_engine = ContentEngine()
