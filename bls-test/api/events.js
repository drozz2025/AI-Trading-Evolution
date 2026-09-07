const data = require('../events.json');

export default function handler(req, res) {
  const now = req.query.now ? new Date(req.query.now) : new Date();
  const all = data.events.map(e => ({ ...e, is_live: new Date(e.scheduled_time) <= now }));
  const live = all.filter(e => e.is_live && e.status === 'scheduled').sort((a,b) => new Date(b.scheduled_time)-new Date(a.scheduled_time))[0] || null;
  res.status(200).json({ source: 'BLS-TEST', server_time: now.toISOString(), event: live, events: all });
}
