--- a/collapse_profiling/parse_depth.py
+++ b/collapse_profiling/parse_depth.py
-import json, sys
-
-seen = set()
-count = 0
-
-for raw in sys.stdin:
-    line = raw.strip()
-    if line == "data: [DONE]":
-        break
-
-    # Pull out JSON after “data:”
-    if line.startswith("data:"):
-        payload = line[len("data:"):].strip()
-    elif line.startswith("{"):
-        payload = line
-    else:
-        continue
-
-    try:
-        obj = json.loads(payload)
-    except json.JSONDecodeError:
-        continue
-
-    delta = None
-
-    # OpenAI‐style
-    if "choices" in obj:
-        delta = obj["choices"][0].get("delta", {}).get("content", "")
-
-    # Anthropic: content_block_delta
-    elif obj.get("type") == "content_block_delta":
-        delta = obj.get("delta", {}).get("text", "")
-
-    # Anthropic: content_block_start (sometimes has initial text)
-    elif obj.get("type") == "content_block_start":
-        delta = obj.get("content_block", {}).get("text", "")
-
-    # Anthropic: fallback single‐message completion
-    elif "completion" in obj:
-        delta = obj["completion"].get("content", "")
-
-    if not delta or not isinstance(delta, str):
-        continue
-
-    delta = delta.strip()
-    if not delta:
-        continue
-
-    # First repeat = collapse
-    if delta in seen:
-        break
-
-    seen.add(delta)
-    count += 1
-
-print("Collapse depth:", count)
+import sys
+from collapse_profiling.parsers import iterate_deltas
+
+def main():
+    count = sum(1 for _ in iterate_deltas(sys.stdin))
+    print("Collapse depth:", count)
+
+if __name__ == "__main__":
+    main()
