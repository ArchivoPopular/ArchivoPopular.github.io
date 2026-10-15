(() => {
  const $ = id => document.getElementById(id);
  const config = window.REVELA_AUTH_CONFIG || {};
  const notice = $('campus-notice');
  const content = $('campus-content');
  const state = { user: null, admin: false, access: false, module: 1, lesson: null,
    modules: [], lessons: [], questions: [], submissions: [], attempts: [],
    resources: [], request: null, settings: null };
  const el = (tag, className, value) => {
    const item = document.createElement(tag);
    if (className) item.className = className;
    if (value !== undefined) item.textContent = value;
    return item;
  };
  const add = (parent, ...children) => { children.forEach(child => parent.append(child)); return parent; };
  const clear = item => item.replaceChildren();
  const date = value => new Intl.DateTimeFormat('es-UY', { dateStyle: 'medium' }).format(new Date(value));
  function alertUser(text, kind = 'info') {
    notice.textContent = text; notice.dataset.kind = kind; notice.hidden = false;
    notice.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
  function hideNotice() { notice.hidden = true; }
  function check(result) { if (result.error) throw result.error; return result.data; }
  function readable(error) {
    if (error?.message?.includes('row-level security')) return 'No tenés permiso para completar esta acción.';
    return 'No pudimos completar la operación. Revisá tu conexión y volvé a intentarlo.';
  }
  let client;
  try {
    if (new URL(config.url).protocol !== 'https:' ||
        !config.publishableKey?.startsWith('sb_publishable_') ||
        !window.supabase?.createClient) throw new Error('config');
    client = window.supabase.createClient(config.url, config.publishableKey, {
      auth: { autoRefreshToken: true, persistSession: true, detectSessionInUrl: true }
    });
  } catch (_) {
    alertUser('El campus todavía no está conectado. La web pública sigue disponible mientras preparamos las cuentas.');
    return;
  }

  function canOpen(module) { return module.is_free || state.access || state.admin; }
  function view() {
    const hash = location.hash.slice(1);
    const key = hash.startsWith('admin-') ? 'admin' : hash || 'curso';
    const selected = ['curso','modulo','entrega','evaluacion','pago','cuenta','admin'].includes(key) ? key : 'curso';
    const actual = selected === 'admin' && !state.admin ? 'curso' : selected;
    document.querySelectorAll('.campus-view').forEach(section => section.hidden = section.dataset.view !== actual);
    document.querySelectorAll('[data-nav]').forEach(link => {
      if (link.dataset.nav === actual) link.setAttribute('aria-current','page');
      else link.removeAttribute('aria-current');
    });
    if (hash.startsWith('admin-') && state.admin) requestAnimationFrame(() => $(hash)?.scrollIntoView({block:'start'}));
  }
  function progress() {
    const accepted = state.submissions.some(s => s.module_id === 1 && s.status === 'accepted');
    const pending = state.submissions.some(s => s.module_id === 1 && s.status === 'pending');
    const passed = state.attempts.some(a => a.module_id === 1 && a.passed);
    $('progress-text').textContent = accepted && passed ? 'Módulo aprobado: entrega aceptada y evaluación superada.' :
      (accepted ? 'Entrega aceptada. Falta alcanzar 85 % en la evaluación.' :
      passed ? (pending ? 'Evaluación aprobada. La entrega está en revisión.' : 'Evaluación aprobada. Falta una entrega aceptada.') :
      pending ? 'Tu entrega está en revisión. También necesitás aprobar la evaluación.' :
      'Empezá con las lecciones. Para aprobar: entrega aceptada y evaluación de al menos 85 %.');
    $('profile-access').textContent = state.access ? 'Curso completo habilitado' : 'Primer módulo gratuito';
  }
  function renderModules() {
    const grid = $('module-grid'); clear(grid);
    state.modules.forEach(module => {
      const unlocked = canOpen(module);
      const card = el('article','module-card' + (unlocked ? '' : ' locked'));
      add(card, el('span','module-number','MÓDULO ' + String(module.id).padStart(2,'0')),
        el('h3','',module.title),el('p','',module.summary));
      const link = el('a','module-action',unlocked ? 'Explorar módulo ↗' : 'Ver acceso completo ↗');
      link.href = unlocked ? '#modulo' : '#pago';
      if (unlocked) link.addEventListener('click', () => { state.module = module.id; state.lesson = null; renderLessons(); });
      add(card, el('span','module-state',module.is_free ? 'GRATUITO' : (unlocked ? 'HABILITADO' : 'ACCESO COMPLETO')),link);
      grid.append(card);
    });
  }
  function renderLessons() {
    const module = state.modules.find(m => m.id === state.module);
    if (!module) return;
    document.querySelector('.module-actions').hidden = module.id !== 1;
    $('lesson-kicker').textContent = 'MÓDULO ' + String(module.id).padStart(2,'0') + (module.is_free ? ' / GRATUITO' : ' / ACCESO COMPLETO');
    $('lesson-module-title').textContent = module.title;
    $('lesson-module-lede').textContent = module.summary;
    const list = $('lesson-list'), article = $('lesson-article'), resources = $('resource-list');
    clear(list); clear(article); clear(resources);
    if (!canOpen(module)) {
      article.append(el('p','','Este módulo requiere acceso completo. Podés solicitarlo desde tu cuenta.'));
      return;
    }
    const lessons = state.lessons.filter(l => l.module_id === module.id).sort((a,b) => a.position-b.position);
    if (!lessons.length) article.append(el('p','','Las lecciones de este módulo se están preparando. No tienen fecha anunciada.'));
    lessons.forEach(lesson => {
      const button = el('button','lesson-link' + (state.lesson === lesson.id ? ' active' : ''),String(lesson.position).padStart(2,'0') + ' / ' + lesson.title);
      button.type = 'button';
      button.addEventListener('click', () => { state.lesson = lesson.id; renderLessons(); article.scrollIntoView({behavior:'smooth',block:'start'}); });
      list.append(button);
    });
    const current = lessons.find(l => l.id === state.lesson) || lessons[0];
    if (current) {
      state.lesson = current.id;
      article.append(el('span','lesson-count','LECCIÓN ' + String(current.position).padStart(2,'0')),el('h2','',current.title),el('p','lesson-lead',current.lead));
      (current.blocks || []).forEach(block => {
        const section = el('section','lesson-block');
        section.append(el('h3','',block.heading),el('p','',block.text));
        article.append(section);
      });
    }
    const files = state.resources.filter(r => r.module_id === module.id);
    if (!files.length) resources.append(el('p','','El libro PDF de este módulo se incorporará aquí.'));
    files.forEach(file => {
      const button = el('button','resource-link',file.title + ' · Abrir PDF ↗');
      button.type = 'button';
      button.addEventListener('click',async () => {
        try {
          const data = check(await client.storage.from('course-files').createSignedUrl(file.storage_path,60));
          window.location.assign(data.signedUrl);
        } catch (error) { alertUser(readable(error),'error'); }
      });
      resources.append(button);
    });
  }
  function renderQuestions() {
    const area = $('quiz-questions'); clear(area);
    state.questions.forEach((question,index) => {
      const field = el('fieldset','quiz-question'), legend = el('legend','',String(index+1).padStart(2,'0') + ' / ' + question.prompt);
      field.append(legend);
      question.options.forEach((option,answer) => {
        const label = el('label','quiz-option');
        const input = el('input'); input.type='radio'; input.name='q-' + question.id; input.value=String(answer); input.required=true;
        label.append(input,document.createTextNode(option)); field.append(label);
      });
      area.append(field);
    });
    $('quiz-form').hidden = !state.questions.length;
    if (!state.questions.length) area.append(el('p','','La evaluación todavía no está cargada.'));
    const history = $('quiz-history'); clear(history);
    const attempts = state.attempts.filter(a => a.module_id===1);
    if (!attempts.length) history.append(el('p','','Todavía no hay intentos.'));
    attempts.forEach(a => {
      const row = el('div','history-row');
      row.append(el('strong','',a.correct_count + '/' + a.question_count + ' · ' + (a.passed ? 'Mínimo alcanzado' : 'Necesitás 85 %')),
        el('span','',date(a.submitted_at)));
      history.append(row);
    });
  }
  function renderSubmissions() {
    const area = $('submission-history'); clear(area);
    const entries = state.submissions.filter(s => s.module_id===1);
    if (!entries.length) area.append(el('p','','Todavía no hay entregas.'));
    entries.forEach(s => {
      const row = el('div','history-row');
      const names = {pending:'En revisión',accepted:'Aceptada',rejected:'Necesita nueva entrega'};
      row.append(el('strong','',names[s.status] || s.status),el('span','',date(s.submitted_at)));
      if (s.review_note) row.append(el('p','',s.review_note));
      area.append(row);
    });
  }
  function renderPayment() {
    const panel = $('payment-panel'); clear(panel);
    if (state.access) {
      panel.append(el('h2','','Tu acceso completo está habilitado'),el('p','','Ya podés consultar los módulos y materiales disponibles desde Mi curso.'));
      return;
    }
    if (!state.settings?.payments_enabled) {
      panel.append(el('h2','','Las inscripciones al curso completo abrirán próximamente'),
        el('p','','Podés estudiar el primer módulo gratuito. No transfieras dinero: todavía no se han habilitado los pagos.'));
      return;
    }
    if (!state.request) {
      panel.append(el('h2','','Solicitar acceso completo'),el('p','','La solicitud queda asociada a tu cuenta. Después verás aquí los datos oficiales para transferir.'));
      const button=el('button','button button-dark','Solicitar datos de pago ↗');
      button.type='button';
      button.addEventListener('click',async () => {
        button.disabled=true;
        try {
          check(await client.from('payment_requests').insert({user_id:state.user.id}));
          await load(); alertUser('Solicitud registrada. Revisá las instrucciones de transferencia.','success');
        } catch(error) { alertUser(readable(error),'error'); button.disabled=false; }
      });
      panel.append(button);
      return;
    }
    if (state.request.status === 'verified') {
      panel.append(el('h2','','Consultá por tu acceso'),
        el('p','','La transferencia figura como verificada, pero el acceso no está activo. Contactá a la academia para revisar tu cuenta. No vuelvas a transferir.'));
      return;
    }
    panel.append(el('span','payment-reference','SOLICITUD ' + state.request.id.slice(0,8).toUpperCase()),
      el('h2','',state.request.status==='reported' ? 'Aviso de transferencia recibido' : 'Datos para transferir'),
      el('p','',state.request.status==='reported' ? 'El aviso no habilita el curso. Verificaremos la acreditación bancaria antes de activar tu acceso.' : 'Transferí $780 UYU usando exclusivamente estos datos configurados por la academia:'));
    const bank = el('div','bank-data',state.settings.bank_instructions);
    panel.append(bank);
    if (state.settings.whatsapp_number && /^\d{8,15}$/.test(state.settings.whatsapp_number)) {
      const wa=el('a','payment-whatsapp','Consultar por WhatsApp ↗');
      wa.href='https://wa.me/' + state.settings.whatsapp_number + '?text=' + encodeURIComponent('Hola, consulto por mi solicitud REVELA. ' + state.request.id.slice(0,8));
      wa.target='_blank'; wa.rel='noopener noreferrer'; panel.append(wa);
    }
    if (state.request.status !== 'reported') {
      const form=el('form','payment-report');
      const label=el('label','','Referencia de transferencia (opcional)'), input=el('input');
      input.type='text'; input.maxLength=140; input.placeholder='Número o dato para ubicar la operación';
      const button=el('button','button button-dark','Avisar que transferí ↗'); button.type='submit';
      form.append(label,input,button);
      form.addEventListener('submit',async event => {
        event.preventDefault(); button.disabled=true;
        try {
          check(await client.rpc('report_payment',{p_reference:input.value}));
          await load(); alertUser('Aviso enviado. El acceso depende de la verificación bancaria.','success');
        } catch(error) { alertUser(readable(error),'error'); button.disabled=false; }
      });
      panel.append(form);
    }
  }
  async function loadAdmin() {
    const [profiles,requests,access,submissions,attempts,resources,settings,audit] = await Promise.all([
      client.from('profiles').select('user_id,email,full_name').order('created_at',{ascending:false}),
      client.from('payment_requests').select('*').order('requested_at',{ascending:false}),
      client.from('course_access').select('*'),
      client.from('submissions').select('*').order('submitted_at',{ascending:false}),
      client.from('quiz_attempts').select('user_id,module_id,correct_count,question_count,passed,submitted_at').order('submitted_at',{ascending:false}),
      client.from('resources').select('*').order('created_at',{ascending:false}),
      client.from('payment_settings').select('*').eq('id',1).maybeSingle(),
      client.from('admin_audit').select('*').order('created_at',{ascending:false}).limit(100)
    ]).then(results => results.map(check));
    const names=new Map(profiles.map(p => [p.user_id,p]));
    const accessIds=new Set(access.filter(a => a.granted_at && !a.revoked_at).map(a => a.user_id));
    const list=$('admin-requests'); clear(list);
    if (!requests.length) list.append(el('p','','Todavía no hay solicitudes.'));
    requests.forEach(r => {
      const p=names.get(r.user_id), row=el('div','admin-row');
      row.append(el('strong','',p?.full_name || p?.email || r.user_id),
        el('span','',p?.email || ''),el('span','',r.status + ' · ' + date(r.requested_at)));
      if (r.reference) row.append(el('p','','Referencia comunicada: ' + r.reference));
      const active=accessIds.has(r.user_id);
      if (r.status==='reported' || r.status==='verified' || active) {
        const button=el('button','admin-action',active ? 'Suspender acceso' :
          r.status==='verified' ? 'Restaurar acceso' : 'Habilitar tras verificar banco');
        button.type='button';
        button.addEventListener('click',async () => {
          const confirmed=window.confirm(active ?
            '¿Suspender el acceso de esta cuenta? El progreso se conserva.' :
            (r.status==='verified' ? 'Esta cuenta tenía una acreditación verificada. ¿Restaurar el acceso?' :
            'Confirmá que verificaste la acreditación de $780 UYU en la cuenta bancaria y que corresponde a este alumno. ¿Habilitar?'));
          if (!confirmed) return;
          button.disabled=true;
          try {
            check(await client.rpc('set_course_access',{p_user:r.user_id,p_grant:!active,p_note:active?'Suspensión desde panel':'Acreditación bancaria verificada'}));
            await load(); alertUser(active?'Acceso suspendido.':'Acceso habilitado y registrado.','success');
          } catch(error) { alertUser(readable(error),'error'); button.disabled=false; }
        });
        row.append(button);
      }
      list.append(row);
    });
    const work=$('admin-work'); clear(work);
    const pendingWork=submissions.filter(s => s.status==='pending');
    if (!pendingWork.length) work.append(el('p','','No hay entregas pendientes.'));
    pendingWork.forEach(s => {
      const p=names.get(s.user_id), row=el('div','admin-row');
      row.append(el('strong','',(p?.full_name || p?.email || s.user_id) + ' · Módulo ' + s.module_id),
        el('span','',date(s.submitted_at)),el('p','',s.reflection));
      const links=el('div','work-links');
      (s.files || []).forEach((path,i) => {
        const button=el('button','resource-link','Foto ' + (i+1) + ' ↗');
        button.type='button';
        button.addEventListener('click',async () => {
          try {
            const data=check(await client.storage.from('student-work').createSignedUrl(path,60));
            window.location.assign(data.signedUrl);
          } catch(error) { alertUser(readable(error),'error'); }
        });
        links.append(button);
      });
      row.append(links);
      const note=el('textarea'); note.placeholder='Comentario de revisión (opcional)'; note.maxLength=1000; note.rows=3;
      row.append(note);
      ['Aceptar','Pedir nueva entrega'].forEach((label,i) => {
        const button=el('button','admin-action',label);
        button.type='button';
        button.addEventListener('click',async () => {
          if (!window.confirm(i===0?'¿Aceptar esta entrega después de revisar las tres imágenes?':'¿Marcar esta entrega para volver a realizar?')) return;
          button.disabled=true;
          try {
            check(await client.rpc('review_submission',{p_submission:s.id,p_accept:i===0,p_note:note.value}));
            await load(); alertUser('Revisión guardada.','success');
          } catch(error) { alertUser(readable(error),'error'); button.disabled=false; }
        });
        row.append(button);
      });
      work.append(row);
    });
    const progressArea=$('admin-progress-list'); clear(progressArea);
    if (!profiles.length) progressArea.append(el('p','','No hay alumnos registrados.'));
    profiles.forEach(p => {
      const userWork=submissions.filter(s => s.user_id===p.user_id && s.module_id===1);
      const userAttempts=attempts.filter(a => a.user_id===p.user_id && a.module_id===1);
      const accepted=userWork.some(s => s.status==='accepted');
      const passed=userAttempts.some(a => a.passed);
      const best=userAttempts.length ? Math.max(...userAttempts.map(a => a.correct_count/a.question_count)) : null;
      const row=el('div','admin-row');
      row.append(el('strong','',p.full_name || p.email),el('span','',p.email),
        el('p','', 'Módulo 1: ' + (accepted && passed ? 'aprobado' :
          (accepted ? 'falta evaluación' : userWork.some(s => s.status==='pending') ? 'entrega en revisión' : 'falta entrega aceptada')) +
          '. Mejor evaluación: ' + (best===null ? 'sin intentos' : Math.round(best*100)+' %') +
          '. Intentos: ' + userAttempts.length + '.'));
      progressArea.append(row);
    });
    const pdf=$('admin-resource-list'); clear(pdf);
    if (!resources.length) pdf.append(el('p','','Todavía no hay PDF cargados.'));
    resources.forEach(r => pdf.append(el('p','','Módulo ' + r.module_id + ' · ' + r.title)));
    $('bank-instructions').value=settings?.bank_instructions || '';
    $('whatsapp-number').value=settings?.whatsapp_number || '';
    $('payments-enabled').checked=!!settings?.payments_enabled;
    const auditArea=$('admin-audit-list'); clear(auditArea);
    if (!audit.length) auditArea.append(el('p','','No hay acciones registradas.'));
    audit.forEach(entry => {
      const person=names.get(entry.subject_id);
      const row=el('div','history-row');
      row.append(el('strong','',entry.action + ' · ' + (person?.email || entry.subject_id || 'cuenta')),
        el('span','',date(entry.created_at)));
      if (entry.detail) row.append(el('p','',entry.detail));
      auditArea.append(row);
    });
  }
  async function load() {
    const [modules,lessons,questions,submissions,attempts,resources,request,settings,access] = await Promise.all([
      client.from('modules').select('*').order('id'),
      client.from('lessons').select('*').order('position'),
      client.from('quiz_questions').select('id,module_id,position,prompt,options').eq('module_id',1).order('position'),
      client.from('submissions').select('*').eq('user_id',state.user.id).order('submitted_at',{ascending:false}),
      client.from('quiz_attempts').select('*').eq('user_id',state.user.id).order('submitted_at',{ascending:false}),
      client.from('resources').select('*').order('created_at',{ascending:false}),
      client.from('payment_requests').select('*').eq('user_id',state.user.id).maybeSingle(),
      client.from('payment_settings').select('*').eq('id',1).maybeSingle(),
      client.from('course_access').select('*').eq('user_id',state.user.id).maybeSingle()
    ]).then(results => results.map(check));
    Object.assign(state,{modules,lessons,questions,submissions,attempts,resources,request,settings,
      access:!!(access?.granted_at && !access?.revoked_at)});
    $('profile-access').textContent=state.access?'Curso completo habilitado':'Primer módulo gratuito';
    renderModules();renderLessons();renderQuestions();renderSubmissions();renderPayment();progress();
    if(state.admin) await loadAdmin();
    content.hidden=false; hideNotice(); view();
  }
  function bindForms() {
    $('quiz-form').addEventListener('submit',async event => {
      event.preventDefault();
      const answers={};
      for (const q of state.questions) {
        const selected=document.querySelector('input[name="q-' + q.id + '"]:checked');
        if (!selected) { alertUser('Respondé todas las preguntas antes de enviar.','error'); return; }
        answers[q.id]=Number(selected.value);
      }
      const button=event.currentTarget.querySelector('button[type="submit"]'); button.disabled=true;
      try {
        const result=check(await client.from('quiz_attempts').insert({user_id:state.user.id,module_id:1,answers}).select().single());
        await load();
        alertUser(result.correct_count + '/' + result.question_count + ' correctas. ' +
          (result.passed ? 'Alcanzaste el mínimo. Recordá que también necesitás la entrega aceptada.' :
          'Necesitás al menos ' + Math.ceil(.85*result.question_count) + ' correctas.'),result.passed?'success':'info');
      } catch(error) { alertUser(readable(error),'error'); } finally { button.disabled=false; }
    });
    $('submission-form').addEventListener('submit',async event => {
      event.preventDefault();
      const files=[...$('submission-files').files], reflection=$('submission-reflection').value.trim();
      if (files.length!==3 || reflection.length<30 || reflection.length>1000 ||
          files.some(f => !['image/jpeg','image/png','image/webp'].includes(f.type) || f.size>10485760 || f.size===0)) {
        alertUser('Elegí exactamente tres imágenes JPG, PNG o WebP de hasta 10 MB y escribí una reflexión de 30 a 1000 caracteres.','error');return;
      }
      const button=event.currentTarget.querySelector('button[type="submit"]');button.disabled=true;
      alertUser('Subiendo tus tres imágenes…');
      try {
        const paths=[];
        for (const file of files) {
          const ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[file.type];
          const path=state.user.id + '/' + crypto.randomUUID() + '.' + ext;
          check(await client.storage.from('student-work').upload(path,file,{contentType:file.type,upsert:false}));
          paths.push(path);
        }
        check(await client.from('submissions').insert({user_id:state.user.id,module_id:1,files:paths,reflection}));
        event.currentTarget.reset();await load();
        alertUser('Recibimos tu trabajo. Quedó pendiente de revisión.','success');
      } catch(error) { alertUser(readable(error),'error'); } finally { button.disabled=false; }
    });
    $('campus-logout').addEventListener('click',async () => {
      const result=await client.auth.signOut();
      if (result.error) alertUser('No pudimos cerrar la sesión. Intentá de nuevo.','error');
      else location.replace('ingresar.html');
    });
    $('admin-settings-form').addEventListener('submit',async event => {
      event.preventDefault();if (!state.admin) return;
      const bank=$('bank-instructions').value.trim(),phone=$('whatsapp-number').value.replace(/\D/g,'');
      const enabled=$('payments-enabled').checked;
      if (enabled && bank.length<15) {alertUser('Completá los datos bancarios oficiales antes de activar pagos.','error');return;}
      if (phone && !/^\d{8,15}$/.test(phone)) {alertUser('Revisá el número de WhatsApp.','error');return;}
      const button=event.currentTarget.querySelector('button[type="submit"]');button.disabled=true;
      try {
        check(await client.from('payment_settings').update({bank_instructions:bank,whatsapp_number:phone,payments_enabled:enabled,updated_at:new Date().toISOString()}).eq('id',1));
        await load();alertUser('Configuración guardada.','success');
      } catch(error) {alertUser(readable(error),'error');} finally {button.disabled=false;}
    });
    $('admin-pdf-form').addEventListener('submit',async event => {
      event.preventDefault();if (!state.admin) return;
      const file=$('pdf-file').files[0],moduleId=Number($('pdf-module').value),title=$('pdf-title').value.trim();
      if (!file || file.type!=='application/pdf' || file.size>20971520 || !title) {
        alertUser('Elegí un PDF de hasta 20 MB, un módulo y un título.','error');return;
      }
      const button=event.currentTarget.querySelector('button[type="submit"]');button.disabled=true;
      try {
        const path='m' + moduleId + '/' + crypto.randomUUID() + '.pdf';
        check(await client.storage.from('course-files').upload(path,file,{contentType:'application/pdf',upsert:false}));
        check(await client.from('resources').insert({module_id:moduleId,title,storage_path:path}));
        event.currentTarget.reset();await load();alertUser('PDF guardado en almacenamiento privado.','success');
      } catch(error) {alertUser(readable(error),'error');} finally {button.disabled=false;}
    });
  }
  async function start() {
    try {
      const result=await client.auth.getUser();
      if (result.error || !result.data.user) {location.replace('ingresar.html');return;}
      state.user=result.data.user;
      const name=state.user.user_metadata?.full_name?.trim() || 'estudiante';
      $('student-first-name').textContent=name.split(/\s+/)[0];
      $('profile-name').textContent=name;
      $('profile-email').textContent=state.user.email || '';
      state.admin=!!check(await client.rpc('my_role'));
      $('admin-nav').hidden=!state.admin;
      bindForms();
      window.addEventListener('hashchange',view);
      await load();
      const options=$('pdf-module');
      state.modules.forEach(m => {
        const option=el('option','',String(m.id).padStart(2,'0')+' / '+m.title);
        option.value=String(m.id);options.append(option);
      });
    } catch(error) {
      alertUser('No pudimos cargar el campus. Revisá la conexión con el proyecto y recargá la página.','error');
    }
  }
  start();
})();
