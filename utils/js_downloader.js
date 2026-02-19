const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * JS Downloader Bridge for Astra Userbot
 * Bypasses Python environment instability for media downloads.
 */

async function download() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.error(JSON.stringify({ error: 'No URL provided' }));
        process.exit(1);
    }

    const url = args[0];
    const mode = args[1] || 'video'; // 'video' or 'audio'
    const cookies_file = args[2] || null;
    const cookies_browser = args[3] || null;

    const tempDir = path.join(__dirname, '../temp');
    if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });

    const timestamp = Date.now();
    const outputTmpl = path.join(tempDir, `jsdl_${timestamp}_%(id)s.%(ext)s`);

    let ytArgs = [
        '--newline',
        '--no-playlist',
        '--geo-bypass',
        '--no-check-certificates',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        '-o', outputTmpl
    ];

    if (cookies_file) {
        ytArgs.push('--cookies', cookies_file);
    } else if (cookies_browser) {
        ytArgs.push('--cookies-from-browser', cookies_browser);
    }

    if (mode === 'audio') {
        ytArgs.push('--extract-audio', '--audio-format', 'mp3', '--audio-quality', '0');
        ytArgs.push('-f', 'ba/b');
    } else {
        // More robust format: try to get mp4 specifically, fallback to best but limited to 720p for fast uploads
        ytArgs.push('-f', 'bestvideo[height<=720][ext=mp4]+bestaudio[m4a]/best[height<=720][ext=mp4]/best[ext=mp4]/best');
    }

    ytArgs.push(url);

    const cp = spawn('/opt/homebrew/bin/yt-dlp', ytArgs);

    cp.stderr.on('data', (data) => {
        // Log errors to stderr of this process
        process.stderr.write(data);
    });

    cp.on('close', (code) => {
        if (code !== 0) {
            process.exit(code);
        }

        // Find the downloaded file
        const files = fs.readdirSync(tempDir).filter(f => f.startsWith(`jsdl_${timestamp}_`));
        if (files.length === 0) {
            console.error(JSON.stringify({ error: 'No file found after download' }));
            process.exit(1);
        }

        // Output results as JSON for Python to parse
        const results = files.map(f => path.join(tempDir, f));
        console.log(JSON.stringify({ success: true, files: results }));
    });
}

download().catch(err => {
    console.error(JSON.stringify({ error: err.message }));
    process.exit(1);
});
