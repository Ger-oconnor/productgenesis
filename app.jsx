// app.jsx — Product Genesis (full rebuild, single file for reliability)

const { useState, useEffect, useRef, useMemo } = React;
const CATS = globalThis.PG_CATEGORIES;
const POSTS = globalThis.PG_POSTS;

// ─── helpers ──────────────────────────────────────────────────────────
const TYPE = {
  essay: "Essay",
  note: "Note",
  video: "Video",
  "case-study": "Case study",
  thought: "Thought",
};
function catById(id) { return CATS.find(c => c.id === id); }
function ytThumb(url) {
  if (!url) return null;
  const m = url.match(/[?&]v=([^&]+)/);
  return m ? `https://img.youtube.com/vi/${m[1]}/hqdefault.jpg` : null;
}
function smoothScrollTo(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const y = el.getBoundingClientRect().top + globalThis.scrollY - 64;
  globalThis.scrollTo({ top: y, behavior: "smooth" });
}

// ─── Dispatch / Vol helpers ──────────────────────────────────────────
const _dispatchDates = [...new Set(POSTS.filter(p => p.date.includes('2026')).map(p => p.date))]
  .sort((a, b) => new Date(a) - new Date(b));
const VOL_TOTAL = _dispatchDates.length;
const VOL_LABEL = String(VOL_TOTAL).padStart(2, '0');
const VOL_LATEST_DATE = _dispatchDates[VOL_TOTAL - 1] || '';
const VOL_LATEST_MONTH = VOL_LATEST_DATE.replace(/\s*\d+,\s*/, ' ').trim();
const VOL_LATEST_COUNT = POSTS.filter(p => p.date === VOL_LATEST_DATE).length;
function volOf(post) {
  const i = _dispatchDates.indexOf(post.date);
  return i >= 0 ? i + 1 : null;
}

