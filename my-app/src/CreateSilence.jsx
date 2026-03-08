import { useState } from "react";
import { createSilence } from "./api";


export default function CreateSilence() {

  const [matchers, setMatchers] = useState([
    { label: "", operator: "=", value: "" }
  ]);

  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [comment, setComment] = useState("");

  const username = sessionStorage.getItem("username");

  const addMatcher = () => {
    setMatchers([...matchers, { label: "", operator: "=", value: "" }]);
  };

  const updateMatcher = (index, field, value) => {
    const newMatchers = [...matchers];
    newMatchers[index][field] = value;
    setMatchers(newMatchers);
  };

  const submit = async () => {

    const payload = {
      timestamp: new Date().toISOString(),
      matchers: matchers.map(m => ({
        name: m.label,
        operator: m.operator,
        value: m.value
      })),
      start,
      end,
      comment
    };

    console.log("Sending to backend:", payload);
    console.log(username)

    await createSilence(payload, username);

    alert("Silence request sent");
  };

  return (
    <div className="create-silence-container">
      <h2 className="create-silence-title">Create Silence</h2>

      <div className="matchers-section">
        <h3>Matchers</h3>

        {matchers.map((m, i) => (
          <div key={i} className="matcher-group">
            <input
              className="input-field"
              placeholder="label"
              value={m.label}
              onChange={(e) =>
                updateMatcher(i, "label", e.target.value)
              }
            />

            <select
              className="input-field"
              value={m.operator}
              onChange={(e) =>
                updateMatcher(i, "operator", e.target.value)
              }
            >
              <option value="=">=</option>
              <option value="!=">!=</option>
              <option value="=~">=~ (regex)</option>
              <option value="!~">!~ (regex not)</option>
            </select>

            <input
              className="input-field"
              placeholder="value"
              value={m.value}
              onChange={(e) =>
                updateMatcher(i, "value", e.target.value)
              }
            />
          </div>
        ))}

        <button className="add-matcher-btn" onClick={addMatcher}>Add Matcher</button>
      </div>

      <div className="time-section">
        <h3>Start Time</h3>
        <input
          className="input-field"
          type="datetime-local"
          onChange={(e) => setStart(e.target.value)}
        />

        <h3>End Time</h3>
        <input
          className="input-field"
          type="datetime-local"
          onChange={(e) => setEnd(e.target.value)}
        />
      </div>

      <div className="comment-section">
        <h3>Comment</h3>
        <textarea
          className="input-field textarea-field"
          onChange={(e) => setComment(e.target.value)}
        />
      </div>

      <button className="submit-btn" onClick={submit}>Create Silence</button>
    </div>
  );
}