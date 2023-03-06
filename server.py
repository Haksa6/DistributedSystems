from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from socketserver import ThreadingMixIn

# Allows multiple client requests
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Set the server
server = ThreadedXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler)

# Add note function
def add_note(topic, text, timestamp):
    tree = ET.parse("notes.xml")
    root = tree.getroot()
    
    for topic_element in root.findall("topic"):
        
            # If the topic exits append to it
            if topic_element.attrib['name'] == topic:
                print(topic_element.attrib['name'])
                note = ET.SubElement(topic_element, 'note')
                text_element = ET.SubElement(note, "text")
                text_element.text = text
                timestamp_element = ET.SubElement(note, "timestamp")
                timestamp_element.text = timestamp
                break
    
    else:
        # Create a new topic and add the note to it
        topic_element = ET.Element('topic')
        topic_element.attrib['name'] = topic
        note = ET.SubElement(topic_element, 'note')
        text_element = ET.SubElement(note, "text")
        text_element.text = text
        timestamp_element = ET.SubElement(note, "timestamp")
        timestamp_element.text = timestamp
        root.append(topic_element)

    # Save to xml database
    tree.write("notes.xml")

    return True

def get_contents(topic):
    tree = ET.parse("notes.xml")
    root = tree.getroot()

    for topic_element in root.findall("topic"):
         if topic_element.attrib['name'] == topic:
            notes = []
            for note in topic_element.findall("note"):
                text_element = note.find("text")
                date_element = note.find("timestamp")
                wikipedia_link = note.find("wikipedia_link")
                # Check that the note exists
                if text_element is not None:
                    notes.append(({"text":text_element.text}))
                if date_element is not None:
                     notes.append(({"timestamp":date_element.text}))
                if wikipedia_link is not None:
                     notes.append(({"wikipedia_link":wikipedia_link.text}))
            return notes

    # If the topic doesnt exist, return an empty list
    return []

     

def append_link(topic, link):
    tree = ET.parse("notes.xml")
    root = tree.getroot()
    print(topic, link)

    for topic_element in root.findall("topic"):
        # If the topic exits append to it
            if topic_element.attrib['name'] == topic:
                note = ET.SubElement(topic_element, 'note')
                wikipedia_link = ET.SubElement(note, "wikipedia_link")
                wikipedia_link.text = link
                # Save to xml database
                tree.write("notes.xml")
                return True
    
    return False
    


server.register_function(add_note)
server.register_function(get_contents)
server.register_function(append_link)
print("Server running on port 8000")



server.serve_forever()