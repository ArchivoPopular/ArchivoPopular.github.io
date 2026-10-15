/* REVELA. account flows. A publishable key is safe in the browser; never use a secret key here. */
(() => {
  const config = window.REVELA_AUTH_CONFIG || {};
  const status = document.getElementById('auth-state');
  const form = document.querySelector('.auth-panel form');
  const page = document.body.dataset.authPage;

  function message(value, kind = 'info') {
    if (!status) return;
    status.textContent = value;
    status.dataset.kind = kind;
    status.hidden = false;
  }

  function enableForm(enabled) {
    if (!form) return;
    form.querySelectorAll('input, button[type="submit"]').forEach(control => {
      control.disabled = !enabled;
    });
  }

  function busy(value) {
    const button = form?.querySelector('button[type="submit"]');
    if (button) button.disabled = value;
    form?.setAttribute('aria-busy', String(value));
  }

  function errorMessage(error) {
    const code = error?.code;
    if (code === 'invalid_credentials') return 'El correo o la contraseña no coinciden.';
    if (code === 'email_not_confirmed') return 'Confirmá tu correo desde el enlace que te enviamos y volvé a ingresar.';
    if (code === 'weak_password') return 'Elegí una contraseña más segura.';
    if (code === 'over_email_send_rate_limit' || code === 'over_request_rate_limit') return 'Se hicieron demasiados intentos. Esperá unos minutos y probá de nuevo.';
    return 'No pudimos completar la solicitud. Revisá tu conexión e intentá nuevamente.';
  }

  function validForm() {
    if (form.checkValidity()) return true;
    form.reportValidity();
    return false;
  }

  async function submit(action) {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!validForm()) return;
      busy(true);
      message('Un momento…');
      try {
        await action();
      } catch (error) {
        message(errorMessage(error), 'error');
      } finally {
        busy(false);
      }
    });
  }

  let validConfig = false;
  try {
    const url = new URL(config.url);
    validConfig = url.protocol === 'https:' && !!config.publishableKey &&
      config.publishableKey.startsWith('sb_publishable_') &&
      typeof window.supabase?.createClient === 'function';
  } catch (_) { /* A missing project keeps the forms closed. */ }

  if (!validConfig) {
    message('Las cuentas todavía no están habilitadas. Volvé pronto.');
    enableForm(false);
    return;
  }

  const client = window.supabase.createClient(config.url, config.publishableKey, {
    auth: { autoRefreshToken: true, persistSession: true, detectSessionInUrl: true }
  });
  const accountUrl = new URL('cuenta.html', location.href).href;

  if (page === 'register') {
    enableForm(true);
    status.hidden = true;
    submit(async () => {
      const name = form.elements.name.value.trim();
      const email = form.elements.email.value.trim().toLowerCase();
      const password = form.elements.password.value;
      if (!name) return message('Escribí tu nombre.', 'error');
      if (password !== form.elements.confirm.value) return message('Las contraseñas no coinciden.', 'error');
      const { data, error } = await client.auth.signUp({
        email, password,
        options: { data: { full_name: name }, emailRedirectTo: accountUrl }
      });
      if (error) throw error;
      form.reset();
      if (data.session) location.assign(accountUrl);
      else message('Si el correo se puede registrar, te enviamos un enlace para confirmar tu cuenta. Revisá también la carpeta de spam.', 'success');
    });
  } else if (page === 'login') {
    enableForm(true);
    status.hidden = true;
    if (new URLSearchParams(location.search).has('clave')) message('Contraseña actualizada. Ingresá con tu nueva clave.', 'success');
    submit(async () => {
      const { error } = await client.auth.signInWithPassword({
        email: form.elements.email.value.trim().toLowerCase(),
        password: form.elements.password.value
      });
      if (error) throw error;
      location.assign(accountUrl);
    });
  } else if (page === 'recovery') {
    enableForm(true);
    status.hidden = true;
    submit(async () => {
      const { error } = await client.auth.resetPasswordForEmail(form.elements.email.value.trim().toLowerCase(), {
        redirectTo: new URL('nueva-clave.html', location.href).href
      });
      if (error) throw error;
      form.reset();
      message('Si existe una cuenta con ese correo, recibirás un enlace para cambiar la contraseña. Revisá también la carpeta de spam.', 'success');
    });
  } else if (page === 'new-password') {
    const hash = new URLSearchParams(location.hash.slice(1));
    if (hash.has('error')) message('El enlace no es válido o venció. Solicitá uno nuevo.', 'error');
    else message('Comprobando el enlace de recuperación…');
    client.auth.onAuthStateChange(event => {
      if (event === 'PASSWORD_RECOVERY') {
        enableForm(true);
        message('Ya podés elegir una contraseña nueva.', 'success');
      }
    });
    submit(async () => {
      const password = form.elements.password.value;
      if (password !== form.elements.confirm.value) return message('Las contraseñas no coinciden.', 'error');
      const { error } = await client.auth.updateUser({ password });
      if (error) throw error;
      await client.auth.signOut();
      location.assign(new URL('ingresar.html?clave=actualizada', location.href).href);
    });
  } else if (page === 'account') {
    (async () => {
      const { data, error } = await client.auth.getUser();
      if (error || !data.user) {
        location.replace(new URL('ingresar.html', location.href).href);
        return;
      }
      const name = data.user.user_metadata?.full_name;
      document.getElementById('account-name').textContent = typeof name === 'string' && name.trim() ? name.trim() : 'Tu cuenta';
      document.getElementById('account-email').textContent = data.user.email || '';
      document.getElementById('account-details').hidden = false;
      status.hidden = true;
      const logout = document.getElementById('logout');
      logout.addEventListener('click', async () => {
        logout.disabled = true;
        const { error: signOutError } = await client.auth.signOut();
        if (signOutError) {
          logout.disabled = false;
          message('No pudimos cerrar la sesión. Intentá nuevamente.', 'error');
          return;
        }
        location.replace(new URL('ingresar.html', location.href).href);
      });
    })().catch(() => message('No pudimos verificar tu cuenta. Revisá tu conexión y recargá la página.', 'error'));
  }
})();
