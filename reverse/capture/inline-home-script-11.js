
(function(){
  var END = 1786687200000;
  var UTM = '?utm_source=site&utm_medium=banner&utm_campaign=seedance25_unlimited';
  var bar  = document.getElementById('acbBar');
  var hero = document.getElementById('acbHero');

  document.querySelectorAll('[data-cta]').forEach(function(a){ a.href += UTM; });

  var fixedEls = [], navH = 0;
  document.querySelectorAll('*').forEach(function(el){
    if(el === bar) return;
    if(hero && (el === hero || hero.contains(el))) return;
    var cs = getComputedStyle(el);
    if(cs.position === 'fixed' && parseInt(cs.top,10) === 0){
      fixedEls.push(el);
      if(el.offsetHeight > navH && el.offsetHeight < 200) navH = el.offsetHeight;
    }
  });

  function offset(){
    var h = (bar && bar.style.display !== 'none') ? bar.offsetHeight : 0;
    document.body.style.paddingTop = h ? h + 'px' : '';
    fixedEls.forEach(function(el){ el.style.top = h ? h + 'px' : ''; });
    if(hero) hero.style.marginTop = (navH + 24) + 'px';
  }

  function tick(){
    var ms = END - Date.now();
    if(ms <= 0){
      if(bar)  bar.style.display  = 'none';
      if(hero) hero.style.display = 'none';
      offset();
      return;
    }
    var s = Math.floor(ms/1000);
    var d = Math.floor(s/86400);
    var h = Math.floor(s%86400/3600);
    var m = Math.floor(s%3600/60);
    var sec = s%60;
    document.querySelectorAll('[data-cd]').forEach(function(el){
      var k = el.getAttribute('data-cd');
      if(k === 'compact'){
        el.textContent = d>0 ? d+'d '+h+'h '+m+'m'
                             : h+'h '+m+'m '+String(sec).padStart(2,'0')+'s';
      }
      if(k === 'd') el.textContent = d;
      if(k === 'h') el.textContent = h;
      if(k === 'm') el.textContent = m;
    });
    if(bar)  bar.style.display  = 'flex';
    if(hero) hero.style.display = 'block';
  }

  tick();
  offset();
  setInterval(tick, 1000);
  window.addEventListener('resize', offset);
})();
