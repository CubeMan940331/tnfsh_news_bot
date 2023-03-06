# tnfsh news discord bot
forwarding news to discord channel

source: https://www.tnfsh.tn.edu.tw/latestevent/index.aspx?Parser=9,3,19

## setting config
to create 'config.pkl' using pickle
```python
import pickle
with open('config.pkl','wb') as file:
  pickle.dump({
    'token': bot_token_str,
    'channel_id': channel_id_int
   },file)
```
or just edit the code
