import requests
import time
for i in range(30):
    string_chinese= "这位28岁的厨师在旧金山一家购物中心被发现死亡"
    start_time=time.time()
    test_post = requests.get('http://10.104.101.60:8009/'+string_chinese)
    time_taken = time.time() - start_time
    print('time_taken: ', time_taken)
    print(test_post.text)