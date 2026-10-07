# Security Notes

## Required production settings

- Set a strong, random SECRET_KEY.
- Use PostgreSQL in production.
- Set ALLOWED_ORIGINS to the exact frontend origin(s).
- Keep GROQ_API_KEY server-side; never expose it to Vite or browser code.
- Do not commit .env files or uploaded datasets.

## Dataset isolation

Every dataset route and AI request must verify that the dataset belongs to the authenticated user.

## AI data handling

NeuroSync sends the selected dataset's derived analysis context to the configured Groq provider. Do not upload sensitive business data unless the deployment's data-processing requirements permit it.

## Storage

The current upload implementation uses local disk for the prototype. For horizontally scaled or ephemeral production deployments, move dataset files to durable object storage and keep only metadata in PostgreSQL.
