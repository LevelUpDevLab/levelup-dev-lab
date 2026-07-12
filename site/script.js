// Progressive enhancement only: the page is complete without this script.
// It refreshes the "Latest episode" card from episodes.json so the HTML
// doesn't need editing every time a new episode ships.
(function () {
  "use strict";

  var container = document.querySelector("[data-latest-episode]");
  if (!container || typeof fetch !== "function") return;

  fetch("episodes.json")
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    })
    .then(function (data) {
      var episodes = (data && data.episodes) || [];
      if (episodes.length === 0) return;

      // Newest = highest episode number.
      var latest = episodes.reduce(function (a, b) {
        return Number(b.number) > Number(a.number) ? b : a;
      });

      render(latest);
    })
    .catch(function () {
      // Leave the static fallback in place. Nothing to do.
    });

  function render(ep) {
    // Build DOM with textContent (never innerHTML) so JSON stays data.
    var article = document.createElement("article");
    article.className = "episode";

    var heading = document.createElement("h3");
    var number = document.createElement("span");
    number.className = "episode-number";
    number.textContent = ep.number;
    heading.appendChild(number);
    heading.appendChild(document.createTextNode(" " + ep.title));

    var summary = document.createElement("p");
    summary.textContent = ep.summary;

    var meta = document.createElement("p");
    meta.className = "episode-meta";
    meta.textContent = (ep.languages || []).join(", ") + " · " + ep.pillar;

    var links = document.createElement("p");
    if (ep.videoUrl) {
      links.appendChild(link(ep.videoUrl, "Watch the episode"));
      links.appendChild(document.createTextNode(" · "));
    }
    links.appendChild(link(ep.codeUrl, "Episode code and README"));

    article.appendChild(heading);
    article.appendChild(summary);
    article.appendChild(meta);
    article.appendChild(links);
    container.replaceWith(article);
  }

  function link(href, text) {
    var a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    return a;
  }
})();
