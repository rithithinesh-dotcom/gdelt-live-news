<style>
.tw2{--bg:#F5F9FF;--sidebar-top:#D9E9FF;--sidebar-bottom:#BFD8FF;--primary:#2563EB;--secondary:#60A5FA;
--card:#FFFFFF;--text:#1E3A8A;--muted:#5D7DB8;--lightgray:#EEF5FF;--success:#22C55E;--warning:#F59E0B;--danger:#EF4444;
--radius:20px;--radius-sm:14px;--shadow:0 10px 30px rgba(37,99,235,.08);--shadow-lift:0 18px 40px rgba(37,99,235,.16);
font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);
display:flex;min-height:700px;border-radius:16px;overflow:hidden;box-sizing:border-box}
.tw2 *{box-sizing:border-box}
.tw2 .sidebar{width:220px;flex-shrink:0;background:linear-gradient(180deg,var(--sidebar-top),var(--sidebar-bottom));padding:22px 14px;display:flex;flex-direction:column;justify-content:space-between}
.tw2 .nav-item{display:flex;align-items:center;gap:10px;padding:11px 14px;border-radius:var(--radius-sm);font-weight:500;font-size:13.5px;color:var(--text);cursor:pointer;margin-bottom:4px;transition:.2s;user-select:none}
.tw2 .nav-item:hover{background:rgba(255,255,255,.45)}
.tw2 .nav-item.active{background:var(--card);color:var(--primary);box-shadow:var(--shadow);font-weight:700}
.tw2 .data-source{background:rgba(255,255,255,.55);border-radius:var(--radius-sm);padding:14px;box-shadow:var(--shadow);margin-bottom:14px}
.tw2 .data-source-label{font-size:10px;color:var(--muted);text-transform:uppercase;margin:0 0 4px}
.tw2 .data-source-name{display:flex;align-items:center;gap:6px;font-weight:700;color:var(--primary);font-size:14px}
.tw2 .data-source-desc{font-size:10.5px;color:var(--muted);margin:6px 0 0;line-height:1.4}
.tw2 .sidebar-footer{font-size:10.5px;color:var(--muted);text-align:center;line-height:1.5}
.tw2 .main{flex:1;padding:22px 26px 30px;min-width:0;overflow-y:auto}
.tw2 .topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap;gap:12px}
.tw2 .brand{display:flex;align-items:center;gap:12px}
.tw2 .brand-icon{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--secondary));display:flex;align-items:center;justify-content:center;box-shadow:var(--shadow-lift);color:#fff;font-size:20px;flex-shrink:0}
.tw2 .brand-text h1{margin:0;font-size:22px;font-weight:800;color:var(--primary);letter-spacing:-.02em}
.tw2 .brand-text p{margin:2px 0 0;font-size:12px;color:var(--muted);font-weight:500}
.tw2 .topbar-right{display:flex;align-items:center;gap:10px}
.tw2 .lu-card{background:var(--card);border-radius:var(--radius-sm);padding:8px 16px;box-shadow:var(--shadow)}
.tw2 .lu-label{font-size:10px;color:var(--muted)}
.tw2 .lu-value{font-size:13px;font-weight:700}
.tw2 .refresh-btn{width:40px;height:40px;border-radius:50%;background:var(--card);box-shadow:var(--shadow);display:flex;align-items:center;justify-content:center;border:none;color:var(--primary);cursor:pointer;font-size:16px;transition:.2s}
.tw2 .refresh-btn:hover{box-shadow:var(--shadow-lift)}
.tw2 .refresh-btn.spin{animation:tw2spin .7s linear}
@keyframes tw2spin{to{transform:rotate(360deg)}}
.tw2 .search-wrap{position:relative;margin-bottom:20px}
.tw2 .search-bar{width:100%;padding:15px 44px;border-radius:999px;border:none;background:var(--card);box-shadow:var(--shadow);font-size:14px;color:var(--text);font-family:inherit}
.tw2 .search-bar:focus{outline:none;box-shadow:var(--shadow-lift)}
.tw2 .search-icon{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:15px}
.tw2 .cards-row{display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:16px;margin-bottom:22px}
.tw2 .card{background:var(--card);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);transition:.25s}
.tw2 .card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lift)}
.tw2 .eyebrow{font-size:11px;font-weight:700;letter-spacing:.04em;color:var(--muted);text-transform:uppercase;margin:0 0 12px}
.tw2 .card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.tw2 .topic-main{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.tw2 .topic-icon{width:44px;height:44px;border-radius:14px;background:var(--lightgray);display:flex;align-items:center;justify-content:center;font-size:22px}
.tw2 .topic-title{font-size:28px;font-weight:800;color:var(--primary)}
.tw2 .badge{display:inline-flex;align-items:center;gap:5px;padding:5px 11px;border-radius:999px;font-size:11px;font-weight:700;background:#FFEDE0;color:#EA6A1F}
.tw2 .topic-desc{font-size:12.5px;color:var(--muted);line-height:1.5;margin:0 0 14px}
.tw2 .metric-pill{background:var(--lightgray);border-radius:var(--radius-sm);padding:12px 16px;display:flex;justify-content:space-between;align-items:center}
.tw2 .metric-label{font-size:11px;color:var(--muted)}
.tw2 .metric-value{font-size:21px;font-weight:800}
.tw2 .metric-growth{color:var(--success);font-weight:700;font-size:14px}
.tw2 .metric-sub{font-size:11px;color:var(--muted);margin:6px 2px 0}
.tw2 .period-select{border:none;background:var(--lightgray);color:var(--primary);font-weight:600;font-size:12px;padding:6px 12px;border-radius:999px;font-family:inherit;cursor:pointer}
.tw2 .sent-body{display:flex;align-items:center;gap:14px}
.tw2 .legend{display:flex;flex-direction:column;gap:9px;flex:1}
.tw2 .legend-row{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;color:var(--muted)}
.tw2 .legend-row b{color:var(--text)}
.tw2 .dot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:6px}
.tw2 .sent-footer{margin-top:14px;padding-top:12px;border-top:1px solid var(--lightgray);display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}
.tw2 .section-head{display:flex;justify-content:space-between;align-items:center;margin:4px 0 12px}
.tw2 .section-head h2{font-size:17px;margin:0}
.tw2 .categories-row{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:22px}
.tw2 .cat-card{background:var(--card);border-radius:var(--radius-sm);padding:14px;box-shadow:var(--shadow);transition:.25s;cursor:pointer}
.tw2 .cat-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lift)}
.tw2 .cat-icon{width:34px;height:34px;border-radius:10px;background:var(--lightgray);display:flex;align-items:center;justify-content:center;font-size:16px;margin-bottom:9px}
.tw2 .cat-name{font-size:12.5px;font-weight:700;margin-bottom:3px}
.tw2 .cat-mentions{font-size:11px;color:var(--muted);margin-bottom:6px}
.tw2 .cat-growth{font-size:11.5px;font-weight:700;color:var(--success)}
.tw2 .headline-row{display:flex;align-items:center;gap:14px;padding:13px 4px;border-bottom:1px solid var(--lightgray)}
.tw2 .headline-row:last-child{border-bottom:none}
.tw2 .headline-thumb{width:52px;height:52px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px}
.tw2 .headline-main{flex:1;min-width:0}
.tw2 .headline-title{font-size:13.5px;font-weight:600;margin:0 0 4px;line-height:1.4}
.tw2 .headline-meta{font-size:11.5px;color:var(--muted)}
.tw2 .sentiment-badge{padding:5px 11px;border-radius:999px;font-size:11.5px;font-weight:700;white-space:nowrap}
.tw2 .sentiment-badge.Positive{background:#E7F9EE;color:var(--success)}
.tw2 .sentiment-badge.Neutral{background:#FFF6E5;color:var(--warning)}
.tw2 .sentiment-badge.Negative{background:#FDEAEA;color:var(--danger)}
.tw2 .read-more{background:var(--lightgray);color:var(--primary);font-weight:600;font-size:12px;padding:8px 14px;border-radius:999px;white-space:nowrap;border:none;cursor:pointer;font-family:inherit}
.tw2 .read-more:hover{background:var(--primary);color:#fff}
@media (max-width:900px){.tw2{flex-direction:column}.tw2 .sidebar{width:100%;flex-direction:row;flex-wrap:wrap}.tw2 .cards-row{grid-template-columns:1fr}.tw2 .categories-row{grid-template-columns:repeat(2,1fr)}}
</style>

<div class="tw2">
  <aside class="sidebar">
    <div>
      <div class="nav-item active">🏠 Dashboard</div>
      <div class="nav-item">📈 Trending Topics</div>
      <div class="nav-item">🔍 News Search</div>
      <div class="nav-item">😊 Sentiment Analysis</div>
      <div class="nav-item">📂 Categories</div>
      <div class="nav-item">🔖 Bookmarks</div>
      <div class="nav-item">📄 Reports</div>
      <div class="nav-item">⚙️ Settings</div>
    </div>
    <div>
      <div class="data-source">
        <p class="data-source-label">Data Source</p>
        <div class="data-source-name">🌍 GDELT</div>
        <p class="data-source-desc">Global Database of Events, Language &amp; Tone</p>
      </div>
      <p class="sidebar-footer">© 2026 TrendWatch<br>All Rights Reserved</p>
    </div>
  </aside>

  <main class="main">
    <div class="topbar">
      <div class="brand">
        <div class="brand-icon">📈</div>
        <div class="brand-text">
          <h1>TrendWatch</h1>
          <p>Live News Trend &amp; Sentiment Analytics</p>
        </div>
      </div>
      <div class="topbar-right">
        <div class="lu-card"><div class="lu-label">Last Updated</div><div class="lu-value" id="tw2LuValue">—</div></div>
        <button class="refresh-btn" id="tw2RefreshBtn" type="button">⟳</button>
      </div>
    </div>

    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input class="search-bar" id="tw2SearchInput" placeholder="Search news, topics or keywords...">
    </div>

    <div class="cards-row">
      <div class="card">
        <p class="eyebrow">Today's Top Trending Topic</p>
        <div class="topic-main">
          <div class="topic-icon">🤖</div>
          <div class="topic-title">AI</div>
          <div class="badge">🔥 Trending</div>
        </div>
        <p class="topic-desc">Artificial Intelligence is dominating global discussions.</p>
        <div class="metric-pill">
          <div><div class="metric-label">Mentions Today</div><div class="metric-value" id="tw2TopicMentions">0</div></div>
          <div class="metric-growth">↑ +78%</div>
        </div>
        <p class="metric-sub">vs yesterday</p>
      </div>

      <div class="card">
        <div class="card-header">
          <p class="eyebrow" style="margin:0">Mentions Over Time</p>
          <select class="period-select" id="tw2PeriodSelect">
            <option value="7">7 Days</option><option value="30">30 Days</option><option value="90">90 Days</option>
          </select>
        </div>
        <div id="tw2ChartWrap" style="height:190px"></div>
      </div>

      <div class="card">
        <p class="eyebrow">Sentiment Overview</p>
        <div class="sent-body">
          <div id="tw2DonutWrap" style="width:110px;height:110px;flex-shrink:0"></div>
          <div class="legend">
            <div class="legend-row"><span><span class="dot" style="background:#2563EB"></span>Positive</span><b>65%</b></div>
            <div class="legend-row"><span><span class="dot" style="background:#60A5FA"></span>Neutral</span><b>25%</b></div>
            <div class="legend-row"><span><span class="dot" style="background:#EEF5FF;border:1px solid #5D7DB8"></span>Negative</span><b>10%</b></div>
          </div>
        </div>
        <div class="sent-footer"><span>Total Analyzed</span><b>15,842 Articles</b></div>
      </div>
    </div>

    <div class="section-head"><h2>Trending Categories</h2></div>
    <div class="categories-row" id="tw2CategoriesRow"></div>

    <div class="card">
      <div class="section-head" style="margin-top:0"><h2>Latest News Headlines</h2></div>
      <div id="tw2HeadlinesList"></div>
    </div>
  </main>
</div>

<script>
(function(){
  var CATS = [
    {name:"AI & Technology", icon:"🤖", color:"#2563EB", mentions:24596, growth:78},
    {name:"Politics", icon:"🏛️", color:"#7C3AED", mentions:18362, growth:32},
    {name:"Business & Finance", icon:"📊", color:"#0EA5E9", mentions:14827, growth:21},
    {name:"Health", icon:"❤️", color:"#EF4444", mentions:12103, growth:18},
    {name:"Sports", icon:"⚽", color:"#22C55E", mentions:9845, growth:12},
    {name:"Entertainment", icon:"🎬", color:"#F59E0B", mentions:8194, growth:8}
  ];

  var HEADLINES = [
    {headline:"AI transforms healthcare: new study shows 30% improvement in diagnostics", source:"TechCrunch", time:"2h ago", sentiment:"Positive", color:"#2563EB", icon:"🤖"},
    {headline:"Parliament passes new digital economy bill amid heated debate", source:"The Hindu", time:"5h ago", sentiment:"Neutral", color:"#7C3AED", icon:"🏛️"},
    {headline:"City United wins the championship after thrilling final match", source:"ESPN Sports", time:"9h ago", sentiment:"Positive", color:"#22C55E", icon:"⚽"},
    {headline:"Markets rally as inflation data beats expectations", source:"Bloomberg", time:"12h ago", sentiment:"Positive", color:"#0EA5E9", icon:"📊"},
    {headline:"Health ministry launches nationwide vaccination drive", source:"Reuters", time:"18h ago", sentiment:"Neutral", color:"#EF4444", icon:"❤️"},
    {headline:"Blockbuster film breaks opening weekend box office records", source:"Variety", time:"1d ago", sentiment:"Positive", color:"#F59E0B", icon:"🎬"}
  ];

  function esc(str){
    var d = document.createElement("div");
    d.textContent = str || "";
    return d.innerHTML;
  }

  function renderCategories(){
    var html = "";
    for(var i=0;i<CATS.length;i++){
      var c = CATS[i];
      html += '<div class="cat-card"><div class="cat-icon">'+c.icon+'</div>' +
        '<div class="cat-name">'+esc(c.name)+'</div>' +
        '<div class="cat-mentions">'+c.mentions.toLocaleString()+' mentions</div>' +
        '<div class="cat-growth">↑ '+c.growth+'%</div></div>';
    }
    document.getElementById("tw2CategoriesRow").innerHTML = html;
  }

  function renderHeadlines(list){
    var emoji = {Positive:"🙂",Neutral:"😐",Negative:"☹️"};
    if(!list.length){
      document.getElementById("tw2HeadlinesList").innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px">No matching headlines.</p>';
      return;
    }
    var html = "";
    for(var i=0;i<list.length;i++){
      var a = list[i];
      html += '<div class="headline-row">' +
        '<div class="headline-thumb" style="background:'+a.color+'">'+a.icon+'</div>' +
        '<div class="headline-main"><p class="headline-title">'+esc(a.headline)+'</p>' +
        '<div class="headline-meta">'+esc(a.source)+' · '+esc(a.time)+'</div></div>' +
        '<div class="sentiment-badge '+a.sentiment+'">'+emoji[a.sentiment]+' '+a.sentiment+'</div>' +
        '<button class="read-more" type="button">Read More →</button></div>';
    }
    document.getElementById("tw2HeadlinesList").innerHTML = html;
  }

  function animateCounter(el, target){
    var start = 0, startTime = null, dur = 900;
    function tick(now){
      if(startTime === null) startTime = now;
      var p = Math.min((now-startTime)/dur, 1);
      var eased = 1 - Math.pow(1-p, 3);
      el.textContent = Math.round(start + (target-start)*eased).toLocaleString();
      if(p<1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function buildSeries(days){
    var data = [], base = 14000;
    for(var i=0;i<days;i++){
      base = base * (1 + (Math.random()*0.12 - 0.03));
      data.push(Math.round(base));
    }
    return data;
  }

  function renderLineChart(days){
    var data = buildSeries(days);
    var w = 300, h = 190, pad = 10;
    var max = Math.max.apply(null, data), min = Math.min.apply(null, data);
    var range = (max - min) || 1;
    var stepX = (w - pad*2) / (data.length - 1 || 1);
    var points = data.map(function(v, idx){
      var x = pad + idx*stepX;
      var y = pad + (h - pad*2) * (1 - (v - min)/range);
      return [x, y];
    });
    var linePath = points.map(function(p, idx){ return (idx===0?"M":"L") + p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" ");
    var areaPath = linePath + " L" + points[points.length-1][0].toFixed(1) + "," + (h-pad) + " L" + points[0][0].toFixed(1) + "," + (h-pad) + " Z";

    var svg = '<svg viewBox="0 0 '+w+' '+h+'" style="width:100%;height:100%" preserveAspectRatio="none">' +
      '<path d="'+areaPath+'" fill="rgba(37,99,235,0.12)" stroke="none"></path>' +
      '<path d="'+linePath+'" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"></path>' +
      '</svg>';
    document.getElementById("tw2ChartWrap").innerHTML = svg;
  }

  function renderDonut(){
    var pos = 65, neu = 25, neg = 10;
    var r = 45, c = 55, circumference = 2 * Math.PI * r;
    var posLen = circumference * pos/100;
    var neuLen = circumference * neu/100;
    var negLen = circumference * neg/100;
    var svg = '<svg viewBox="0 0 110 110" style="width:100%;height:100%;transform:rotate(-90deg)">' +
      '<circle cx="'+c+'" cy="'+c+'" r="'+r+'" fill="none" stroke="#EEF5FF" stroke-width="14"></circle>' +
      '<circle cx="'+c+'" cy="'+c+'" r="'+r+'" fill="none" stroke="#2563EB" stroke-width="14" ' +
        'stroke-dasharray="'+posLen+' '+circumference+'" stroke-linecap="butt"></circle>' +
      '<circle cx="'+c+'" cy="'+c+'" r="'+r+'" fill="none" stroke="#60A5FA" stroke-width="14" ' +
        'stroke-dasharray="'+neuLen+' '+circumference+'" stroke-dashoffset="-'+posLen+'" stroke-linecap="butt"></circle>' +
      '</svg>';
    document.getElementById("tw2DonutWrap").innerHTML = svg;
  }

  function setLastUpdated(){
    var now = new Date();
    var opts1 = {month:'short', day:'numeric', year:'numeric'};
    var opts2 = {hour:'2-digit', minute:'2-digit'};
    document.getElementById("tw2LuValue").textContent = now.toLocaleDateString('en-US', opts1) + " • " + now.toLocaleTimeString('en-US', opts2);
  }

  function wireSearch(){
    document.getElementById("tw2SearchInput").addEventListener("input", function(e){
      var q = e.target.value.trim().toLowerCase();
      var filtered = q ? HEADLINES.filter(function(a){ return a.headline.toLowerCase().indexOf(q) !== -1; }) : HEADLINES;
      renderHeadlines(filtered);
    });
  }

  function wireRefresh(){
    var btn = document.getElementById("tw2RefreshBtn");
    btn.addEventListener("click", function(){
      btn.classList.add("spin");
      setLastUpdated();
      renderLineChart(parseInt(document.getElementById("tw2PeriodSelect").value, 10));
      animateCounter(document.getElementById("tw2TopicMentions"), 20000 + Math.floor(Math.random()*8000));
      setTimeout(function(){ btn.classList.remove("spin"); }, 700);
    });
  }

  function wirePeriodSelect(){
    document.getElementById("tw2PeriodSelect").addEventListener("change", function(e){
      renderLineChart(parseInt(e.target.value, 10));
    });
  }

  function wireNav(){
    var items = document.querySelectorAll(".tw2 .nav-item");
    for(var i=0;i<items.length;i++){
      items[i].addEventListener("click", function(){
        for(var j=0;j<items.length;j++) items[j].classList.remove("active");
        this.classList.add("active");
      });
    }
  }

  wireSearch();
  wireRefresh();
  wirePeriodSelect();
  wireNav();
  renderCategories();
  renderHeadlines(HEADLINES);
  renderLineChart(7);
  renderDonut();
  animateCounter(document.getElementById("tw2TopicMentions"), 24596);
  setLastUpdated();
})();
</script>
