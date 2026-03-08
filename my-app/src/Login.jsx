import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const nav = useNavigate();

  const login = () => {
    sessionStorage.setItem("username", username);
    nav("/create");
  };

  return (
    <div>
      <h2>Silence Manager</h2>
      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={login}>Login</button>
    </div>
  );
}