// ─── Hero: Honeycomb ─────────────────────────────────────────────────
function HoneycombHero({ onCategory }) {
  const R = 78;
  const W = Math.sqrt(3) * R;
  const hex = (cx, cy, r) => {
    const pts = [];
    for (let i = 0; i < 6; i++) {
      const a = (Math.PI / 3) * i;
      pts.push(`${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`);
    }
    return pts.join(' ');
  };
  const cells = [
    { id: 'vision',      cx: 130, cy: 110 },
    { id: 'strategy',    cx: 130 + W, cy: 110 },
    { id: 'development', cx: 130 - W/2, cy: 110 + R * 1.5 },
    { id: 'marketing',   cx: 130 + W * 1.5, cy: 110 + R * 1.5 },
    { id: 'sales',       cx: 130, cy: 110 + R * 3 },
    { id: 'operations',  cx: 130 + W, cy: 110 + R * 3 },
  ];
  return (
    <div className="hero-honeycomb">
      <svg viewBox="0 0 440 460" aria-label="Category map">
        {cells.map((c) => {
          const cat = catById(c.id);
          return (
            <g key={c.id} className="hex-cell" onClick={() => onCategory(c.id)}>
              <polygon className="hex-shape" points={hex(c.cx, c.cy, R - 4)} />
              <text className="hex-num" x={c.cx} y={c.cy - 14} textAnchor="middle">{cat.n}</text>
              <text className="hex-label" x={c.cx} y={c.cy + 10} textAnchor="middle">{cat.label}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ─── Hero: Orbital ────────────────────────────────────────────────────
function OrbitalHero({ onCategory }) {
  const vision = catById('vision');
  const rest = CATS.filter(c => c.id !== 'vision');
  const angles = [-90, -25, 45, 125, 215];
  return (
    <div className="hero-orbital">
      <div className="orb">
        <div className="orb-ring r1"></div>
        <div className="orb-ring r2"></div>
        <div className="orb-center" role="button" tabIndex={0}
             onClick={() => onCategory('vision')}
             onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onCategory('vision')}>
          <div className="num">01</div>
          <div className="lbl">{vision.label}</div>
          <div className="blurb">Where it all points.</div>
        </div>
        {rest.map((c, i) => {
          const a = (angles[i] * Math.PI) / 180;
          const x = 50 + 42 * Math.cos(a);
          const y = 50 + 42 * Math.sin(a);
          return (
            <div key={c.id} className="orb-node" style={{ left: `${x}%`, top: `${y}%` }}
                 role="button" tabIndex={0}
                 onClick={() => onCategory(c.id)}
                 onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onCategory(c.id)}>
              <div className="num">{c.n}</div>
              <div className="lbl">{c.label}</div>
              <div className="blurb">{c.blurb.split('.')[0]}.</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Hero: Editorial ─────────────────────────────────────────────────
function EditorialHero({ onCategory }) {
  return (
    <div className="hero-editorial">
      <div className="cover" role="button" tabIndex={0}
           onClick={() => onCategory('vision')}
           onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onCategory('vision')}>
        <div className="stamp">
          <span>Product Genesis</span>
          <span className="bar"></span>
          <span>Vol. {VOL_LABEL}</span>
        </div>
        <h2>
          What <span className="accent">design</span><br/>
          becomes next.
        </h2>
        <div className="foot">
          <span>Cover · May 2026</span>
          <span>Open ↗</span>
        </div>
      </div>
      <div className="ed-list">
        <h3>The six zones</h3>
        {CATS.map(c => (
          <div key={c.id} className="ed-row" role="button" tabIndex={0}
               onClick={() => onCategory(c.id)}
               onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onCategory(c.id)}>
            <div className="ed-num">{c.n}</div>
            <div>
              <div className="ed-label">{c.label}</div>
              <div className="ed-blurb">{c.blurb}</div>
            </div>
            <div className="ed-arrow">→</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Post card ───────────────────────────────────────────────────────
function PostCard({ post, span, expanded, onToggle }) {
  const cat = catById(post.cat);
  const subLabel = post.sub && cat.sub ? cat.sub.find(s => s.id === post.sub)?.label : null;
  const tone = post.tone ? `tone-${post.tone}` : '';

  if (expanded) {
    return (
      <article id={`post-${post.id}`} className={`card expanded ${tone}`}>
        <ExpandedView post={post} cat={cat} subLabel={subLabel} onClose={onToggle} />
      </article>
    );
  }

  return (
    <article
      className={`card ${span} type-${post.type} ${tone} ${post.feature ? 'feature' : ''}`}
      role="button" tabIndex={0}
      onClick={onToggle}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onToggle()}
    >
      <div className="card-head">
        <span className="pill cat">{cat.label}{subLabel ? ` · ${subLabel}` : ''}</span>
        <span className="pill type">{TYPE[post.type]}</span>
      </div>
      {post.type === 'video' && (
        <div className="vid-thumb">
          {ytThumb(post.sourceUrl) && (
            <img className="vid-img" src={ytThumb(post.sourceUrl)} alt="" />
          )}
          <div className="play-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div className="vid-len">{post.videoLength}</div>
        </div>
      )}
      <h3 className="card-title">{post.title}</h3>
      {post.dek && post.type !== 'thought' && <p className="card-dek">{post.dek}</p>}
      <div className="card-foot">
        <span>{post.date}</span>
        <span className="read-more">{post.type === 'video' ? 'Watch' : 'Read'} →</span>
      </div>
    </article>
  );
}

// ─── Expanded view ───────────────────────────────────────────────────
function ExpandedView({ post, cat, subLabel, onClose }) {
  const [copied, setCopied] = useState(false);
  const [playing, setPlaying] = useState(false);

  const ytId = useMemo(() => {
    if (!post.sourceUrl) return null;
    const m = post.sourceUrl.match(/[?&]v=([^&]+)/);
    return m ? m[1] : null;
  }, [post.sourceUrl]);

  const shareUrl = `${globalThis.location.origin}${globalThis.location.pathname}#post-${post.id}`;

  const copyLink = () => {
    navigator.clipboard?.writeText(shareUrl).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const shareX = () => {
    const text = post.tweet
      ? post.tweet.replace('[link]', shareUrl)
      : `${post.title} ${shareUrl}`;
    const params = new URLSearchParams({ text });
    globalThis.open(`https://twitter.com/intent/tweet?${params}`, '_blank', 'noopener,width=600,height=400');
  };

  const shareLinkedIn = () => {
    const params = new URLSearchParams({ url: shareUrl });
    globalThis.open(`https://www.linkedin.com/sharing/share-offsite/?${params}`, '_blank', 'noopener,width=600,height=500');
  };

  const body = post.body || [post.dek];

  return (
    <div>
      <div className="card-head" style={{ marginBottom: 16 }}>
        <span className="pill cat">{cat.label}{subLabel ? ` · ${subLabel}` : ''}</span>
        <span className="pill type">{TYPE[post.type]}</span>
        <button className="x-close" onClick={onClose} style={{ marginLeft: 'auto' }}>Close ×</button>
      </div>
      <div className="expand-grid">
        <div className="expand-body">
          {post.type === 'video' && (
            playing && ytId
              ? <div className="vid-embed">
                  <iframe
                    src={`https://www.youtube.com/embed/${ytId}?autoplay=1`}
                    title={post.title}
                    allow="autoplay; encrypted-media; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              : <div className="vid-thumb large"
                    role={ytId ? 'button' : undefined} tabIndex={ytId ? 0 : undefined}
                    onClick={ytId ? () => setPlaying(true) : undefined}
                    onKeyDown={ytId ? (e) => (e.key === 'Enter' || e.key === ' ') && setPlaying(true) : undefined}
                    style={ytId ? { cursor: 'pointer' } : undefined}>
                  {ytThumb(post.sourceUrl) && (
                    <img className="vid-img" src={ytThumb(post.sourceUrl)} alt="" />
                  )}
                  <div className="play-btn"><svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></div>
                  <div className="vid-len">{post.videoLength}</div>
                </div>
          )}
          <h2>{post.title}</h2>
          {post.dek && <p className="expand-dek">{post.dek}</p>}
          {body.map((p) => <p key={p.substring(0, 32)}>{p}</p>)}
          {post.sourceUrl && post.type !== 'video' && (
            <div className="source-line">
              Source: <a href={post.sourceUrl} target="_blank" rel="noopener noreferrer"
                onClick={() => gtag('event', 'outbound_click', { post_id: post.id, post_title: post.title, url: post.sourceUrl })}
              >{post.sourceLabel || post.sourceUrl}</a>
            </div>
          )}
        </div>
        <aside className="expand-side">
          {post.type === 'video' && ytId && (
            <div className="side-block">
              {!playing && (
                <button className="watch-btn" onClick={() => setPlaying(true)}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
                  Play video
                </button>
              )}
              <a className="watch-ext" href={post.sourceUrl} target="_blank" rel="noopener noreferrer"
                onClick={() => gtag('event', 'outbound_click', { post_id: post.id, post_title: post.title, url: post.sourceUrl })}>
                Open on YouTube ↗
              </a>
              {post.videoLabel && <div className="vid-label-text">{post.videoLabel}</div>}
            </div>
          )}
          <div className="side-block">
            <h4>Share</h4>
            <div className="share-row">
              <button className="share-btn" title="Share on X" onClick={shareX}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2H21.5l-7.5 8.57L23 22h-6.812l-5.34-6.987L4.8 22H1.54l8.04-9.19L1 2h6.953l4.83 6.376L18.244 2z"/></svg>
              </button>
              <button className="share-btn" title="Share on LinkedIn" onClick={shareLinkedIn}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.22 8h4.56v13.5H.22V8zm7.4 0h4.37v1.84h.06c.61-1.15 2.1-2.36 4.32-2.36 4.62 0 5.47 3.04 5.47 7v7.02h-4.56v-6.22c0-1.48-.03-3.39-2.07-3.39-2.07 0-2.39 1.61-2.39 3.28v6.33H7.62V8z"/></svg>
              </button>
              <button className="share-btn" title="Copy link" onClick={copyLink}>
                {copied
                  ? <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><path d="M20 6L9 17l-5-5"/></svg>
                  : <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>}
              </button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}


// ─── Layout helper ───────────────────────────────────────────────────
function spanFor(p) {
  if (p.feature) return 'span-8';
  if (p.type === 'thought') return 'span-4';
  if (p.type === 'note') return 'span-4';
  if (p.type === 'video') return 'span-6';
  if (p.type === 'case-study') return 'span-6';
  return 'span-6';
}

// ─── Bento feed (homepage Latest) ───────────────────────────────────
function LatestFeed({ expandedId, setExpandedId, density, volFilter }) {
  const layout = useMemo(() => {
    const pool = volFilter === null ? POSTS : POSTS.filter(p => volOf(p) === volFilter);
    const featured = pool.find(p => p.feature && p.type === 'essay') || pool[0];
    if (!featured) return [];
    const v = pool.find(p => p.type === 'video' && p.id !== featured.id);
    const cs = pool.find(p => p.type === 'case-study' && p.id !== featured.id);
    const t1 = pool.find(p => p.type === 'thought');
    const n1 = pool.find(p => p.type === 'note');
    const e2 = pool.find(p => p.type === 'essay' && p.id !== featured.id);
    const t2 = pool.find(p => p.type === 'thought' && p.id !== t1?.id);
    return [
      { p: featured, span: 'span-8' },
      v && { p: v, span: 'span-4' },
      cs && { p: cs, span: 'span-6' },
      e2 && { p: e2, span: 'span-6' },
      t1 && { p: t1, span: 'span-4' },
      n1 && { p: n1, span: 'span-4' },
      t2 && { p: t2, span: 'span-4' },
    ].filter(Boolean);
  }, [volFilter]);
  return (
    <div className={`bento ${density}`}>
      {layout.map(({ p, span }) => (
        <PostCard key={p.id} post={p} span={span}
          expanded={expandedId === p.id}
          onToggle={() => setExpandedId(expandedId === p.id ? null : p.id)}
          />
      ))}
    </div>
  );
}

// ─── Category section ───────────────────────────────────────────────
function CategorySection({ cat, posts, expandedId, setExpandedId, density, volFilter }) {
  const [subFilter, setSubFilter] = useState('all');
  const volPosts = volFilter === null ? posts : posts.filter(p => volOf(p) === volFilter);
  const filtered = (subFilter === 'all' ? volPosts : volPosts.filter(p => p.sub === subFilter)).slice(0, 10);
  return (
    <section id={`cat-${cat.id}`} className="pg-section scroll-anchor">
      <div className="sec-head">
        <div className="sec-head-left">
          <span className="sec-tag">{cat.n} · {cat.label}</span>
          <h2 className="sec-h">On <em>{cat.label.toLowerCase()}.</em></h2>
          <p className="sec-sub">{cat.blurb}</p>
        </div>
        {cat.sub && (
          <div className="sec-filters">
            <button className={`pg-filter ${subFilter==='all'?'active':''}`} onClick={() => setSubFilter('all')}>All</button>
            {cat.sub.map(s => (
              <button key={s.id} className={`pg-filter ${subFilter===s.id?'active':''}`} onClick={() => setSubFilter(s.id)}>{s.label}</button>
            ))}
          </div>
        )}
      </div>
      <div className={`bento ${density}`}>
        {filtered.map(p => (
          <PostCard key={p.id} post={p} span={spanFor(p)}
            expanded={expandedId === p.id}
            onToggle={() => setExpandedId(expandedId === p.id ? null : p.id)}
            />
        ))}
      </div>
    </section>
  );
}

// ─── Newsletter ──────────────────────────────────────────────────────
function Newsletter() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  return (
    <section className="pg-section">
      <div className={`newsletter ${sent ? 'sent' : ''}`}>
        {sent ? (
          <div>
            <div className="check">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
            </div>
            <h3>You're in.</h3>
            <p>Next dispatch lands Tuesday. Watch for "Product Genesis" in your inbox — no funnels, no sequences, just the writing.</p>
          </div>
        ) : (
          <>
            <div>
              <h3>The newsletter for <em>product people</em> shipping into the AI era.</h3>
              <p>One essay, one case study, one quiet thought. Twice a month. Read in eight minutes.</p>
            </div>
            <div>
              <form onSubmit={(e) => { e.preventDefault(); if (email.includes('@')) setSent(true); }}>
                <input type="email" placeholder="you@company.com" value={email} onChange={e => setEmail(e.target.value)} required />
                <button type="submit">Subscribe →</button>
              </form>
              <div className="nl-stamp">Joined by 4,820 product folks · No spam · One-click unsubscribe</div>
            </div>
          </>
        )}
      </div>
    </section>
  );
}

// ─── About ───────────────────────────────────────────────────────────
function AboutBlock() {
  return (
    <section id="about" className="pg-section scroll-anchor">
      <div className="sec-head">
        <div className="sec-head-left">
          <span className="sec-tag">07 · About</span>
          <h2 className="sec-h">Who's behind <em>Genesis.</em></h2>
        </div>
      </div>
      <div className="about-row">
        <div className="portrait">GO</div>
        <div>
          <h3>Gerald O'Connor — <em>Hong Kong</em></h3>
          <p>My mission is to master the art of how companies operate to embody grit, integrity and empathy, pulling 100% in one direction in service of their clients and staff.</p>
          <p>Product Genesis is where I think in public. It's a daily digest of what's worth knowing at the intersection of AI and product — curated, synthesised, and written for practitioners, not spectators.</p>
          <div className="cta-row">
            <a className="pg-cta" href="https://www.linkedin.com/in/geraldoconnor1/" target="_blank" rel="noopener noreferrer">Connect on LinkedIn →</a>
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Vol bar ─────────────────────────────────────────────────────────
function VolBar({ volFilter, setVolFilter }) {
  return (
    <div className="vol-bar">
      <div className="vol-bar-inner">
        <span className="vol-bar-label">Vol. {VOL_LABEL}</span>
        <div className="vol-bar-chips">
          <button
            className={`vol-chip${volFilter === null ? ' active' : ''}`}
            onClick={() => setVolFilter(null)}
          >All dispatches</button>
          <button
            className={`vol-chip${volFilter === VOL_TOTAL ? ' active' : ''}`}
            onClick={() => setVolFilter(VOL_TOTAL)}
          >Vol. {VOL_LABEL} · {VOL_LATEST_COUNT} new</button>
        </div>
      </div>
    </div>
  );
}

// ─── App ─────────────────────────────────────────────────────────────
function App() {
  const [t, setTweak] = useTweaks(globalThis.TWEAK_DEFAULTS);
  const [volFilter, setVolFilter] = useState(null);
  const [showVolBar, setShowVolBar] = useState(false);
  const [expandedId, setExpandedId] = useState(() => {
    const hash = globalThis.location.hash;
    return hash.startsWith('#post-') ? hash.slice(6) : null;
  });

  const openPost = (id) => {
    setExpandedId(id);
    if (id) {
      globalThis.history.replaceState(null, '', `#post-${id}`);
      setTimeout(() => {
        const el = document.getElementById(`post-${id}`);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    } else {
      globalThis.history.replaceState(null, '', globalThis.location.pathname + globalThis.location.search);
    }
  };

  useEffect(() => {
    if (expandedId) {
      const tryScroll = (attempts = 0) => {
        const el = document.getElementById(`post-${expandedId}`);
        if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        else if (attempts < 10) { setTimeout(() => tryScroll(attempts + 1), 100); }
      };
      setTimeout(() => tryScroll(), 100);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    document.documentElement.dataset.theme = t.dark ? 'dark' : 'light';
  }, [t.dark]);

  useEffect(() => {
    document.documentElement.dataset.surface = t.surface || 'paper';
  }, [t.surface]);

  useEffect(() => {
    if (t.palette) {
      document.documentElement.style.setProperty('--accent', t.palette[0]);
      document.documentElement.style.setProperty('--accent-2', t.palette[1]);
    }
  }, [t.palette]);

  useEffect(() => {
    const hero = document.querySelector('.pg-hero');
    if (!hero) return;
    const obs = new IntersectionObserver(([e]) => setShowVolBar(!e.isIntersecting), { threshold: 0 });
    obs.observe(hero);
    return () => obs.disconnect();
  }, []);

  const onCategoryClick = (id) => {
    setExpandedId(null);
    setTimeout(() => smoothScrollTo(`cat-${id}`), 30);
  };

  const Hero = ({
    honeycomb: HoneycombHero,
    orbital: OrbitalHero,
    editorial: EditorialHero,
  })[t.heroVariant] || HoneycombHero;

  return (
    <>
      <header className="pg-header">
        <div className="pg-header-inner">
          <div className="pg-logo">
            <span className="dot"></span>
            <span>Product Genesis</span>
            <em>field notes</em>
          </div>
          <nav className="pg-nav">
            {CATS.map(c => (
              <a key={c.id} href={`#cat-${c.id}`} onClick={(e) => { e.preventDefault(); onCategoryClick(c.id); }}>
                {c.label}
              </a>
            ))}
            <a href="#about" onClick={(e) => { e.preventDefault(); smoothScrollTo('about'); }}>About</a>
          </nav>
          <span className="pg-spacer"></span>
          <span className="pg-issue">Vol. {VOL_LABEL} · {VOL_LATEST_MONTH} 2026</span>
          <button className="pg-cta">Book a call</button>
        </div>
      </header>

      {showVolBar && <VolBar volFilter={volFilter} setVolFilter={setVolFilter} />}

      <section className="pg-hero">
        <div className="hero-inner">
          <div className="hero-copy">
            <div className="hero-meta">
              <span className="pip"></span>
              <span>Vol. {VOL_LABEL} · Field manual</span>
              <span>·</span>
              <span>{VOL_LATEST_COUNT} new dispatches</span>
            </div>
            <h1 className="hero-title">
              Product design,<br/>
              rebuilt for the <em>age of AI</em>.
            </h1>
            <p className="hero-sub">
              Field notes, strategy memos, and case studies from inside the rewiring — vision through operations. Written for founders and teams shipping into a world where intelligence is a primitive.
            </p>
          </div>
          <div className="hero-art">
            <Hero onCategory={onCategoryClick} />
          </div>
        </div>
      </section>

      <section id="latest" className="pg-section scroll-anchor">
        <div className="sec-head">
          <div className="sec-head-left">
            <span className="sec-tag">↓ Latest</span>
            <h2 className="sec-h">Newest <em>dispatches.</em></h2>
            <p className="sec-sub">Click any card to read in place. Or pick a zone from the cover to jump straight to its archive.</p>
          </div>
        </div>
        <LatestFeed expandedId={expandedId} setExpandedId={openPost} density={t.density} volFilter={volFilter} />
      </section>

      {CATS.map((cat, i) => {
        const catPosts = POSTS.filter(p => p.cat === cat.id);
        return (
          <div key={cat.id} className={i % 2 === 0 ? 'tinted' : ''}>
            <CategorySection cat={cat} posts={catPosts}
              expandedId={expandedId} setExpandedId={openPost}
              density={t.density} volFilter={volFilter} />
          </div>
        );
      })}

      <AboutBlock />

      <footer className="pg-footer">
        <div>© 2026 Product Genesis · Field notes from the AI rebuild</div>
        <div className="foot-links">
          <a href="#latest" onClick={(e) => { e.preventDefault(); smoothScrollTo('latest'); }}>Archive</a>
          <a href="#about" onClick={(e) => { e.preventDefault(); smoothScrollTo('about'); }}>About</a>
          <button type="button" className="foot-link-btn">RSS</button>
          <button type="button" className="foot-link-btn">Contact</button>
        </div>
      </footer>

      <TweaksPanel title="Tweaks">
        <TweakSection label="Hero" />
        <TweakSelect
          label="Variant"
          value={t.heroVariant}
          options={[
            { value: 'honeycomb', label: 'Honeycomb grid' },
            { value: 'orbital',   label: 'Orbital map' },
            { value: 'editorial', label: 'Editorial cover' },
          ]}
          onChange={(v) => setTweak('heroVariant', v)}
        />
        <TweakSection label="Theme" />
        <TweakSelect
          label="Surface"
          value={t.surface || 'paper'}
          options={[
            { value: 'paper', label: 'Paper cream' },
            { value: 'bone',  label: 'Bone grey'   },
            { value: 'cool',  label: 'Cool light'  },
            { value: 'navy',  label: 'Deep navy'   },
            { value: 'slate', label: 'Slate dark'  },
          ]}
          onChange={(v) => setTweak('surface', v)}
        />
        <TweakToggle label="Dark mode" value={t.dark} onChange={(v) => setTweak('dark', v)} />
        <TweakColor
          label="Accent"
          value={t.palette}
          options={[
            ['#4A95D0', '#14244C'],
            ['#14244C', '#4A95D0'],
            ['#c8553d', '#a13f29'],
            ['#3b6f4f', '#2a5a3c'],
            ['#1a1a1a', '#000000'],
          ]}
          onChange={(v) => setTweak('palette', v)}
        />
        <TweakSection label="Layout" />
        <TweakRadio
          label="Density"
          value={t.density}
          options={['compact', 'regular', 'comfy']}
          onChange={(v) => setTweak('density', v)}
        />
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
