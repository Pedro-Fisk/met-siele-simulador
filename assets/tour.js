/* ─────────────────────────────────────────────────────────────────────────
   FiskTour — tour guiado de primeiro acesso (spotlight + painéis), em PT.
   Sem dependências, CSP-safe, tema claro/escuro. Usado no portal e em cada
   ferramenta. Cada passo: { el:'#sel'|null, title, html, placement? }.
     FiskTour.mount(steps, {key})  → roda na primeira visita + botão "❓" p/ rever
     FiskTour.start(steps, {key})  → roda agora
     FiskTour.seen(key) / FiskTour.reset(key)
   Passo com el:null (ou elemento ausente/oculto) vira um cartão central.
   ───────────────────────────────────────────────────────────────────────── */
(function(){
  'use strict';
  if (window.FiskTour) return;
  var PREFIX = 'fisk_tour_';

  var CSS = ''
  + '.ftour-mask{position:fixed;inset:0;z-index:99998;pointer-events:auto}'
  + '.ftour-hi{position:fixed;z-index:99998;border-radius:12px;box-shadow:0 0 0 9999px rgba(15,12,12,.66);'
  +   'transition:all .25s cubic-bezier(.4,0,.2,1);pointer-events:none;outline:3px solid #c9922e;outline-offset:2px}'
  + '.ftour-card{position:fixed;z-index:99999;max-width:330px;width:calc(100vw - 2.4rem);'
  +   'background:#fff;color:#161414;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.35);'
  +   "font-family:'Nunito',system-ui,sans-serif;padding:1.15rem 1.2rem 1rem;transition:all .2s ease}"
  + '.ftour-dark .ftour-card{background:#211e1e;color:#f2efef}'
  + '.ftour-step{font-size:.68rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#c9922e;margin-bottom:.35rem}'
  + ".ftour-card h3{font-family:'Poppins',system-ui,sans-serif;font-size:1.08rem;font-weight:800;margin:0 0 .4rem;line-height:1.25}"
  + '.ftour-card p{font-size:.9rem;line-height:1.55;margin:0;color:inherit}'
  + '.ftour-card p b{color:#c9922e}'
  + '.ftour-actions{display:flex;align-items:center;gap:.5rem;margin-top:1rem}'
  + '.ftour-skip{background:none;border:none;color:#9a9494;font-family:inherit;font-weight:700;font-size:.8rem;cursor:pointer;padding:.3rem 0;margin-right:auto}'
  + '.ftour-skip:hover{color:#6f6a6a}'
  + '.ftour-btn{border:none;cursor:pointer;font-family:inherit;font-weight:800;font-size:.85rem;border-radius:999px;padding:.5rem 1.1rem;transition:transform .1s}'
  + '.ftour-btn:active{transform:scale(.95)}'
  + '.ftour-prev{background:transparent;color:#6f6a6a;border:1.5px solid #ececec;padding:.5rem .9rem}'
  + '.ftour-dark .ftour-prev{border-color:#3a3535;color:#b5aeae}'
  + '.ftour-next{background:#c9922e;color:#fff}'
  + '.ftour-arrow{position:fixed;z-index:99999;width:0;height:0;transition:all .2s ease}'
  + '.ftour-help{position:fixed;right:1rem;bottom:1rem;z-index:9990;width:2.7rem;height:2.7rem;border-radius:50%;'
  +   'border:none;cursor:pointer;background:#c9922e;color:#fff;font-size:1.15rem;font-weight:800;'
  +   'box-shadow:0 6px 18px rgba(201,146,46,.45);display:flex;align-items:center;justify-content:center}'
  + '.ftour-help:hover{transform:translateY(-2px)}'
  + '@media (max-width:520px){.ftour-card{max-width:none;left:1.2rem!important;right:1.2rem!important;width:auto}}';

  function injectCSS(){
    if (document.getElementById('ftour-css')) return;
    var s = document.createElement('style'); s.id='ftour-css'; s.textContent=CSS;
    document.head.appendChild(s);
  }
  function isDark(){ return document.body.classList.contains('theme-dark'); }
  function visible(el){
    if(!el) return false;
    if(el.hasAttribute('hidden')) return false;
    var r = el.getBoundingClientRect();
    if(r.width===0 && r.height===0) return false;
    var st = getComputedStyle(el);
    return st.display!=='none' && st.visibility!=='hidden';
  }

  function Runner(steps, opts){
    this.steps = steps.slice();
    this.opts = opts||{};
    this.i = 0;
    this.mask=null; this.hi=null; this.card=null;
    this._onKey=this._key.bind(this); this._onResize=this._reposition.bind(this);
  }
  Runner.prototype.run = function(){
    injectCSS();
    document.body.classList.toggle('ftour-dark', isDark());
    this.mask = document.createElement('div'); this.mask.className='ftour-mask';
    this.hi = document.createElement('div'); this.hi.className='ftour-hi'; this.hi.style.opacity='0';
    this.card = document.createElement('div'); this.card.className='ftour-card';
    document.body.appendChild(this.mask); document.body.appendChild(this.hi); document.body.appendChild(this.card);
    this.mask.addEventListener('click', this._skip.bind(this));
    document.addEventListener('keydown', this._onKey);
    window.addEventListener('resize', this._onResize);
    this.show();
  };
  Runner.prototype._resolve = function(step){
    var el = step.el ? (typeof step.el==='string' ? document.querySelector(step.el) : step.el) : null;
    return (el && visible(el)) ? el : null;
  };
  Runner.prototype.show = function(){
    var self=this, step=this.steps[this.i], el=this._resolve(step);
    var inView = false;
    if(el){
      var r=el.getBoundingClientRect();
      inView = r.top>=0 && r.bottom<=innerHeight;
      if(!inView){ try{ el.scrollIntoView({block:'center', inline:'nearest'}); }catch(e){ el.scrollIntoView(); } }
    }
    if(el && !inView) setTimeout(function(){ self._render(step, self._resolve(step)); }, 200);
    else self._render(step, el);
  };
  Runner.prototype._render = function(step, el){
    var last = this.i===this.steps.length-1, first = this.i===0;
    this.card.innerHTML =
      '<div class="ftour-step">Passo '+(this.i+1)+' de '+this.steps.length+'</div>'+
      '<h3>'+step.title+'</h3><p>'+step.html+'</p>'+
      '<div class="ftour-actions">'+
        '<button class="ftour-skip">Pular tour</button>'+
        (first?'':'<button class="ftour-btn ftour-prev">Voltar</button>')+
        '<button class="ftour-btn ftour-next">'+(last?'Concluir ✓':'Próximo →')+'</button>'+
      '</div>';
    this.card.querySelector('.ftour-skip').onclick = this._skip.bind(this);
    this.card.querySelector('.ftour-next').onclick = this._next.bind(this);
    var prev=this.card.querySelector('.ftour-prev'); if(prev) prev.onclick=this._prev.bind(this);
    this._place(el);
  };
  Runner.prototype._place = function(el){
    var card=this.card, hi=this.hi, vw=innerWidth, vh=innerHeight, gap=14, pad=6;
    if(!el){
      hi.style.opacity='0'; hi.style.width='0'; hi.style.height='0';
      card.style.left=Math.max(12,(vw-card.offsetWidth)/2)+'px';
      card.style.top=Math.max(12,(vh-card.offsetHeight)/2)+'px';
      return;
    }
    var r=el.getBoundingClientRect();
    hi.style.opacity='1';
    hi.style.left=(r.left-pad)+'px'; hi.style.top=(r.top-pad)+'px';
    hi.style.width=(r.width+pad*2)+'px'; hi.style.height=(r.height+pad*2)+'px';
    var ch=card.offsetHeight, cw=card.offsetWidth;
    var below=r.bottom+gap, above=r.top-gap-ch;
    var top = (vh-r.bottom > ch+gap+10) ? below : (above>10 ? above : Math.max(12,(vh-ch)/2));
    var left = Math.min(Math.max(12, r.left+r.width/2 - cw/2), vw-cw-12);
    if(vw<=520){ left=null; }         // CSS fixa left/right em telas pequenas
    if(left!==null) card.style.left=left+'px';
    card.style.top=top+'px';
  };
  Runner.prototype._reposition = function(){ this._place(this._resolve(this.steps[this.i])); };
  Runner.prototype._key = function(e){
    if(e.key==='Escape') this._skip();
    else if(e.key==='ArrowRight'||e.key==='Enter') this._next();
    else if(e.key==='ArrowLeft') this._prev();
  };
  Runner.prototype._next = function(){ if(this.i<this.steps.length-1){ this.i++; this.show(); } else this._finish(); };
  Runner.prototype._prev = function(){ if(this.i>0){ this.i--; this.show(); } };
  Runner.prototype._skip = function(){ this._finish(); };
  Runner.prototype._finish = function(){
    document.removeEventListener('keydown', this._onKey);
    window.removeEventListener('resize', this._onResize);
    [this.mask,this.hi,this.card].forEach(function(n){ if(n&&n.parentNode) n.parentNode.removeChild(n); });
    if(this.opts.key){ try{ localStorage.setItem(PREFIX+this.opts.key,'1'); }catch(e){} }
    if(typeof this.opts.onDone==='function') this.opts.onDone();
  };

  var API = {
    start: function(steps, opts){ new Runner(steps, opts).run(); },
    seen: function(key){ try{ return localStorage.getItem(PREFIX+key)==='1'; }catch(e){ return false; } },
    reset: function(key){ try{ localStorage.removeItem(PREFIX+key); }catch(e){} },
    startIfFirst: function(steps, opts){ if(!API.seen(opts.key)) API.start(steps, opts); },
    /* roda na 1ª visita + adiciona botão flutuante "❓" para rever quando quiser */
    mount: function(steps, opts){
      opts = opts||{};
      injectCSS();
      if(!opts.noButton && !document.querySelector('.ftour-help[data-key="'+opts.key+'"]')){
        var b=document.createElement('button'); b.className='ftour-help'; b.setAttribute('data-key',opts.key||'');
        b.title='Ver o tour de novo'; b.textContent='❓';
        b.onclick=function(){ API.start(steps, opts); };
        document.body.appendChild(b);
      }
      var delay = opts.delay||500;
      if(!API.seen(opts.key)) setTimeout(function(){ API.start(steps, opts); }, delay);
    }
  };
  window.FiskTour = API;
})();
