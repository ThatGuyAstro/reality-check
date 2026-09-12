(function () {
  fetch('data/activity.json').then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (rows) {
      var list = document.getElementById('activity');
      list.innerHTML = rows.length ? rows.map(function (r) { return '<div class="activity-row"><span class="who">' + r.who + '</span><span>' + r.text + '</span><span class="who">' + r.at + '</span></div>'; }).join('')
        : '<div class="empty good">No activity yet.<br>Activity appears here when tasks change.<a href="board.html">Go to the board</a></div>';
    })
    .catch(function () { document.getElementById('activity').innerHTML = '<div class="empty good">We could not load activity.<a href="#" onclick="location.reload();return false;">Try again</a></div>'; });
  // P5: the comments panel skeleton is never replaced
})();
