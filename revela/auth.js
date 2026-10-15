// La interfaz queda bloqueada hasta que exista un servicio de autenticación real.
// El registro y el ingreso se implementarán junto con el campus y sus permisos.
document.querySelectorAll('.auth-panel form').forEach(form => {
  form.addEventListener('submit', event => event.preventDefault());
});
