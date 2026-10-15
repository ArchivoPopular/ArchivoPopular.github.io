# REVELA. — web y campus de fotografía

La rama `revela-preparacion-registro` contiene:

- Web pública editorial con propuesta, método, planes y preguntas frecuentes.
- Registro, confirmación por correo, ingreso, recuperación y cuenta.
- Campus con seis módulos en el índice; **el primer módulo** tiene cuatro lecciones web, evaluación inicial de 20 preguntas y entrega de tres fotografías con reflexión. Los otros módulos son estructura y temario propuesto, sin lecciones definitivas.
- Progreso: un módulo se considera aprobado solo con **entrega aceptada por admin** y evaluación de **al menos 85 %**, calculado en la base de datos.
- Solicitud de acceso completo por **$780 UYU**, transferencia manual, aviso de operación, verificación bancaria fuera de la web y habilitación desde el panel.
- Panel administrador para solicitudes, revisión de entregas, progreso, carga de PDF en almacenamiento privado, configuración de datos de pago e historial de habilitaciones.
- SQL inicial en `supabase/schema.sql` con RLS, almacenamiento privado y permisos por persona.

## Estado real

**No fusionar con `main` ni activar cobros todavía.** `auth-config.js` ya está conectado al proyecto Supabase de REVELA y la API de autenticación respondió correctamente. Todavía falta ejecutar el esquema para crear las tablas, permisos y almacenamiento privado. La web pública actual en `main` sigue siendo informativa.

Para probarlo en un proyecto real:

1. Crear un proyecto Supabase y ejecutar una vez `supabase/schema.sql` en SQL Editor. Después cargar la clave de corrección **privada** `REVELA_clave_evaluacion_modulo_1.sql` desde el archivo entregado por separado. Mantener la confirmación de correo activada.
2. La **Project URL** y la **publishable key** ya están colocadas en `auth-config.js`. Nunca publicar secret/service_role keys.
3. Configurar la Site URL real y las rutas exactas `cuenta.html` y `nueva-clave.html` como redirecciones permitidas en Authentication → URL Configuration. Usar HTTPS.
4. Crear una cuenta administradora, confirmar el correo y asignar su UUID siguiendo `supabase/README.md`. No inferir un administrador por el dominio del correo.
5. Configurar envío de correo apto para producción, política de privacidad, condiciones del curso y datos reales de transferencia/WhatsApp. Mantener `payments_enabled=false` hasta que haya contenido pago utilizable y condiciones publicadas.
6. Probar en el proyecto real con tres cuentas: estudiante gratuito, estudiante habilitado y administrador. Comprobar registro, recuperación, PDF privado, tres imágenes, nota 17/20 y 16/20, entrega aceptada/rechazada, pago reportado sin autoacceso, habilitación y suspensión.
7. Revisar pedagógicamente el primer módulo y las preguntas. Definir programa final, política de intentos, revisión de trabajos, vigencia del acceso y política de devoluciones antes de abrir inscripciones.

Los PDF se agregan después desde el panel admin; nunca desde una carpeta pública del repositorio. No hay certificado automático. Los datos bancarios, correos de estudiantes, trabajos y claves secretas no se guardan en GitHub.

## Limitaciones actuales

La conexión con Auth se verificó contra el proyecto real, pero el esquema todavía no se ejecutó. No se verificaron entrega de correos, políticas RLS ni permisos de Storage en vivo. El servicio de correo de prueba de Supabase tiene límites; configurar un remitente apto para producción. El número de intentos de evaluación permanece abierto y no debe darse por decidido a partir de esta versión.
