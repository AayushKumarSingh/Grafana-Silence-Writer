import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000"
});

export const createSilence = (data, username) =>
  API.post("/silence", data, {
    headers: { username }
  });

export const getHistory = (username) =>
  API.get("/history", {
    headers: { username }
  });