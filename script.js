const counter = document.querySelector("#visitor-count");
const counted = localStorage.getItem("uchumeow-visitor-counted") === "yes";
const endpoint = counted ? "/api/count" : "/api/visit";

fetch(`${window.COUNTER_API_URL}${endpoint}`, {
  method: counted ? "GET" : "POST",
  signal: AbortSignal.timeout(3000),
})
  .then((response) => response.json())
  .then((data) => {
    counter.textContent = String(data.count).padStart(6, "0");
    localStorage.setItem("uchumeow-visitor-counted", "yes");
  })
  .catch(() => {
    counter.textContent = "offline";
  });
