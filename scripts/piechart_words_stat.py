from db.task_db import TaskDB
from collections import Counter
import matplotlib.pyplot as plt

db = TaskDB(user_id="ilya")



cnt = Counter(min(5, item.hits) for item in db.get_words_statistics())

labels = sorted(cnt)
values = [cnt[k] for k in labels]
labels_upd = [f"{k}: ({cnt[k]} {int(cnt[k] / sum(values) * 100)}%)" for k in labels]

plt.pie(x=values, labels=labels_upd)
plt.show()

