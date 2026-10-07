'use strict';
(() => {
  const D = JSON.parse(document.getElementById('workshop-data').textContent);
  const R = D.resources;
  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => [...root.querySelectorAll(s)];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const paras = text => String(text).split('\n\n').map(p=>`<p>${esc(p)}</p>`).join('');
  const sourceMap = Object.fromEntries(D.sources.map(s=>[s.id,s]));
  const source = id => sourceMap[id];
  const sourceLink = (id, title) => {const s=source(id);return s ? `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(title || s.title)} ↗</a>` : `<span>Reference unavailable</span>`;};
  const goodURL = u => {try{return new URL(u).protocol==='https:';}catch{return false;}};
  const external = (u,title) => goodURL(u)?`<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(title)} ↗</a>`:esc(title);
  const storageKey = 'sds-work-visible-v1';
  const S = {view:'session',slide:1,guide:'start',artifact:'collection',lens:'All',query:'',kit:'Builder',readAll:false,present:false,duration:40,showAll:false,model:0,readme:'before',message:'confirmed',help:{},work:{start:'',title:'',status:'planned'},remember:false};
  const timers = {};
  const timerInfo = {
    inventory:{seconds:90,presets:[45,90,120],name:'Write your notes'},
    'shared-fluency':{seconds:120,presets:[60,120,180],name:'Table discussion'},
    'own-fluency':{seconds:180,presets:[120,180,240],name:'Your learning move'},
    'shared-legibility':{seconds:120,presets:[60,120,180],name:'Compare your questions'},
    'own-legibility':{seconds:180,presets:[120,180,240],name:'Your explanation'},
    reach:{seconds:90,presets:[60,90,120],name:'Your opening sentences'},
    work:{seconds:420,presets:[300,420,660],name:'Independent work'},
    peer:{seconds:180,presets:[180,240],name:'Read, explain, revise'}
  };
  let dialogOpener=null, toastTimeout=null, copiedText='';
  const dialog=$('#dialog');
  function notify(text){const el=$('#notification');el.textContent=text;el.hidden=false;clearTimeout(toastTimeout);toastTimeout=setTimeout(()=>{el.hidden=true;},4500);}
  function validateWork(x){
    if(!x || typeof x!=='object' || !R.starts.some(s=>s.id===x.start) && x.start!=='') throw new Error('Choose a recognized starting condition.');
    if(typeof x.title!=='string' || x.title.length>180) throw new Error('The work title must be text of 180 characters or fewer.');
    if(!['planned','started','observed'].includes(x.status)) throw new Error('The work status is not recognized.');
    return {start:x.start,title:x.title.trim(),status:x.status};
  }
  function loadWork(){try{const raw=localStorage.getItem(storageKey);if(raw){const x=JSON.parse(raw);if(x.schema!==1)throw new Error();S.work=validateWork(x.work);S.remember=true;}}catch{S.remember=false;}}
  function storeWork(){try{if(S.remember)localStorage.setItem(storageKey,JSON.stringify({schema:1,work:S.work}));else localStorage.removeItem(storageKey);return true;}catch{S.remember=false;notify('Browser storage is unavailable. Your title remains in this open page; export a work card to keep it.');return false;}}
  function workLabel(){return S.work.title || (S.work.start ? R.starts.find(s=>s.id===S.work.start).label : 'Keep your circled note or chosen question beside you.');}
  function renderOwn(){
    $$('[data-own-work]').forEach(el=>{el.innerHTML=`<div class="own-work"><span><b>Your work today:</b> ${esc(workLabel())}${S.work.title?`<small>${{planned:'A plan or question',started:'Work in progress',observed:'Work with an observed result'}[S.work.status]}</small>`:''}</span><button class="textbutton" data-action="work-card">${S.work.title?'Edit':'Add a title'}</button></div>`;});
    $$('[data-start-options]').forEach(el=>{el.innerHTML=R.starts.map(x=>`<button data-start="${x.id}" aria-pressed="${S.work.start===x.id}">${esc(x.label)}</button>`).join('');});
    renderRoutes();renderRecommendations();
  }
  function selectStart(id){if(!R.starts.some(x=>x.id===id))return;S.work.start=id;S.showAll=false;storeWork();renderOwn();renderAllHelp();notify(R.starts.find(x=>x.id===id).first);}
  function pauseTimers(){Object.values(timers).forEach(t=>{if(t.running){t.remaining=Math.max(0,Math.ceil((t.deadline-Date.now())/1000));t.running=false;}});renderTimers();}
  function timeRange(n){let a=0;D.session.slice(0,n-1).forEach(x=>a+=minutes(x));return `${a}:00–${a+minutes(D.session[n-1])}:00`;}
  function minutes(scene){return scene.minutes+(S.duration===45?(scene.number===12?4:scene.number===13?1:0):0);}
  function refreshSceneContext(){D.session.forEach(s=>{const el=$(`[data-scene="${s.number}"] .scene-context`);if(el)el.innerHTML=`<b>${esc(s.theme)}</b><span class="mode">${esc(s.kind)}</span><span>${timeRange(s.number)}</span>`;});}
  function applyView(view,sub,focus=true){
    if(!['session','work','guide','artifact'].includes(view))view='session';
    if(S.view!==view)pauseTimers();S.view=view;
    ['session','work','guide','artifact'].forEach(x=>$(`#${x}-view`).hidden=x!==view);
    $$('.mainnav button').forEach(x=>{const is=(x.dataset.view===view)||(x.dataset.artifact&&view==='artifact');is?x.setAttribute('aria-current','page'):x.removeAttribute('aria-current');});
    if(view==='session')setSlide(Number(sub)||S.slide,false);
    if(view==='work')renderRoutes();
    if(view==='guide'){S.guide=D.guides[sub]?sub:S.guide;renderGuide();}
    if(view==='artifact'){S.artifact=['collection','writing','readings'].includes(sub)?sub:S.artifact;renderArtifact();}
    if(focus){window.scrollTo(0,0);$('#main').focus({preventScroll:true});}
  }
  function navigate(view,sub){closeDialog();applyView(view,sub);const h='#'+view+(sub?'/'+encodeURIComponent(sub):'');try{if(location.hash!==h)history.pushState(null,'',h);}catch{location.hash=h;}}
  function readHash(){const parts=location.hash.slice(1).split('/');let sub='';try{sub=decodeURIComponent(parts[1]||'');}catch{}applyView(parts[0]||document.body.dataset.default||'session',sub,false);}
  function setSlide(n,update=true){n=Math.max(1,Math.min(D.session.length,Number.isFinite(n)?n:1));if(n!==S.slide)pauseTimers();S.slide=n;
    $$('.slide').forEach((el,i)=>el.hidden=!S.readAll && i+1!==n);
    $('#slide-count').textContent=`${String(n).padStart(2,'0')} / ${D.session.length}`;
    $('#slide-progress').style.width=(n/D.session.length*100)+'%';
    $('#previous').disabled=n===1;$('#next').disabled=n===D.session.length;
    const theme=D.session[n-1].theme;$$('#chapter-nav button').forEach(x=>x.dataset.theme===theme?x.setAttribute('aria-current','step'):x.removeAttribute('aria-current'));
    if(update){if(S.view!=='session'){navigate('session',String(n));return;}if(S.readAll)$(`[data-scene="${n}"]`).scrollIntoView();else window.scrollTo(0,0);try{history.pushState(null,'',`#session/${n}`);}catch{}$('#main').focus({preventScroll:true});}
  }
  function openDialog(title,html){
    if(!dialog.open)dialogOpener=document.activeElement;
    $('#dialog-title').textContent=title;$('#dialog-body').innerHTML=html;
    if(!dialog.open)dialog.showModal();dialog.scrollTop=0;$('.dialog-close').focus();
    secureLinks(dialog);
  }
  function closeDialog(){if(dialog.open)dialog.close();}
  dialog.addEventListener('close',()=>{if(dialogOpener?.isConnected)dialogOpener.focus({preventScroll:true});else $('#main').focus({preventScroll:true});dialogOpener=null;});
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog();}});
  function secureLinks(root=document){$$('a[href]',root).forEach(a=>{if(/^https:\/\//.test(a.getAttribute('href'))){a.target='_blank';a.rel='noopener noreferrer';}});}
  function openWorkCard(){openDialog('Keep a title for your work',`<p>This optional card keeps your starting condition and a brief title visible between activities. Your project and exercise notes stay in your own file or on paper.</p><form id="work-form"><label class="dialog-field">Starting condition<select name="start" id="work-start"><option value="">Choose a starting condition</option>${R.starts.map(s=>`<option value="${s.id}" ${s.id===S.work.start?'selected':''}>${esc(s.label)}</option>`).join('')}</select></label><label class="dialog-field">A brief, nonsensitive title<input id="work-title" name="title" maxlength="180" value="${esc(S.work.title)}" placeholder="For example: how to evaluate music recommendations"></label><label class="dialog-field">What stage is the work in?<select id="work-status" name="status">${[['planned','A plan or question'],['started','Work in progress'],['observed','Work with an observed result']].map(([v,t])=>`<option value="${v}" ${v===S.work.status?'selected':''}>${t}</option>`).join('')}</select></label><label class="checkline"><input type="checkbox" id="remember" ${S.remember?'checked':''}><span>Remember this card in this browser. Leave unchecked on a shared computer. Browser storage can be cleared; an export is a separate backup.</span></label><div class="buttonrow"><button class="button" type="submit">Use this card</button><button class="button secondary" type="button" data-action="export-card">Export card</button><button class="textbutton" type="button" data-action="import-card">Import card</button></div><p class="small">The export contains only this card, not your repository, assignment, or answers.</p><div class="dialog-section"><button class="textbutton" type="button" data-action="clear-card">Clear my card and browser copy</button></div></form>`);}
  function download(text,name,type='text/plain;charset=utf-8'){const b=new Blob([text],{type}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),15000);}
  function workbook(){return `# My work today\n\nSDS Career Services · Make Your Work Visible\n\n**Selected work:** ${S.work.title||'[Name the assignment, project, question, or task you selected.]'}\n**Starting condition:** ${R.starts.find(x=>x.id===S.work.start)?.label||'[Choose your starting condition.]'}\n**Status:** ${S.work.status}\n\nKeep this same work in view throughout the session. This worksheet is optional; you can write in your own notes instead.\n\n## Fluency: my learning move\nWhat have I already done?\n\nWhat do I want to understand, compare, or practice next?\n\nWhat is a first action I can take with the time and access I have?\n\n## Legibility: my project explanation\nWhat problem or question am I addressing?\n\nWhat approach did I use or plan to use, and what is my contribution?\n\nWhat happened, what is still planned, and what does it mean?\n\nWhat evidence can a reader inspect?\n\n## Reach: an introduction\nWho might have a genuine reason to discuss this work?\n\nMy two opening sentences:\n\n## Work time\nThe change or first step I will attempt now:\n\nWhere I will do it:\n\n## Reader feedback\nI understand ...\n\nI am still looking for ...\n\nA decision I explained without reading the template:\n\nOne revision I made:\n\n## After today\nMy next action:\n\nWhere I saved the actual work:\n\nNo new account, public posting, or paid tool is required. This file does not contain your work from other tools.\n`;}
  function openText(title,text,filename){copiedText=text;openDialog(title,`<p class="small">Use what fits your actual work. Keep plans, attempts, and observed results distinct.</p><textarea class="dialog-code" id="copy-text" readonly aria-label="${esc(title)}">${esc(text)}</textarea><div class="buttonrow"><button class="button" data-action="copy-text">Copy text</button><button class="button secondary" data-save-text="${esc(filename)}">Save Markdown</button><button class="textbutton" data-action="select-text">Select text</button></div><p id="copy-status" class="status-message" role="status"></p>`);}
  async function copyText(){const t=$('#copy-text');try{if(!navigator.clipboard)throw Error();await navigator.clipboard.writeText(t.value);$('#copy-status').textContent='Copied to your clipboard.';}catch{t.focus();t.select();$('#copy-status').textContent='Clipboard access is unavailable. The text is selected; copy it with your keyboard or save the Markdown file.';}}
  function renderHelp(id){const el=$(`[data-help="${id}"]`),h=R.help[id];if(!el||!h)return;const level=S.help[id]||'task';const options=[['task','I’ve got it'],['nudge','Give me a nudge'],['example','Show me an example']];
    let content='';if(level==='nudge'){const ns=id==='own-fluency'&&S.work.start?R.state_nudges[S.work.start]:h.nudge;content=`<p class="help-title">Questions to help you begin</p><ul>${ns.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`;}
    if(level==='example')content=`<p class="help-title">An example, not your answer</p><p>${esc(h.example)}</p>${id==='object'?'<button class="textbutton" data-action="use-example">Use this question as my starting point</button>':''}`;
    el.className='help';el.innerHTML=`<div class="help-buttons" role="group" aria-label="Choose support for this activity">${options.map(([v,t])=>`<button data-help-id="${id}" data-help-level="${v}" aria-pressed="${level===v}" aria-controls="help-panel-${id}">${t}</button>`).join('')}</div><div class="help-panel" id="help-panel-${id}" ${level==='task'?'hidden':''}>${content}</div>`;
  }
  function renderAllHelp(){Object.keys(R.help).forEach(renderHelp);}
  function initTimers(){Object.entries(timerInfo).forEach(([id,i])=>{timers[id]={duration:i.seconds,remaining:i.seconds,running:false,deadline:0,done:false};const el=$(`[data-timer="${id}"]`);el.className='timer';el.innerHTML=`<div class="timer-label">${i.name}</div><div class="timer-display" role="timer" aria-label="${i.name} remaining" aria-live="off"></div><div class="timer-buttons"><button data-timer-toggle="${id}" aria-label="Start ${i.name.toLowerCase()}">Start</button><button data-timer-reset="${id}" aria-label="Reset ${i.name.toLowerCase()}">Reset</button></div><div class="timer-presets" aria-label="Timer duration">${i.presets.map(n=>`<button data-timer-id="${id}" data-seconds="${n}">${n%60?n+' sec':(n/60)+' min'}</button>`).join('')}</div><p class="timer-status" role="status"></p>`;});renderTimers();}
  function fmt(n){return `${Math.floor(n/60)}:${String(n%60).padStart(2,'0')}`;}
  function setTimer(id,seconds){const t=timers[id];if(!t)return;t.running=false;t.duration=seconds;t.remaining=seconds;t.done=false;renderTimers();}
  function toggleTimer(id){const t=timers[id];if(t.running){t.remaining=Math.max(0,Math.ceil((t.deadline-Date.now())/1000));t.running=false;}else{if(t.remaining<=0)t.remaining=t.duration;t.deadline=Date.now()+t.remaining*1000;t.running=true;t.done=false;}renderTimers();}
  function renderTimers(){Object.entries(timers).forEach(([id,t])=>{const el=$(`[data-timer="${id}"]`);$('.timer-display',el).textContent=fmt(t.remaining);const b=$('[data-timer-toggle]',el);b.textContent=t.running?'Pause':t.remaining<=0?'Restart':t.remaining!==t.duration?'Resume':'Start';b.setAttribute('aria-label',`${b.textContent} ${timerInfo[id].name.toLowerCase()}`);el.classList.toggle('expired',t.done);const text=t.done?'Time to compare, revise, or continue.':t.running?'Running in this browser.':t.remaining!==t.duration?'Paused.':'Ready when you are.';if($('.timer-status',el).textContent!==text)$('.timer-status',el).textContent=text;});updatePeer();}
  function updatePeer(){const t=timers.peer;if(!t)return;const elapsed=t.duration-t.remaining;let text;if(elapsed===0)text=t.duration>=240?'Each partner has 90 seconds; both use the last minute to revise.':'Each partner has one minute; both use the last minute to revise.';else{const round=(t.duration-60)/2;text=elapsed<round?'Partner A: read first, give specific feedback, then hear one decision.':elapsed<2*round?'Partner B: switch roles and repeat.':t.remaining>0?'Both authors: revise one thing in your work.':'Save the revision and return to the room.';}if($('#peer-phase').textContent!==text)$('#peer-phase').textContent=text;}
  setInterval(()=>{let changed=false;Object.values(timers).forEach(t=>{if(t.running){const n=Math.max(0,Math.ceil((t.deadline-Date.now())/1000));if(n!==t.remaining){t.remaining=n;changed=true;}if(n===0){t.running=false;t.done=true;}}});if(changed)renderTimers();},250);
  function setDuration(n){S.duration=n===45?45:40;setTimer('work',S.duration===45?660:420);setTimer('peer',S.duration===45?240:180);refreshSceneContext();$('.deck-tools [data-action=settings]').textContent=S.duration+' min';notify(`Using the ${S.duration}-minute plan. Work and peer timers have been reset.`);}
  function renderModel(){const m=R.model[S.model];$('#model-steps').innerHTML=R.model.map((x,i)=>`<button data-model="${i}" aria-pressed="${i===S.model}">${i+1}. ${esc(x.title)}</button>`).join('');$('#model-panel').innerHTML=`<h3>${esc(m.heading)}</h3><p>${esc(m.body)}</p><p class="model-detail">${esc(m.detail)}</p>${S.model===3?'<button class="button secondary" data-download="measurement-brief">Read the example brief</button>':''}`;}
  function renderReadme(){const r=R.readme[S.readme];$('#readme-title').textContent=r.title;$('#readme-text').innerHTML=r.paragraphs.map(x=>`<p>${esc(x)}</p>`).join('');$('#readme-criteria').innerHTML=R.criteria.map((x,i)=>`<article class="criterion"><h3>${esc(x)}</h3><p>${esc(r.checks[i])}</p></article>`).join('');$$('[data-readme]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.readme===S.readme));}
  function renderMessage(){const m=R.messages[S.message];$('#message-title').textContent=m.title;$('#message-copy').innerHTML=paras(m.text);$('#message-framework').textContent=m.framework;$$('[data-message]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.message===S.message));}
  function recommended(){return (R.starts.find(s=>s.id===S.work.start)||R.starts.find(s=>s.id==='new')).routes.map(id=>R.routes.find(r=>r.id===id));}
  function renderRecommendations(){$('#work-recommendations').innerHTML=recommended().map(r=>`<article class="recommendation"><h3>${esc(r.title)}</h3><p>${esc(r.why)}</p><button class="textbutton" data-route="${r.id}">See steps</button></article>`).join('');}
  function renderRoutes(){const selected=R.starts.find(s=>s.id===S.work.start),rs=S.showAll?R.routes:recommended();$('#route-summary').textContent=S.showAll?'All ten options are available. Keep the work you selected in mind.':selected?`Three suggestions for your starting condition. ${selected.first}`:'Start with one of these suggestions, or choose a starting condition above.';$('#all-routes').textContent=S.showAll?'Return to my suggestions':'Show all ten options';$('#all-routes').setAttribute('aria-pressed',S.showAll);$('#route-grid').innerHTML=rs.map(r=>`<article class="route-card"><h2>${esc(r.title)}</h2><p>${esc(r.why)}</p><p class="route-done"><b>What you can leave with:</b> ${esc(r.done)}</p><button class="button secondary" data-route="${r.id}">Open the steps</button></article>`).join('');}
  function openRoute(id){const r=R.routes.find(x=>x.id===id);if(!r)return;openDialog(r.title,`<p>${esc(r.why)}</p><p><b>Where to work:</b> ${esc(r.where)}</p><ol class="dialog-steps">${r.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol><p class="task-card"><b>A finish line for this attempt:</b> ${esc(r.done)}</p><p class="small"><b>A fallback:</b> ${esc(r.fallback)}</p><div class="buttonrow"><button class="button" data-template="${r.template}">Get the outline</button><button class="button secondary" data-prompt="${r.prompt}">Optional coaching prompt</button></div><div class="dialog-section"><h3>References for this activity</h3>${r.refs.map(id=>`<p class="small">${sourceLink(id)}</p>`).join('')}</div>`);}
  const guideNames={start:'Ways to get started',explaining:'Explain your work',github:'GitHub essentials',permissions:'What you may share',writing:'Introduce your work',tools:'AI and student resources',sources:'Sources and dates',about:'About this edition'};
  function renderGuide(){const id=D.guides[S.guide]?S.guide:'start';S.guide=id;$('#guide-nav').innerHTML=Object.entries(guideNames).map(([k,v])=>`<button data-guide="${k}" ${k===id?'aria-current="page"':''}>${v}</button>`).join('');$('#guide-content').innerHTML=D.guides[id].html;secureLinks($('#guide-content'));
    if(id==='tools')$('#guide-content').insertAdjacentHTML('afterbegin',`<div class="prompt-list">${[['coach','Coach','Help me identify a manageable next learning step.'],['critic','Critic','Ask for missing evidence before rewriting my README.'],['coding','Coding assistant','Help me investigate a bounded change and explain it.'],['pulse','Pulse check','Ask what changed, why, and what comes next.']].map(([k,t,p])=>`<article><h3>${t}</h3><p>${p}</p><button class="button secondary" data-prompt="${k}">Read the prompt</button></article>`).join('')}</div>`);
    if(id==='sources'){const el=$('#source-results');if(el)renderSources();}
    $('#guide-content').insertAdjacentHTML('beforeend','<div class="guide-links"><button class="button secondary" data-action="return">Return to the session</button><button class="textbutton" data-action="export-guide">Save the complete Markdown guide</button></div>');
    wrapTables($('#guide-content'));
  }
  function renderSources(){const q=($('#source-search')?.value||'').toLowerCase();const ss=D.sources.filter(s=>`${s.title} ${s.publisher} ${s.note} ${s.kind}`.toLowerCase().includes(q));$('#source-results').innerHTML=`<p class="result-count" role="status">${ss.length} references</p>`+ss.map(s=>`<article class="source-entry"><p class="source-meta">${esc(s.publisher)} · ${esc(s.checked)}</p><h3>${external(s.url,s.title)}</h3><p>${esc(s.note)}</p></article>`).join('');}
  function wrapTables(root){$$('table',root).forEach(t=>{if(t.parentElement.classList.contains('table-scroll'))return;const div=document.createElement('div');div.className='table-scroll';div.tabIndex=0;div.setAttribute('role','region');div.setAttribute('aria-label','Scrollable reference table');t.before(div);div.appendChild(t);});}
  function renderArtifact(){
    $$('.artifact-tabs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.artifact===S.artifact));const el=$('#artifact-content');
    if(S.artifact==='collection'){el.innerHTML=`<p class="lead">The five perspectives are ways to examine a portfolio, not permanent types you must choose between. This collection includes student-era work and established practitioners; each card explains the distinction.</p><div class="lens-filters" aria-label="Filter by perspective">${['All','Builder','Storyteller','Expert','Researcher','Analyst'].map(x=>`<button data-lens="${x}" aria-pressed="${S.lens===x}">${x}</button>`).join('')}</div><label class="searchfield">Search names, projects, or topics<input id="portfolio-search" type="search" value="${esc(S.query)}" placeholder="For example: music, research, dashboards"></label><div id="portfolio-results"></div>`;renderPortfolios();}
    if(S.artifact==='writing'){el.innerHTML=`<p class="lead">Choose the kind of explanation your reader needs. Each guide keeps the original Artifact’s six-part structure, with questions you can answer from your own evidence.</p><div class="writing-layout"><nav class="writing-nav" aria-label="Writing perspectives">${R.writing_guides.map(g=>`<button data-kit="${g.lens}" aria-pressed="${S.kit===g.lens}">${g.lens}</button>`).join('')}</nav><article id="writing-paper" class="writing-paper"></article></div>`;renderKit();}
    if(S.artifact==='readings'){el.innerHTML=`<p class="lead">These nine selections come from the original Artifact writing kit. Read for the author’s explanatory choices, not for a promise that your project will produce the same career outcome.</p><div class="collection-grid">${R.readings.map(r=>`<article class="reading-card"><p class="eyebrow">${esc(r.lens)}</p><h2>${esc(r.title)}</h2><p>${esc(r.note)}</p><p class="small">${esc(r.status)}</p>${external(r.url,'Read the example')}</article>`).join('')}</div>`;}
  }
  function renderPortfolios(){const q=S.query.toLowerCase();const ps=R.portfolios.filter(p=>(S.lens==='All'||p.lens===S.lens)&&`${p.name} ${p.summary} ${p.projects.join(' ')}`.toLowerCase().includes(q));$('#portfolio-results').innerHTML=`<p class="result-count" role="status">${ps.length} of ${R.portfolios.length} original selections</p><div class="collection-grid">${ps.map(p=>`<button class="portfolio-card" data-portfolio="${p.id}" aria-label="Explore ${esc(p.name)}"><span class="eyebrow">The ${esc(p.lens)}</span><h2>${esc(p.name)}</h2><p class="stage-label">${esc(p.stage)}</p><p>${esc(p.summary)}</p><span class="card-action">Explore the example →</span></button>`).join('')}</div>${ps.length?'':'<p class="no-results">No matches. Try a broader word or choose All.</p>'}`;}
  function openPortfolio(id){const p=R.portfolios.find(p=>p.id===id);if(!p)return;openDialog(p.name,`<p class="eyebrow">The ${esc(p.lens)}</p><p class="small">${esc(p.stage)}</p><p class="lead">${esc(p.summary)}</p><h3>What to look for</h3><p>${esc(p.pattern)}</p><h3>Places to begin</h3><ul>${p.projects.map(t=>`<li>${esc(t)}</li>`).join('')}</ul><p>${external(p.url,'Visit the portfolio or repository')}</p><div class="dialog-section"><p class="small">${esc(p.note)}</p><p class="small">${esc(p.origin)} Reviewed ${esc(p.checked)}.</p><button class="button secondary" data-kit-link="${p.lens}">Open this writing guide</button></div>`);}
  function renderKit(){const g=R.writing_guides.find(x=>x.lens===S.kit)||R.writing_guides[0];$('#writing-paper').innerHTML=`<p class="eyebrow">For ${esc(g.audience.toLowerCase())}</p><h2>${esc(g.title)}</h2><p>${esc(g.description)}</p><div class="table-scroll" tabindex="0" role="region" aria-label="Writing guide structure"><table><thead><tr><th>Section</th><th>What to include</th><th>How it helps the reader</th></tr></thead><tbody>${g.rows.map(r=>`<tr><td>${esc(r.section)}</td><td>${esc(r.include)}</td><td>${esc(r.reason)}</td></tr>`).join('')}</tbody></table></div><div class="buttonrow"><button class="button" data-kit-template="${g.lens}">Get the Markdown outline</button><button class="textbutton" data-artifact="readings">Browse writing examples →</button></div><p class="small" style="margin-top:18px">${esc(g.origin)}</p>`;$$('[data-kit]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.kit===S.kit));}
  function contents(){let html='';[...new Set(D.session.map(s=>s.theme))].forEach(theme=>{html+=`<section class="contents-group"><h3>${esc(theme)}</h3>${D.session.filter(s=>s.theme===theme).map(s=>`<button data-jump="${s.number}"><span>${String(s.number).padStart(2,'0')}</span>${esc(s.title)}<span>${timeRange(s.number)}</span></button>`).join('')}</section>`;});openDialog('The workshop sequence',html);}
  document.addEventListener('click',e=>{
    const b=e.target.closest('button, a[data-source-link]');if(!b)return;
    if(b.dataset.view){navigate(b.dataset.view);return;}
    if(b.dataset.jump){closeDialog();navigate('session',b.dataset.jump);return;}
    if(b.dataset.guide){navigate('guide',b.dataset.guide);return;}
    if(b.dataset.artifact){navigate('artifact',b.dataset.artifact);return;}
    if(b.dataset.start){selectStart(b.dataset.start);return;}
    if(b.dataset.helpId){const id=b.dataset.helpId;S.help[id]=b.dataset.helpLevel;renderHelp(id);$(`[data-help-id="${id}"][data-help-level="${S.help[id]}"]`).focus({preventScroll:true});return;}
    if(b.dataset.timerToggle){toggleTimer(b.dataset.timerToggle);return;}
    if(b.dataset.timerReset){setTimer(b.dataset.timerReset,timers[b.dataset.timerReset].duration);return;}
    if(b.dataset.seconds){setTimer(b.dataset.timerId,Number(b.dataset.seconds));return;}
    if(b.dataset.model!==undefined){S.model=Number(b.dataset.model);renderModel();$(`[data-model="${S.model}"]`).focus({preventScroll:true});return;}
    if(b.dataset.readme){S.readme=b.dataset.readme;renderReadme();return;}
    if(b.dataset.message){S.message=b.dataset.message;renderMessage();return;}
    if(b.dataset.route){openRoute(b.dataset.route);return;}
    if(b.dataset.pdf){const item=D.printables?.[b.dataset.pdf];if(item){const binary=atob(item.base64);const bytes=Uint8Array.from(binary,c=>c.charCodeAt(0));download(bytes,item.name,'application/pdf');}else notify('Use the PDF from the release package.');return;}
    if(b.dataset.template){const t=R.templates[b.dataset.template];if(t)openText('Project outline',t,`${b.dataset.template}-outline.md`);return;}
    if(b.dataset.prompt){const t=R.prompts[b.dataset.prompt];if(t)openText('Optional AI coaching prompt',t,`${b.dataset.prompt}-prompt.md`);return;}
    if(b.dataset.saveText){download($('#copy-text').value,b.dataset.saveText,'text/markdown;charset=utf-8');return;}
    if(b.dataset.download){if(b.dataset.download==='workbook')download(workbook(),'my-work-today.md','text/markdown;charset=utf-8');else if(b.dataset.download==='measurement-brief')openText('The example measurement brief',D.measurement,'music-recommendations-brief.md');return;}
    if(b.dataset.lens){S.lens=b.dataset.lens;$$('[data-lens]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.lens===S.lens));renderPortfolios();return;}
    if(b.dataset.portfolio){openPortfolio(b.dataset.portfolio);return;}
    if(b.dataset.kit){S.kit=b.dataset.kit;renderKit();return;}
    if(b.dataset.kitLink){S.kit=b.dataset.kitLink;navigate('artifact','writing');return;}
    if(b.dataset.kitTemplate){const g=R.writing_guides.find(x=>x.lens===b.dataset.kitTemplate);openText(g.title,g.template,`${g.lens.toLowerCase()}-writing-outline.md`);return;}
    if(b.dataset.duration){setDuration(Number(b.dataset.duration));closeDialog();return;}
    if(b.id==='all-routes'){S.showAll=!S.showAll;renderRoutes();return;}
    const action=b.dataset.action;if(!action)return;
    if(action==='close')closeDialog();
    if(action==='return')navigate('session',String(S.slide));
    if(action==='work-router')navigate('work');
    if(action==='work-card')openWorkCard();
    if(action==='contents')contents();
    if(action==='use-example'){if(S.work.title&&!window.confirm('Replace your current title with the music-recommendation question?'))return;S.work={start:'curiosity',title:'How could I evaluate whether music recommendations are useful?',status:'planned'};storeWork();renderOwn();renderAllHelp();notify('Keep this question in view. You can adapt it as you learn.');}
    if(action==='speaker'){const s=D.session[S.slide-1];openDialog(`Slide ${s.number} · ${s.kind}`,`<p class="eyebrow">${timeRange(s.number)} of Reggie’s segment</p><p class="lead">${esc(s.say)}</p><ul>${s.actions.map(a=>`<li>${esc(a)}</li>`).join('')}</ul><p class="dialog-section"><b>Transition:</b> ${esc(s.transition)}</p>`);}
    if(action==='read-all'){S.readAll=!S.readAll;document.body.classList.toggle('read-all',S.readAll);b.setAttribute('aria-pressed',S.readAll);b.textContent=S.readAll?'Slide view':'Read all';pauseTimers();setSlide(S.slide,false);}
    if(action==='present'){S.present=!S.present;document.body.classList.toggle('presenting',S.present);b.setAttribute('aria-pressed',S.present);b.textContent=S.present?'Exit present':'Present';notify(S.present?'Personal work titles and route selections are hidden while presenting.':'Personal work cards are visible again.');}
    if(action==='settings')openDialog('Session timing and display',`<p>The 40-minute plan follows the approved sequence. The 45-minute option adds four minutes to independent work and one to peer review. Changing plans resets those two timers.</p><div class="buttonrow"><button class="button" data-duration="40">40 minutes</button><button class="button secondary" data-duration="45">45 minutes</button><button class="textbutton" data-action="fullscreen">Enter full screen</button></div><p class="small">Use the arrow keys to change slides. Home and End go to the opening and close. Keys do not change slides while you are typing or a dialog is open. Timers are local to this browser and pause when you leave an activity.</p>`);
    if(action==='fullscreen'){closeDialog();if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>notify('Full screen is unavailable here. Use your browser’s full-screen control.'));else notify('Use your browser’s full-screen control on this device.');}
    if(action==='copy-text')copyText();
    if(action==='select-text'){$('#copy-text').focus();$('#copy-text').select();}
    if(action==='export-guide')download(D.fieldMarkdown,'make-your-work-visible-field-guide.md','text/markdown;charset=utf-8');
    if(action==='export-card'){let card=S.work;if($('#work-title')){try{card=validateWork({start:$('#work-start').value,title:$('#work-title').value,status:$('#work-status').value});}catch(err){notify(err.message);return;}}download(JSON.stringify({schema:1,work:card},null,2),'my-work-card.json','application/json');}
    if(action==='import-card'){const input=document.createElement('input');input.type='file';input.accept='.json,application/json';input.addEventListener('change',async()=>{const f=input.files[0];if(!f)return;try{if(f.size>32768)throw Error('Use a work-card JSON file smaller than 32 KB.');const x=JSON.parse(await f.text());if(x.schema!==1)throw Error('This is not a supported work-card export.');const w=validateWork(x.work);if(S.work.title&&!window.confirm('Replace the current work card with this imported card?'))return;S.work=w;storeWork();renderOwn();renderAllHelp();openWorkCard();notify('Imported the title and starting condition. Project notes stay in your own file.');}catch(err){notify(err.message||'This file is not a valid work card.');}});input.click();}
    if(action==='clear-card'){if(!window.confirm('Clear this card and its saved browser copy? Your other files will not be changed.'))return;S.work={start:'',title:'',status:'planned'};S.remember=false;storeWork();renderOwn();renderAllHelp();closeDialog();notify('The work card and its saved browser copy have been cleared.');}
  });
  document.addEventListener('submit',e=>{if(e.target.id!=='work-form')return;e.preventDefault();try{S.work=validateWork({start:$('#work-start').value,title:$('#work-title').value,status:$('#work-status').value});S.remember=$('#remember').checked;storeWork();S.showAll=false;renderOwn();renderAllHelp();closeDialog();notify(S.remember?'Work card saved in this browser.':'Work card kept for this open page only.');}catch(err){notify(err.message);}});
  document.addEventListener('input',e=>{if(e.target.id==='portfolio-search'){S.query=e.target.value;renderPortfolios();}if(e.target.id==='source-search')renderSources();});
  $('#previous').addEventListener('click',()=>setSlide(S.slide-1));$('#next').addEventListener('click',()=>setSlide(S.slide+1));
  document.addEventListener('keydown',e=>{if(S.view!=='session'||dialog.open||e.altKey||e.ctrlKey||e.metaKey||/^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(e.target.tagName)||e.target.isContentEditable)return;const k=e.key;if(['ArrowRight','ArrowLeft','Home','End'].includes(k)){e.preventDefault();setSlide(k==='Home'?1:k==='End'?D.session.length:S.slide+(k==='ArrowRight'?1:-1));}});
  window.addEventListener('hashchange',readHash);window.addEventListener('popstate',readHash);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseTimers();});
  loadWork();
  $('#chapter-nav').innerHTML=[...new Set(D.session.map(s=>s.theme))].map((t,i)=>`<button data-jump="${D.session.find(s=>s.theme===t).number}" data-theme="${esc(t)}">${String(i).padStart(2,'0')} ${esc(t)}</button>`).join('');
  $$('a[data-source-link]').forEach(a=>{const s=source(a.dataset.sourceLink);if(s){a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';}else a.textContent='Reference unavailable';});
  initTimers();renderAllHelp();renderModel();renderReadme();renderMessage();renderOwn();refreshSceneContext();readHash();secureLinks();
})();
