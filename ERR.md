```
RAW/XML in progress... 1
<li820><data><celltemp>5.1120729e1</celltemp><cellpres>9.7705745e1</cellpres><co2>7.7817983e2</co2><co2abs>5.0988197e-2</co2abs><ivolt>1.1333007e1</ivolt><raw>2725768,1977365</raw></data></li820>

Traceback (most recent call last):
  File "licor_read.py", line 96, in <module>
    tree = et.parse(file_xml)                                                     # Set XML Parser
  File "/usr/lib/python2.7/xml/etree/ElementTree.py", line 1182, in parse
    tree.parse(source, parser)
  File "/usr/lib/python2.7/xml/etree/ElementTree.py", line 656, in parse
    parser.feed(data)
  File "/usr/lib/python2.7/xml/etree/ElementTree.py", line 1642, in feed
    self._raiseerror(v)
  File "/usr/lib/python2.7/xml/etree/ElementTree.py", line 1506, in _raiseerror
    raise err
    
xml.etree.ElementTree.ParseError: junk after document element: line 2, column 0
```