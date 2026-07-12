/* Verfügbarkeits-Banner — rendert die Pille oben aus window.VERFUEGBAR_AB.
   Nicht bearbeiten; das Datum steht in verfuegbarkeit.js. */
(function () {
  var bar = document.getElementById("availbar");
  var txt = document.getElementById("availtext");
  if (!bar || !txt) return;

  var M = ["Januar","Februar","März","April","Mai","Juni","Juli","August",
           "September","Oktober","November","Dezember"];
  var raw = (window.VERFUEGBAR_AB || "").trim();
  var today = new Date(); today.setHours(0, 0, 0, 0);

  var off = false, dateStr = "";
  var m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(raw);
  if (m) {
    var d = new Date(+m[1], +m[2] - 1, +m[3]); d.setHours(0, 0, 0, 0);
    if (!isNaN(d.getTime()) && d.getTime() > today.getTime()) {
      off = true;
      dateStr = d.getDate() + ". " + M[d.getMonth()] + " " + d.getFullYear();
    }
  }

  if (off) {
    bar.className = "availbar av-off";
    txt.innerHTML = "Momentan ausgebucht · <b>ab " + dateStr + "</b> wieder buchbar";
  } else {
    bar.className = "availbar av-on";
    txt.innerHTML = "<b>Jetzt verfügbar</b> · kurzfristige Einsätze möglich";
  }
  bar.hidden = false;
})();
