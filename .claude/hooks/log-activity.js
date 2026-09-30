// Logt alle AI-acties (prompts, bestandswijzigingen, commando's) naar .claude/logs/ai-activity.md
const fs = require("fs");
const path = require("path");

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  try {
    const e = JSON.parse(raw || "{}");
    // Fixed location relative to this script, never taken from input (prevents path traversal).
    const root = path.resolve(__dirname, "..", "..");
    const logFile = path.join(root, ".claude", "logs", "ai-activity.md");
    const rel = (p) => (p ? path.relative(root, p).split(path.sep).join("/") : "?");
    const short = (s, n = 200) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);

    const ts = new Date().toISOString().replace("T", " ").slice(0, 19);
    const sid = (e.session_id || "").slice(0, 8);
    const input = e.tool_input || {};
    let line;

    switch (e.hook_event_name) {
      case "UserPromptSubmit":
        line = `\n### ${ts} · sessie \`${sid}\`\n- 💬 **Prompt:** ${short(e.prompt, 300)}`;
        break;
      case "Stop":
        line = `- ✅ Beurt afgerond`;
        break;
      case "PostToolUse":
        if (["Bash", "PowerShell"].includes(e.tool_name)) {
          line = `- ⚙️ **${e.tool_name}:** \`${short(input.command, 200)}\``;
        } else {
          line = `- ✏️ **${e.tool_name}:** \`${rel(input.file_path || input.notebook_path)}\``;
        }
        break;
      default:
        return;
    }

    if (!fs.existsSync(logFile)) {
      fs.mkdirSync(path.dirname(logFile), { recursive: true });
      fs.writeFileSync(logFile, "# AI-activiteitenlog\n\nAutomatisch bijgehouden door `.claude/hooks/log-activity.js`.\n");
    }
    fs.appendFileSync(logFile, line + "\n");
  } catch (_) {
    // Loggen mag de AI nooit blokkeren
  }
  process.exit(0);
});
