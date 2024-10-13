# Geniux [![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&r=r&ts=1683906897&type=6e&v=0.1.0&x2=0)](https://pypi.org/project/geniux)

## Установка и обновление
```bash
pip install --upgrade geniux
```

## Быстрый старт
```python
from geniux import Client

client = Client()

result = client.searchTracks("New Sylveon")
print(result)

client.close()
```
