# xml2yaml
Python3 XML to YAML parser learning project

## Usage
```python3
import xml_parser

with  open('in.xml', 'r', encoding='utf-8') as in_, \
      open('out.yaml', 'w+', encoding='utf-8') as out:
    a = xml_parser.parse(in_)
    xml_parser.to_yaml(a, out)
```
