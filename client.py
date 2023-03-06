import xmlrpc.client
import requests

# Connect to the server
proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
    
while True:
    print("1. Create a new note")
    print("2. Get info by a topic")
    print("3. Search and append information from Wikipedia")
    print("4. Exit")
        
    choice = input("Enter your choice (1-3): ")
        
    if choice == "1":
        # Ask the user for input and send it to the server
        topic = input("Enter the topic: ")
        text = input("Enter the note text: ")
        timestamp = input("Enter the timestamp: ")
            
            
        result = proxy.add_note(topic, text, timestamp)
            
        if result:
            print("Note created successfully!")
        else:
            print("Failed to create note")
    elif choice == "2":
        topic = input("Enter the topic: ")
            
        notes = proxy.get_contents(topic)

        print(notes)

    elif choice == "3":
        # Get the data
        search_term = input("Enter a search term: ")
        wikipedia_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={search_term}"
        response = requests.get(wikipedia_url)
        # If the response was succesful
        if response.status_code == 200:
            data = response.json()
            # If the links exists
            if data[3]:
                # Get the first link from the data
                theLink = data[3][0]
                topic = input("Enter the topic to append the wikipedia link to: ")
                result = proxy.append_link(topic, theLink)
                if result:
                    print("link appended succesfully!")
                else:
                    print("Failed to append the link")
            else:
                print("No results found on wikipedia")
        else:
            print("Failed to get data")


    elif choice == "4":
        # Exit the loop 
        print("Exiting...")
        break
        
    else:
        print("Invalid choice. Please try again.")

