// app.js — tema, ricerca, animazioni. Nessuna richiesta di rete: il sito vive su file://.

(function () {
  "use strict";

  // --- Tema -----------------------------------------------------------------
  var CHIAVE = "cockpit-tema";
  var radice = document.documentElement;

  try {
    var salvato = localStorage.getItem(CHIAVE);
    if (salvato) radice.setAttribute("data-tema", salvato);
  } catch (e) {
    // localStorage può essere negato: il tema di default resta valido.
  }

  var bottoneTema = document.querySelector("[data-cambia-tema]");
  if (bottoneTema) {
    var disegna = function () {
      bottoneTema.textContent = radice.getAttribute("data-tema") === "scuro" ? "☾" : "☀";
    };
    disegna();
    bottoneTema.addEventListener("click", function () {
      var nuovo = radice.getAttribute("data-tema") === "scuro" ? "chiaro" : "scuro";
      radice.setAttribute("data-tema", nuovo);
      disegna();
      try { localStorage.setItem(CHIAVE, nuovo); } catch (e) {}
    });
  }

  // --- Contatori animati ----------------------------------------------------
  // Il numero sale fino al valore: l'avanzamento si legge meglio se lo si vede muovere.
  document.querySelectorAll("[data-conta]").forEach(function (nodo) {
    var arrivo = parseFloat(nodo.getAttribute("data-conta"));
    if (isNaN(arrivo)) return;
    var durata = 1100, avvio = null;
    var passo = function (ora) {
      if (avvio === null) avvio = ora;
      var quota = Math.min((ora - avvio) / durata, 1);
      var eased = 1 - Math.pow(1 - quota, 3);
      nodo.textContent = Math.round(arrivo * eased).toLocaleString("it-IT");
      if (quota < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  });

  // --- Archi ----------------------------------------------------------------
  document.querySelectorAll("[data-arco]").forEach(function (cerchio) {
    var quota = parseFloat(cerchio.getAttribute("data-arco")) || 0;
    var lunghezza = cerchio.getTotalLength ? cerchio.getTotalLength() : 0;
    if (!lunghezza) return;
    cerchio.style.strokeDasharray = String(lunghezza);
    cerchio.style.strokeDashoffset = String(lunghezza);
    requestAnimationFrame(function () {
      cerchio.style.strokeDashoffset = String(lunghezza * (1 - quota));
    });
  });

  // --- Ingresso in scena ----------------------------------------------------
  if ("IntersectionObserver" in window) {
    var osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (voce) {
        if (voce.isIntersecting) {
          voce.target.classList.add("sequenza");
          osservatore.unobserve(voce.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll("[data-entra]").forEach(function (n) { osservatore.observe(n); });
  }

  // --- Filtri ---------------------------------------------------------------
  document.querySelectorAll("[data-filtro-gruppo]").forEach(function (gruppo) {
    var bersaglio = document.querySelector(gruppo.getAttribute("data-filtro-gruppo"));
    if (!bersaglio) return;
    gruppo.addEventListener("click", function (evento) {
      var bottone = evento.target.closest("[data-filtro]");
      if (!bottone) return;
      var valore = bottone.getAttribute("data-filtro");
      gruppo.querySelectorAll("[data-filtro]").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === bottone));
      });
      bersaglio.querySelectorAll("[data-tipo]").forEach(function (riga) {
        riga.hidden = !(valore === "*" || riga.getAttribute("data-tipo") === valore);
      });
    });
  });

  // --- Ricerca --------------------------------------------------------------
  var finestra = document.getElementById("ricerca");
  var campo = document.getElementById("ricerca-campo");
  var esiti = document.getElementById("ricerca-esiti");
  if (!finestra || !campo || !esiti) return;

  // Caricato da assets/indice.js, condiviso da tutte le pagine.
  var voci = Array.isArray(window.INDICE) ? window.INDICE : [];

  var normalizza = function (s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  };

  var mostra = function (query) {
    var q = normalizza(query.trim());
    esiti.innerHTML = "";
    if (!q) return;
    var termini = q.split(/\s+/);
    voci
      .filter(function (v) {
        var ago = normalizza(v.t + " " + (v.s || ""));
        return termini.every(function (t) { return ago.indexOf(t) !== -1; });
      })
      .slice(0, 30)
      .forEach(function (v) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = (window.RADICE || "") + (v.e ? "../" : "") + v.h;
        a.textContent = v.t;
        var piccolo = document.createElement("small");
        piccolo.textContent = v.s || "";
        li.appendChild(a);
        li.appendChild(piccolo);
        esiti.appendChild(li);
      });
  };

  var apri = function () {
    if (!finestra.open) finestra.showModal();
    campo.value = "";
    esiti.innerHTML = "";
    campo.focus();
  };

  campo.addEventListener("input", function () { mostra(campo.value); });
  campo.addEventListener("keydown", function (evento) {
    if (evento.key !== "Enter") return;
    var primo = esiti.querySelector("a");
    if (primo) { evento.preventDefault(); primo.click(); }
  });

  document.querySelectorAll("[data-apri-ricerca]").forEach(function (b) {
    b.addEventListener("click", apri);
  });
  document.addEventListener("keydown", function (evento) {
    if ((evento.ctrlKey || evento.metaKey) && evento.key.toLowerCase() === "k") {
      evento.preventDefault();
      apri();
    }
  });
})();
