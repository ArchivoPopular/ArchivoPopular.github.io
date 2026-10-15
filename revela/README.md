# REVELA. — rama de preparación de las cuentas

Esta carpeta contiene la portada de lanzamiento y un flujo de cuentas con Supabase Auth: `registro.html`, `ingresar.html`, `recuperar.html`, `nueva-clave.html` y `cuenta.html`. Incluye verificación de correo, recuperación de contraseña y cierre de sesión. `cuenta.html` muestra solo nombre y correo de la persona autenticada; todavía no es el campus.

**No fusionar esta rama con `main` todavía.** La portada y las preguntas frecuentes describen el primer módulo como disponible, pero todavía no está construido. La rama `main` conserva la información real de preapertura. Las pantallas de cuenta quedan cerradas mientras `auth-config.js` no tenga la URL del proyecto y su clave pública.

## Conectar un proyecto

1. Crear un proyecto Supabase; mantener activado Email/Password y la confirmación por correo en Authentication → Providers.
2. Copiar **Project URL** y **publishable key** desde el proyecto a `auth-config.js`. La URL debe usar HTTPS. Nunca colocar una secret key, service_role key o contraseña aquí.
3. En Authentication → URL Configuration, definir Site URL del sitio que se publicará y agregar **rutas exactas** de redirección: `https://TU-DOMINIO/revela/cuenta.html` y `https://TU-DOMINIO/revela/nueva-clave.html` (ajustar el prefijo según el hosting). Los enlaces del correo deben respetar `redirectTo`.
4. Configurar envío de correo para producción. El servicio de correo de prueba de Supabase tiene límites y disponibilidad limitada.
5. Abrir el sitio bajo HTTPS y comprobar registro, confirmación por correo, ingreso, cierre de sesión, enlace de recuperación vencido y cambio de contraseña. La clave pública permite conectar el navegador a Supabase; los permisos de datos futuros se implementarán con políticas en servidor (RLS), nunca ocultando enlaces en HTML.

## Antes de abrir al público

- Publicar política de privacidad y condiciones aplicables al registro, pagos y entregas de alumnos.
- Construir y probar el primer módulo gratuito. La portada actual afirma que ya se puede acceder a él.
- Proteger cualquier material pago con permisos en servidor y conectar la verificación manual de pagos antes de ofrecer ese acceso.
- Revisar los textos de disponibilidad y fusionar con `main` solo cuando el contenido anunciado esté listo.

No incluir datos bancarios, contraseñas, claves secretas ni fotografías de estudiantes en el repositorio.
