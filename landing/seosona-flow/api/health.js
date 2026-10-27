// Kiểm tra deployment còn sống — /health hoặc /api/health
export default function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.setHeader('Allow', 'GET, HEAD');
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }

  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Cache-Control', 'no-store');
  return res.status(200).json({
    ok: true,
    project: "SEOSONA Flow",
    slug: "seosona-flow",
    commit: process.env.VERCEL_GIT_COMMIT_SHA || null,
    region: process.env.VERCEL_REGION || null,
    env: process.env.VERCEL_ENV || 'development',
    at: new Date().toISOString()
  });
}
