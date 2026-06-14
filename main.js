/* ── State ──────────────────────────────────────────────────────────────── */
const allMovies    = window.MOVIE_LIST || [];
let   selectedTitle = null;

/* ── DOM refs ───────────────────────────────────────────────────────────── */
const input    = document.getElementById("movieInput");
const dropdown = document.getElementById("dropdown");
const results  = document.getElementById("results");
const btn      = document.getElementById("getRecsBtn");

/* ── Autocomplete ───────────────────────────────────────────────────────── */
input.addEventListener("input", () => {
  selectedTitle = null;
  const q = input.value.toLowerCase().trim();
  if (!q) { closeDropdown(); return; }

  const matches = allMovies.filter(m => m.toLowerCase().includes(q)).slice(0, 10);
  if (!matches.length) { closeDropdown(); return; }

  dropdown.innerHTML = matches
    .map(m => `<li role="option" tabindex="0">${m}</li>`)
    .join("");

  dropdown.querySelectorAll("li").forEach(li => {
    li.addEventListener("click",    () => pickMovie(li.textContent));
    li.addEventListener("keydown",  e => { if (e.key === "Enter") pickMovie(li.textContent); });
  });

  dropdown.classList.add("open");
});

function pickMovie(title) {
  selectedTitle = title;
  input.value   = title;
  closeDropdown();
}

function closeDropdown() {
  dropdown.classList.remove("open");
}

document.addEventListener("click", e => {
  if (!e.target.closest(".search-wrap")) closeDropdown();
});

input.addEventListener("keydown", e => {
  if (e.key === "Enter") { closeDropdown(); fetchRecommendations(); }
});

btn.addEventListener("click", fetchRecommendations);

/* ── Genre parser ───────────────────────────────────────────────────────── */
function parseGenres(raw) {
  if (!raw) return "Unknown";
  try {
    const arr = JSON.parse(raw.replace(/'/g, '"'));
    return arr.slice(0, 2).map(g => g.name).join(", ");
  } catch {
    return String(raw).split(",")[0].trim() || "Unknown";
  }
}

/* ── Fetch recommendations from Flask ──────────────────────────────────── */
async function fetchRecommendations() {
  const title = (selectedTitle || input.value).trim();
  if (!title) { input.focus(); return; }

  btn.disabled = true;
  results.innerHTML = `
    <div class="status">
      <div class="spinner"></div>
      Finding movies similar to <strong style="color:#e8e6f0">${title}</strong>…
    </div>`;

  try {
    const res  = await fetch("/recommend", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ title }),
    });

    const data = await res.json();

    if (!res.ok) {
      results.innerHTML = `<div class="error-box">⚠️ ${data.error || "Something went wrong."}</div>`;
      return;
    }

    renderResults(data.title, data.recommendations);

  } catch (err) {
    results.innerHTML = `<div class="error-box">⚠️ Network error — is the Flask server running?</div>`;
  } finally {
    btn.disabled = false;
  }
}

/* ── Render cards ───────────────────────────────────────────────────────── */
function renderResults(title, recs) {
  results.innerHTML = `
    <div class="section-meta">
      <span class="pill">10 picks</span>
      <span class="because">Because you liked <strong>${title}</strong></span>
    </div>
    <div class="movie-grid" id="movieGrid"></div>
  `;

  const grid = document.getElementById("movieGrid");

  recs.forEach(rec => {
    const rating  = rec.vote_average ? Number(rec.vote_average).toFixed(1) : "N/A";
    const genres  = parseGenres(rec.genres);
    const overview = rec.overview ? rec.overview.slice(0, 140) + (rec.overview.length > 140 ? "…" : "") : "";

    const card = document.createElement("div");
    card.className = "movie-card";

    const safeId = rec.original_title.replace(/\W/g, "_");

    card.innerHTML = `
      <div class="poster-wrap" id="pw_${safeId}">
        <span class="poster-placeholder">🎞</span>
      </div>
      <div class="card-body">
        <div class="card-title">${rec.original_title}</div>
        <div class="card-tags">
          ${rating !== "N/A" ? `<span class="tag tag-rating">★ ${rating}</span>` : ""}
          <span class="tag tag-genre">${genres}</span>
        </div>
        ${overview ? `<div class="card-overview">${overview}</div>` : ""}
      </div>
    `;

    grid.appendChild(card);

    /* Load poster if available */
    if (rec.poster) {
      const img = new Image();
      img.src = rec.poster;
      img.alt = rec.original_title;
      img.onload = () => {
        const pw = document.getElementById(`pw_${safeId}`);
        if (pw) { pw.innerHTML = ""; pw.appendChild(img); }
      };
    }
  });
}
