# REVELA. — base de datos

`schema.sql` se ejecuta **una sola vez** en el SQL Editor de un proyecto Supabase nuevo. Crea tablas, permisos, almacenamiento privado y el primer módulo de prueba. No contiene credenciales ni datos bancarios. La clave de respuestas está en un archivo privado separado, fuera del repositorio: `REVELA_clave_evaluacion_modulo_1.sql`. Ejecutarlo después de `schema.sql`; hasta ese momento la evaluación no se puede calificar.

Después de crear una cuenta propia y confirmar su correo, buscá su UUID en Authentication → Users y asigná el primer administrador desde SQL Editor:

```sql
insert into public.app_admins (user_id) values ('UUID-DE-TU-CUENTA');
```

El panel `admin.html` podrá entonces completar las instrucciones bancarias y el teléfono de WhatsApp, revisar entregas, subir PDF y habilitar manualmente el curso **después** de comprobar la acreditación bancaria. No actives cobros hasta tener contenidos pagos, condiciones y datos reales.

El contenido del primer módulo y sus 20 preguntas son una versión editorial inicial para revisión de Santiago; 20 preguntas hacen visible el límite 17/20 = 85 %. Las políticas de reintentos, revisión de entregas y programa definitivo todavía deben confirmarse. En esta versión la entrega queda **pendiente** hasta que el administrador la acepte; no se emite certificado.

Los permisos de `storage.objects` y las políticas RLS deben verificarse con al menos una cuenta gratuita, una habilitada y una administradora en el proyecto real antes de publicar. Los PDF van al bucket privado `course-files`; los trabajos, al bucket privado `student-work`.
