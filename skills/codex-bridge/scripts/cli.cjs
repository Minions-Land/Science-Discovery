#!/usr/bin/env node
/**
 * codex-bridge CLI
 * Usage:
 *   npx codex-bridge setup          — register MCP with Claude Code
 *   npx codex-bridge setup --global  — register globally (all projects)
 *   npx codex-bridge install-skill   — symlink the /delegate skill into ~/.claude/skills/
 *   npx codex-bridge diagnose        — check config and connectivity
 */

const { execFileSync, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const PKG_ROOT = path.resolve(__dirname, '..');
const SERVER_JS = path.join(PKG_ROOT, 'dist', 'server.js');
const SKILL_SRC = path.join(PKG_ROOT, 'skills', 'codex');
const SKILL_DST = path.join(os.homedir(), '.claude', 'skills', 'codex');

function log(msg) { console.log(`  ${msg}`); }
function ok(msg)  { console.log(`  ✓ ${msg}`); }
function fail(msg){ console.log(`  ✗ ${msg}`); }

function ensureBuild() {
  if (!fs.existsSync(SERVER_JS)) {
    log('dist/server.js not found — building...');
    const r = spawnSync('npm', ['run', 'build'], { cwd: PKG_ROOT, stdio: 'inherit' });
    if (r.status !== 0) { fail('build failed'); process.exit(1); }
  }
  return SERVER_JS;
}

function setup(global) {
  const serverPath = ensureBuild();
  console.log('\n  codex-bridge MCP setup\n');

  const scope = global ? ['-s', 'user'] : ['-s', 'local'];
  const args = ['mcp', 'add', 'codex-bridge', ...scope, '--', 'node', serverPath];

  try {
    execFileSync('claude', args, { stdio: 'inherit' });
    ok(`Registered codex-bridge (${global ? 'global' : 'project'} scope)`);
  } catch (e) {
    fail('claude mcp add failed — is Claude Code CLI installed?');
    log(`Manual: claude mcp add codex-bridge ${scope.join(' ')} -- node ${serverPath}`);
  }

  console.log('\n  Next steps:');
  log('1. Restart Claude Code (or start a new session)');
  log('2. Verify: /mcp should show codex-bridge with ask_codex + run_codex_worker');
  log('3. Optional: npx codex-bridge install-skill');
  console.log('');
}

function installSkill() {
  console.log('\n  Installing /delegate skill\n');

  if (fs.existsSync(SKILL_DST)) {
    const stat = fs.lstatSync(SKILL_DST);
    if (stat.isSymbolicLink()) {
      fs.unlinkSync(SKILL_DST);
    } else {
      fail(`${SKILL_DST} already exists and is not a symlink. Remove it first.`);
      process.exit(1);
    }
  }

  fs.mkdirSync(path.dirname(SKILL_DST), { recursive: true });
  fs.symlinkSync(SKILL_SRC, SKILL_DST, 'dir');
  ok(`Symlinked ${SKILL_DST} -> ${SKILL_SRC}`);
  log('The /delegate skill is now available in all Claude Code sessions.');
  console.log('');
}

function diagnose() {
  console.log('\n  codex-bridge diagnostics\n');

  // Check build
  if (fs.existsSync(SERVER_JS)) {
    ok(`dist/server.js exists`);
  } else {
    fail('dist/server.js missing — run: npm run build');
  }

  // Check codex CLI
  try {
    const v = execFileSync('codex', ['--version'], { encoding: 'utf8' }).trim();
    ok(`codex CLI: ${v}`);
  } catch {
    fail('codex CLI not found — run_codex_worker will be unavailable');
    log('Install: npm i -g @openai/codex');
  }

  // Check API key
  const hasKey = !!process.env.OPENAI_API_KEY;
  const authJson = path.join(os.homedir(), '.codex', 'auth.json');
  const hasAuthJson = fs.existsSync(authJson);

  if (hasKey) {
    ok('OPENAI_API_KEY is set in environment');
  } else if (hasAuthJson) {
    ok(`API key found in ${authJson}`);
  } else {
    fail('No API key found (env or ~/.codex/auth.json)');
    log('Set OPENAI_API_KEY or run: codex login');
  }

  // Check config
  const globalToml = path.join(os.homedir(), '.codex', 'config.toml');
  if (fs.existsSync(globalToml)) {
    const content = fs.readFileSync(globalToml, 'utf8');
    const model = content.match(/^model\s*=\s*"(.+)"/m);
    const baseUrl = content.match(/base_url\s*=\s*"(.+)"/m);
    if (model) ok(`Model: ${model[1]}`);
    if (baseUrl) ok(`Base URL: ${baseUrl[1]}`);
  } else {
    log('No ~/.codex/config.toml found (will use defaults)');
  }

  // Check skill
  if (fs.existsSync(SKILL_DST)) {
    ok('/delegate skill installed');
  } else {
    log('/delegate skill not installed — run: npx codex-bridge install-skill');
  }

  console.log('');
}

// ── main ──────────────────────────────────────────────────────────────────────

const cmd = process.argv[2];
const flags = process.argv.slice(3);

switch (cmd) {
  case 'setup':
    setup(flags.includes('--global') || flags.includes('-g'));
    break;
  case 'install-skill':
    installSkill();
    break;
  case 'diagnose':
  case 'doctor':
    diagnose();
    break;
  default:
    console.log(`
  codex-bridge — MCP server bridging Claude Code to Codex GPT-5.5

  Commands:
    setup [--global]    Register MCP with Claude Code
    install-skill       Install /delegate skill to ~/.claude/skills/
    diagnose            Check config, CLI, and connectivity

  Quick start:
    npx codex-bridge setup
    npx codex-bridge install-skill
`);
}
