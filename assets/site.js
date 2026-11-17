// dMoon's Chalkboard Physics: renders the video list and the watch page from videos.json
(function () {
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'text') n.textContent = attrs[k]; else n.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function clock(s) { s = Math.round(s); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); }
  function niceDate(d) {
    var t = new Date(d + 'T00:00:00');
    return isNaN(t) ? d : t.toLocaleDateString('en', { year: 'numeric', month: 'short', day: 'numeric' });
  }
  function load() {
    return fetch('videos.json', { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('videos.json: ' + r.status);
      return r.json();
    });
  }

  function renderIndex(root) {
    load().then(function (list) {
      list.sort(function (a, b) { return a.date < b.date ? 1 : -1; });
      root.textContent = '';
      if (!list.length) { root.appendChild(el('p', { class: 'empty', text: 'No videos yet.' })); return; }
      var grid = el('ul', { class: 'grid' });
      list.forEach(function (v) {
        var href = 'watch.html?v=' + encodeURIComponent(v.id);
        grid.appendChild(el('li', { class: 'card' }, [
          el('a', { class: 'thumb', href: href, 'aria-hidden': 'true', tabindex: '-1' }, [
            el('img', { src: v.poster, alt: '', loading: 'lazy' }),
            v.duration ? el('span', { class: 'dur', text: clock(v.duration) }) : null
          ]),
          el('div', { class: 'body' }, [
            el('h3', {}, [el('a', { href: href, text: v.title })]),
            el('p', { text: v.summary || '' }),
            el('ul', { class: 'tags' }, (v.tags || []).map(function (t) { return el('li', { text: t }); })),
            el('div', { class: 'meta', text: [v.paper && v.paper.cite, niceDate(v.date)].filter(Boolean).join('  ·  ') })
          ])
        ]));
      });
      root.appendChild(grid);
    }).catch(function (e) {
      root.textContent = 'Could not load the video list (' + e.message + ').';
    });
  }

  function renderWatch(root) {
    var id = new URLSearchParams(location.search).get('v');
    load().then(function (list) {
      var v = list.filter(function (x) { return x.id === id; })[0];
      root.textContent = '';
      if (!v) { root.appendChild(el('p', { class: 'empty', text: 'Video not found.' })); return; }
      document.title = v.title + " | dMoon's Chalkboard Physics";
      var video = el('video', { class: 'player', controls: '', preload: 'metadata', poster: v.poster, src: v.video });
      root.appendChild(el('h1', { text: v.title }));
      root.appendChild(el('p', { class: 'lead', text: v.summary || '' }));
      root.appendChild(video);

      var left = el('div', {}, []);
      if (v.paper) {
        left.appendChild(el('h2', { text: 'The paper' }));
        var p = el('p', {}, [document.createTextNode((v.paper.authors ? v.paper.authors + ', ' : '') + '"' + v.paper.title + '", ' + v.paper.cite + '. ')]);
        if (v.paper.url) p.appendChild(el('a', { href: v.paper.url, text: 'Read the paper' }));
        left.appendChild(p);
      }
      left.appendChild(el('p', {}, [el('a', { href: v.video, download: '', text: 'Download the video (MP4)' })]));
      if (v.credits) left.appendChild(el('div', { class: 'note', text: v.credits }));

      var right = el('div', {}, []);
      if (v.chapters && v.chapters.length) {
        right.appendChild(el('h2', { text: 'Chapters' }));
        var ul = el('ul', { class: 'chapters' });
        v.chapters.forEach(function (c) {
          var b = el('button', { type: 'button' }, [el('span', { class: 't', text: clock(c.t) }), el('span', { text: c.title })]);
          b.addEventListener('click', function () { video.currentTime = c.t; video.play(); video.scrollIntoView({ block: 'nearest' }); });
          ul.appendChild(el('li', {}, [b]));
        });
        right.appendChild(ul);
      }
      root.appendChild(el('div', { class: 'cols' }, [left, right]));
    }).catch(function (e) {
      root.textContent = 'Could not load the video (' + e.message + ').';
    });
  }

  var idx = document.getElementById('video-list'), watch = document.getElementById('watch');
  if (idx) renderIndex(idx);
  if (watch) renderWatch(watch);
})();
