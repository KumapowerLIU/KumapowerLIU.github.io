// https://raw.githubusercontent.com/malchata/yall.js/main/dist/yall.js
function e(e, o) {
    for (const t in o) {
        const n = o[t];
        e.addEventListener(t, n.listener || n, n.options || void 0);
    }
}

const o = "IntersectionObserver" in window &&
          "IntersectionObserverEntry" in window &&
          "intersectionRatio" in window.IntersectionObserverEntry.prototype,
      t = /baidu|(?:google|bing|yandex|duckduck)bot/i.test(navigator.userAgent),
      n = ["src", "poster"];

function r(e, o) {
    for (const t of n) {
        if (t in e.dataset) {
            e.setAttribute(t, e.dataset[t]);
            if (e.classList.contains(o)) {
                e.classList.remove(o);
            }
        }
    }
}

function s(e, o, t, n) {
    if (e.nodeName === "VIDEO") {
        const sources = Array.from(e.querySelectorAll("source"));
        for (const source of sources) {
            r(source, o);
        }
        e.load();
    }
    r(e, o);
    const s = e.classList;
    if (s.contains(t)) {
        s.remove(t);
        s.add(n);
    }
}

function i(n) {
    const r = (n && n.lazyClass) ? n.lazyClass : "lazy",
          i = (n && n.lazyBackgroundClass) ? n.lazyBackgroundClass : "lazy-bg",
          c = (n && n.lazyBackgroundLoaded) ? n.lazyBackgroundLoaded : "lazy-bg-loaded",
          a = (n && n.threshold) ? n.threshold : 200,
          l = (n && n.events) ? n.events : {},
          d = (n && n.observeChanges) ? n.observeChanges : false,
          f = (n && n.observeRootSelector) ? n.observeRootSelector : "body",
          u = (n && n.mutationObserverOptions) ? n.mutationObserverOptions : { childList: true, subtree: true },
          b = `video.${r},.${i}`;

    let v = Array.from(document.querySelectorAll(b));
    for (const o of v) {
        e(o, l);
    }

    if (o === true && t === false) {
        var y = new IntersectionObserver(entries => {
            for (const entry of entries) {
                if (entry.isIntersecting || entry.intersectionRatio) {
                    const { target: e } = entry;
                    s(e, r, i, c);
                    y.unobserve(e);
                    v = v.filter(o => o !== e);
                    if (v.length === 0 && d === false) {
                        y.disconnect();
                    }
                }
            }
        }, { rootMargin: `${a}px 0%` });

        for (const e of v) {
            y.observe(e);
        }

        if (d) {
            new MutationObserver(() => {
                const n = document.querySelectorAll(b);
                for (const r of n) {
                    if (!v.includes(r)) {
                        v.push(r);
                        e(r, l);
                        if (o === true && t === false) {
                            y.observe(r);
                        }
                    }
                }
            }).observe(document.querySelector(f), u);
        }
    } else if (t) {
        for (const e of v) {
            s(e, r, i, c);
        }
    }
}

window.yall = i;//# sourceMappingURL=yall.js.map
