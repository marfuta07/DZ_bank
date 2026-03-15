from typing import List
from typing import Dict

def filter_by_state(list_dicts: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    '''Функция которая возвращает список словарей с заданым статусом'''

    filter_dicts = []
    for filter_dict in list_dicts:
        if filter_dict.get('state') == state:
            filter_dicts.append(filter_dict)

    return filter_dicts


if __name__ == "__main__":
  list_dicts = [{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
              {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
              {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
              {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
print(filter_by_state(list_dicts))
