function LoadMessages(props){
    const [messages, setMessages] = React.useState([]);

    // Fetching messages from my api
    const fetchMessages = () =>{
        fetch(`messages/${props.group}`)
        .then(response => response.json())
        .then(messages => setMessages(messages));
    }


    // fetch only when the array is empty
    React.useEffect(()=>{
        fetchMessages();
    }, []);


    // List of MEssages
    return(
        <>
            {messages.map(message => (
                <div key={message.id} className="list-group-item list-group-item-action flex-column align-items-start">
                    <h5>{message.content}</h5><br/>
                    <small>{message["timestamp"]}</small><br/>
                    <p>Sender: {message["sender"]}</p>
                    <button type="button" className="m-2 ms-auto btn btn-outline-primary" onClick = {() => decrypt(message.id)}>Decrypt</button>
                </div>
            ))}
        </>
    )
}









