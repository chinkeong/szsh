#!/usr/bin/env node
// Encrypts content.html into index.html so neither the page content nor the
// password ever ships in readable form.
//
//   node build.js <password>          (or set SITE_PASSWORD)

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ITERATIONS = 310000;

const password = process.argv[2] || process.env.SITE_PASSWORD;
if (!password) {
  console.error('Usage: node build.js <password>   (or set SITE_PASSWORD)');
  process.exit(1);
}

const dir = __dirname;
const contentPath = path.join(dir, 'content.html');
if (!fs.existsSync(contentPath)) {
  console.error('content.html not found. Start from the example:');
  console.error('  cp content.example.html content.html');
  process.exit(1);
}
const content = fs.readFileSync(contentPath, 'utf8');
const template = fs.readFileSync(path.join(dir, 'template.html'), 'utf8');

// Must match normalise() in template.html, or the browser derives a different key.
const normalised = password.trim().toLowerCase();

const salt = crypto.randomBytes(16);
const iv = crypto.randomBytes(12);
const key = crypto.pbkdf2Sync(normalised, salt, ITERATIONS, 32, 'sha256');

const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
const ciphertext = Buffer.concat([
  cipher.update(content, 'utf8'),
  cipher.final(),
  cipher.getAuthTag(),   // Web Crypto expects the tag appended to the ciphertext
]);

const payload = JSON.stringify({
  salt: salt.toString('base64'),
  iv: iv.toString('base64'),
  ciphertext: ciphertext.toString('base64'),
  iterations: ITERATIONS,
});

if (!template.includes('__PAYLOAD__')) {
  console.error('template.html is missing the __PAYLOAD__ placeholder.');
  process.exit(1);
}

fs.writeFileSync(path.join(dir, 'index.html'), template.replace('__PAYLOAD__', payload));

console.log(`Encrypted ${content.length} bytes of content.html -> index.html`);
