"""Git Graph Web Viewer - Local web server for visualizing git history."""

import json
import subprocess
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Timer

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>gitbro graph</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
            color: #c9d1d9;
            min-height: 100vh;
            padding: 20px;
        }
        
        h1 {
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #58a6ff, #a371f7, #f778ba);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem;
            letter-spacing: 2px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        input, select {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: inherit;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #58a6ff;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
        }
        
        #search { flex: 1; min-width: 200px; }
        
        .graph-container {
            display: flex;
            gap: 0;
            overflow-x: auto;
        }
        
        .graph-lines {
            min-width: 120px;
            padding: 10px 0;
        }
        
        .commits {
            flex: 1;
        }
        
        .commit {
            display: flex;
            align-items: stretch;
            border-bottom: 1px solid #21262d;
            transition: background 0.2s;
        }
        
        .commit:hover {
            background: #161b22;
        }
        
        .commit-graph {
            width: 120px;
            min-width: 120px;
            position: relative;
            padding: 12px 10px;
        }
        
        .commit-graph svg {
            display: block;
        }
        
        .commit-info {
            flex: 1;
            padding: 12px 15px;
            display: grid;
            grid-template-columns: 80px 1fr auto;
            gap: 15px;
            align-items: center;
        }
        
        .hash {
            font-size: 0.85rem;
            color: #58a6ff;
            cursor: pointer;
        }
        
        .hash:hover { text-decoration: underline; }
        
        .message {
            font-size: 0.95rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .meta {
            display: flex;
            gap: 15px;
            font-size: 0.8rem;
            color: #8b949e;
            white-space: nowrap;
        }
        
        .author { color: #a371f7; }
        .date { color: #8b949e; }
        
        .branch-tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            margin-right: 5px;
        }
        
        .branch { background: #238636; color: #fff; }
        .tag { background: #9e6a03; color: #fff; }
        .head { background: #da3633; color: #fff; }
        
        .empty {
            text-align: center;
            padding: 60px;
            color: #8b949e;
        }
        
        @media (max-width: 768px) {
            .commit-info {
                grid-template-columns: 1fr;
                gap: 5px;
            }
            .meta { justify-content: flex-start; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 gitbro graph</h1>
        
        <div class="controls">
            <input type="text" id="search" placeholder="Search commits...">
            <select id="branch-filter">
                <option value="">All branches</option>
            </select>
        </div>
        
        <div class="graph-container">
            <div class="commits" id="commits"></div>
        </div>
    </div>

    <script>
        const commits = __COMMITS_DATA__;
        const branches = __BRANCHES_DATA__;
        
        const colors = [
            '#58a6ff', '#a371f7', '#f778ba', '#56d364', '#e3b341', 
            '#f0883e', '#ff7b72', '#79c0ff', '#d2a8ff', '#7ee787'
        ];
        
        function getColor(index) {
            return colors[index % colors.length];
        }
        
        function renderGraph() {
            const container = document.getElementById('commits');
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const branchFilter = document.getElementById('branch-filter').value;
            
            // Build commit lookup and lane assignment
            const commitMap = new Map(commits.map(c => [c.hash, c]));
            const lanes = new Map();
            let maxLane = 0;
            
            // Simple lane assignment
            commits.forEach((commit, idx) => {
                let lane = 0;
                // Find first available lane
                while ([...lanes.values()].includes(lane)) {
                    lane++;
                }
                lanes.set(commit.hash, lane);
                maxLane = Math.max(maxLane, lane);
                
                // Release lanes for commits that end here
                if (idx > 0) {
                    const prevCommit = commits[idx - 1];
                    if (!commits.slice(idx).some(c => c.parents.includes(prevCommit.hash))) {
                        lanes.delete(prevCommit.hash);
                    }
                }
            });
            
            const filtered = commits.filter(c => {
                if (searchTerm && !c.message.toLowerCase().includes(searchTerm) && 
                    !c.hash.includes(searchTerm) && !c.author.toLowerCase().includes(searchTerm)) {
                    return false;
                }
                if (branchFilter && !c.refs.some(r => r.name === branchFilter)) {
                    return false;
                }
                return true;
            });
            
            if (filtered.length === 0) {
                container.innerHTML = '<div class="empty">No commits found</div>';
                return;
            }
            
            const svgWidth = 120;
            const nodeRadius = 5;
            const laneWidth = 20;
            const rowHeight = 48;
            
            container.innerHTML = filtered.map((commit, idx) => {
                const lane = lanes.get(commit.hash) || 0;
                const cx = 15 + lane * laneWidth;
                const cy = rowHeight / 2;
                const color = getColor(lane);
                
                // Build SVG for this row
                let svg = `<svg width="${svgWidth}" height="${rowHeight}">`;
                
                // Draw vertical lines for active lanes
                for (let l = 0; l <= maxLane; l++) {
                    const lx = 15 + l * laneWidth;
                    const hasCommitInLane = [...lanes.entries()].some(([h, ln]) => ln === l);
                    if (hasCommitInLane || l === lane) {
                        svg += `<line x1="${lx}" y1="0" x2="${lx}" y2="${rowHeight}" 
                                stroke="${getColor(l)}" stroke-width="2" opacity="0.3"/>`;
                    }
                }
                
                // Draw node
                svg += `<circle cx="${cx}" cy="${cy}" r="${nodeRadius}" fill="${color}"/>`;
                svg += `</svg>`;
                
                // Refs (branches/tags)
                const refsHtml = commit.refs.map(ref => {
                    if (ref.type === 'HEAD') return `<span class="branch-tag head">HEAD</span>`;
                    if (ref.type === 'branch') return `<span class="branch-tag branch">${ref.name}</span>`;
                    if (ref.type === 'tag') return `<span class="branch-tag tag">${ref.name}</span>`;
                    return '';
                }).join('');
                
                return `
                    <div class="commit">
                        <div class="commit-graph">${svg}</div>
                        <div class="commit-info">
                            <span class="hash" onclick="navigator.clipboard.writeText('${commit.hash}')" 
                                  title="Click to copy">${commit.hash.slice(0, 7)}</span>
                            <span class="message">${refsHtml}${escapeHtml(commit.message)}</span>
                            <div class="meta">
                                <span class="author">${escapeHtml(commit.author)}</span>
                                <span class="date">${commit.date}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Populate branch filter
        const branchSelect = document.getElementById('branch-filter');
        const uniqueBranches = [...new Set(commits.flatMap(c => 
            c.refs.filter(r => r.type === 'branch').map(r => r.name)
        ))];
        uniqueBranches.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b;
            opt.textContent = b;
            branchSelect.appendChild(opt);
        });
        
        // Event listeners
        document.getElementById('search').addEventListener('input', renderGraph);
        document.getElementById('branch-filter').addEventListener('change', renderGraph);
        
        // Initial render
        renderGraph();
    </script>
</body>
</html>
'''


def get_git_log(limit: int = 100) -> list:
    """Get git log with graph information."""
    # Format: hash|parents|author|date|message|refs
    format_str = "%H|%P|%an|%ar|%s|%D"
    
    result = subprocess.run(
        ["git", "log", f"-{limit}", f"--pretty=format:{format_str}", "--all"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return []
    
    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        
        parts = line.split("|", 5)
        if len(parts) < 6:
            parts.extend([""] * (6 - len(parts)))
        
        hash_, parents, author, date, message, refs_str = parts
        
        # Parse refs
        refs = []
        if refs_str:
            for ref in refs_str.split(", "):
                ref = ref.strip()
                if not ref:
                    continue
                if ref == "HEAD":
                    refs.append({"type": "HEAD", "name": "HEAD"})
                elif ref.startswith("HEAD -> "):
                    refs.append({"type": "HEAD", "name": "HEAD"})
                    refs.append({"type": "branch", "name": ref[8:]})
                elif ref.startswith("tag: "):
                    refs.append({"type": "tag", "name": ref[5:]})
                elif ref.startswith("origin/"):
                    refs.append({"type": "branch", "name": ref})
                else:
                    refs.append({"type": "branch", "name": ref})
        
        commits.append({
            "hash": hash_,
            "parents": parents.split() if parents else [],
            "author": author,
            "date": date,
            "message": message,
            "refs": refs
        })
    
    return commits


def get_branches() -> list:
    """Get list of all branches."""
    result = subprocess.run(
        ["git", "branch", "-a", "--format=%(refname:short)"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    return [b.strip() for b in result.stdout.strip().split("\n") if b.strip()]


def generate_html(limit: int = 100) -> str:
    """Generate the HTML page with embedded data."""
    commits = get_git_log(limit)
    branches = get_branches()
    
    html = HTML_TEMPLATE
    html = html.replace("__COMMITS_DATA__", json.dumps(commits))
    html = html.replace("__BRANCHES_DATA__", json.dumps(branches))
    
    return html


class GraphHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves the graph HTML."""
    
    html_content = ""
    
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.html_content.encode("utf-8"))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass  # Suppress logging


def start_server(port: int = 8787, limit: int = 100, no_browser: bool = False):
    """Start the web server and open browser."""
    GraphHandler.html_content = generate_html(limit)
    
    server = HTTPServer(("127.0.0.1", port), GraphHandler)
    url = f"http://127.0.0.1:{port}"
    
    print(f"🌐 Git Graph running at: {url}")
    print("   Press Ctrl+C to stop")
    
    if not no_browser:
        Timer(0.5, lambda: webbrowser.open(url)).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()

