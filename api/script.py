import xml.etree.ElementTree as ET

class Response:
    def __init__(self, xml_string):
        self.parse_xml(ET.fromstring(xml_string))

    def parse_xml(self, element, parent=None):
        if not parent:
            parent = self
        if element.attrib:
            for key, value in element.attrib.items():
                setattr(parent, key, value)
        if element.text:
            setattr(parent, 'value', element.text.strip())
        for child in element:
            class_name = child.tag.replace('-', '_').replace('.', '_').replace(':', '_')
            child_obj = type(class_name, (object,), {})
            if child.attrib:
                for key, value in child.attrib.items():
                    setattr(child_obj, key, value)
            setattr(parent, class_name, child_obj())
            self.parse_xml(child, getattr(parent, class_name))

rXML = """
<fi>
    <header Version="1.1">
        <service Version="1.0" Name="DServer">
            <DateTime>2020-05-26T12:27:33</DateTime>
         </service>
        <datasource/>
    </header>
    <response type="inq" totalrows="2">
        <status>
            <code>0</code>
        </status>
        <DocRes url="myurl.com">
            <document>
                <id>1</id>
                <name>doc1</name>
                <detail type="data">
                    <name>Amt</name>
                    <value>33</value>
                </detail>
                <detail type="data">
                    <name>code</name>
                    <value>1</value>
                </detail>
                <detail type="data">
                    <name>desc</name>
                    <value>document 1</value>
                </detail>
            </document>
            <document>
                <id>3</id>
                <name>doc3</name>
                <detail type="data">
                    <name>Amt</name>
                    <value>5</value>
                </detail>
                <detail type="data">
                    <name>code</name>
                    <value>1</value>
                </detail>
                <detail type="data">
                    <name>desc</name>
                    <value>document 3</value>
                </detail>
            </document>
        </DocRes>
    </response>
</fi>
"""

r = Response(rXML)
print(r.header.service.Version) # output: 1.0
print(r.response.DocRes.document[0].name) # output: doc1
print(r.response.DocRes.document[1].detail[2].value) # output: document 3
