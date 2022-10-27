export const BACKEND_URL = process.env["REACT_APP_BACKEND_URL"]
    || `http://${typeof window !== "undefined" ? window.location.hostname : "localhost"}:8080`;
