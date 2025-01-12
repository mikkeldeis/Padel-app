import React from "react";


function App() {
    const [message, setMessage] = useState("");

    const fetchMessage = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/hello/");
            setMessage(response.data.message);
        } catch (error) {
            console.error("Error fetching message:", error);
            setMessage("Error fetching message");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>Paddle App</h1>
            <button onClick={fetchMessage}>Say Hello</button>
            {message && <p>{message}</p>}
        </div>
    );
}

export default App;
