#!/usr/bin/env node
/**
 * postinstall — verify build artifacts exist after npm install.
 */
const fs = require('fs');
const path = require('path');

const SERVER_JS = path.join(__dirname, '..', 'dist', 'server.js');

if (!fs.existsSync(SERVER_JS)) {
  console.log('');
  console.log('  codex-bridge: dist/server.js not found.');
  console.log('  If installing from source, run: npm run build');
  console.log('');
} else {
  console.log('  codex-bridge installed. Run: npx codex-bridge setup');
}
