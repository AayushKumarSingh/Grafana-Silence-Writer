import { useEffect, useState } from "react";
import { getHistory } from "./api";

export default function History() {

  const [history, setHistory] = useState([]);
  const username = sessionStorage.getItem("username");

  useEffect(() => {

    getHistory(username).then(res => {
      setHistory(res.data);
    });

  }, []);

  return (
    <div>

      <h2>Silence History</h2>

      <table border="1">

        <thead>
          <tr>
            <th>Unique ID</th>
            <th>Timestamp</th>
            <th>User</th>
            <th>Status</th>
            <th>Start</th>
            <th>End</th>
            <th>Comment</th>
          </tr>
        </thead>

        <tbody>

          {history.map((h, i) => (
            <tr key={i}>
              <td>{h.id}</td>
              <td>{h.timestamp}</td>
              <td>{h.username}</td>
              <td>{h.status}</td>
              <td>{h.start}</td>
              <td>{h.end}</td>
              <td>{h.comment}</td>
            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}