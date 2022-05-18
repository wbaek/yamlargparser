# YamlArgParser

Yaml Argument Parser

## install

```bash
$ pip install git+https://github.com/wbaek/yamlargparser.git
```


## ArgumentParser

yaml에 있는 변수를 실행시점에 변경하거나 추가로 정의하고 싶을때 사용한다.
기존에 정의되어 있는 yaml에 값을 overwrite하고 싶을때 --key value 형식으로 입력하면되고 기본적인 key의 존재여부 및 value의 type을 확인한다.
ArgumentParser를 상속받아 구현하여 기본적으로 ArgumentParser와 사용법이 동일하다.

* sample_config.yaml
```yaml
value: string
foo:
    bar: text
    baz: 123
data:
    string: text
    int: 1
    float: 0.1
    list: [1, 2, 3]
    dict:
        key: value
```

* sample_config.py
```python
from yamlargparser import ArgumentParser
parser = ArgumentParser(conflict_handler='resolve')
parser.add_argument('--added', type=str, default='NOT_EXIST_CONFIG', help='ADDED_FROM_ARGPARSER')
parser.add_argument('--dump', type=str, default=None, help='config dump filepath')

parsed_args, options = parser.parse_args(return_dict=True)
print(parsed_args)
print(options)
```

```bash
$ python sample_config.py -h
usage: sample_config.py -c CONFIG [CONFIG ...]
sample_config.py: error: the following arguments are required: -c/--config

$ python sample_config.py -c sample_config.yaml -h
usage: sample.py -c CONFIG [CONFIG ...] [-h] [--value VALUE] [--foo-bar FOO_BAR]
                 [--foo-baz FOO_BAZ] [--data-string DATA_STRING]
                 [--data-int DATA_INT] [--data-float DATA_FLOAT]
                 [--data-list [DATA_LIST [DATA_LIST ...]]]
                 [--data-dict-from DATA_DICT_FROM] [--added ADDED]
                 [--dump DUMP]

optional arguments:
  -c CONFIG, --config CONFIG
                        set config filepath
  --added ADDED         ADDED_FROM_ARGPARSER
  --dump DUMP           config dump filepath
  --value VALUE         set str value (default:string)
  --foo-bar FOO_BAR     set str value (default:text)
  --foo-baz FOO_BAZ     set int value (default:123)
  --data-string DATA_STRING
                        set str value (default:text)
  --data-int DATA_INT   set int value (default:1)
  --data-float DATA_FLOAT
                        set float value (default:0.1)
  --data-list [DATA_LIST [DATA_LIST ...]]
                        set int list (default:[1, 2, 3])
  --data-dict-key DATA_DICT_KEY
                        set str value (default:value)
  -h, --help            show this help message and exit

$ python sample_config.py -c sample_config.yaml
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_key='value', data_float=0.1, data_int=1, data_list=[1, 2, 3], data_string='text', dump=None, foo_bar='text', foo_baz=123, value='string')
{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 0.1, 'list': [1, 2, 3], 'dict': {'key': 'value'}}}

$ python sample_config.py -c sample_config.yaml --data-float 10
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_key='value', data_float=10.0, data_int=1, data_list=[1, 2, 3], data_string='text', dump=None, foo_bar='text', foo_baz=123, value='string')
{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 10.0, 'list': [1, 2, 3], 'dict': {'key': 'value'}}}

$ python sample_config.py -c sample_config.yaml --data-float 10 --dump here.yaml
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_key='value', data_float=10.0, data_int=1, data_list=[1, 2, 3], data_string='text', dump='here.yaml', foo_bar='text', foo_baz=123, value='string')
{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 10.0, 'list': [1, 2, 3], 'dict': {'key': 'value'}}}

$ python sample_config.py -c sample_config.yaml --not-exists
usage: sample_config.py -c CONFIG [CONFIG ...] [-h] [--value VALUE] [--foo-bar FOO_BAR]
                        [--foo-baz FOO_BAZ] [--data-string DATA_STRING]
                        [--data-int DATA_INT] [--data-float DATA_FLOAT]
                        [--data-list [DATA_LIST [DATA_LIST ...]]]
                        [--data-dict-from DATA_DICT_FROM] [--added ADDED]
                        [--dump DUMP]
sample_config.py: error: unrecognized arguments: --not-exists
```